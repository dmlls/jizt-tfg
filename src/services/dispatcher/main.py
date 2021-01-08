# Copyright (C) 2021 Diego Miguel Lozano <dml1001@alu.ubu.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For license information on the libraries used, see LICENSE.

"""Dispatcher REST API v1."""

__version__ = '0.1.2'

import argparse
import logging
import hashlib
from datetime import datetime
from werkzeug import serving
from flask import Flask, request
from flask_restful import Api, Resource, abort
from confluent_kafka import Message, KafkaError
from kafka.kafka_topics import KafkaTopic
from kafka.kafka_producer import Producer
from kafka.kafka_consumer import ConsumerLoop
from data_access.job_states import JobState
from data_access.job_dao_factory import JobDAOFactory
from data_access.schemas import (Job, PlainTextRequestSchema,
                                 AcceptedResponseSchema, OkResponseSchema)

# Host for Flask server
HOST = "0.0.0.0"  # make the server publicly available

# Port for Flask server
PORT = 5000

# Args for Python script execution
parser = argparse.ArgumentParser(description='Dispatcher service. '
                                             'Default log level is WARNING.')
parser.add_argument('-i', '--info', action='store_true',
                    help='turn on Python logging to INFO level')
parser.add_argument('-d', '--debug', action='store_true',
                    help='turn on Python logging and Flask to DEBUG level')


class DispatcherService:
    """Dispatcher service.

    This service carries out several tasks:

        * Validate the clients' requests, making sure the body contains
          the necessary fields.
        * Publish messages to the proper microservice Kafka topic, in order
          to begin the text processing.
        * Manage the completed jobs, i.e., the texts that have been already
          processed, storing them in a DB for later retrieval.
    """

    def __init__(self, log_level):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("Dispatcher")

        # Create Kafka Producer and ConsumerLoop
        self.kafka_producer = Producer()
        self.kafka_consumerloop = ConsumerLoop()
        # Get DB
        self.db = JobDAOFactory()

        # Endpoints
        self.api.add_resource(
            PlainText,
            "/v1/summaries/plain-text",
            "/v1/summaries/plain-text/<job_id>",
            endpoint="plain-text-summarization",
            resource_class_kwargs={'dispatcher_service': self,
                                   'kafka_producer': self.kafka_producer}
        )

        self.api.add_resource(
            Health,
            "/",
            "/healthz",
            endpoint="readiness-liveness-probe",
            resource_class_kwargs={'dispatcher_service': self,
                                   'kafka_producer': self.kafka_producer}
        )

    def run(self):
        try:
            self.kafka_consumerloop.start()
            self.app.run(host=HOST,
                         port=PORT,
                         debug=(self.logger.level == "DEBUG")
            )
        finally:
            self.kafka_consumerloop.stop()

    def kafka_delivery_callback(self, err: KafkaError, msg: Message):
        """Kafka per-message delivery callback.

        When passed to :meth:`confluent_kafka.Producer.produce` through
        the :attr:`on_delivery` attribute, this method will be triggered
        by :meth:`confluent_kafka.Producer.poll` or
        :meth:`confluent_kafka.Producer.flush` when wither a message has
        been successfully delivered or the delivery failed (after
        specified retries).

        Args:
            err (:obj:`confluent_kafka.KafkaError`):
                The Kafka error.
            msg (:obj:`confluent_kafka.Message`):
                The produced message, or an event.
        """

        if err:
            self.logger.debug(f'Message delivery failed: {err}')
        else:
            self.logger.debug(f'Message delivered sucessfully: [topic]: '
                              f'"{msg.topic()}", [partition]: "{msg.partition()}"'
                              f', [offset]: {msg.offset()}')


class PlainText(Resource):
    """Resource for plain-text requests."""

    def __init__(self, **kwargs):
        self.request_schema = PlainTextRequestSchema()
        self.accepted_response_schema = AcceptedResponseSchema()
        self.ok_response_schema = OkResponseSchema()
        self.dispatcher_service = kwargs['dispatcher_service']
        self.kafka_producer = kwargs['kafka_producer']

    def post(self):
        """HTTP POST.

        Submit a request. When a client first makes a POST request, a response
        is given with the job id. The client must then make periodic GET requests
        with the specific job id to check the job status. Once the job is completed,
        the GET request will contain the output text, e.g., the summary.

        Returns:
            :obj:`dict`: A 202 Accepted response with a JSON body containing the
            job id, e.g., {'job_id': 73c3de4175449987ef6047f6e0bea91c1036a8599b}.
        Raises:
            :class:`http.client.HTTPException`: If the request body
            JSON is not valid.
        """

        data = request.json
        self._validate_post_request_json(data)

        source = self.request_schema.load(data)['source']
        message_key = get_unique_key(source)  # job id

        job = None

        if self.dispatcher_service.db.job_exists(message_key):
            job = self.dispatcher_service.db.get_job(message_key)
            self.dispatcher_service.logger.debug(
                f'Job already exists: {job}'
            )
        else:
            job = Job(id_=message_key,
                      started_at=datetime.now(),
                      ended_at=None,
                    #   state=JobState.PREPROCESSING.value,
                      state="processing",  #TODO: implement states
                      source=source,
                      output=None
            )
            self.dispatcher_service.db.insert_job(job)

            topic = KafkaTopic.TEXT_PREPROCESSING.value
            message_value = self.request_schema.dumps(data)
            self._produce_message(topic,
                                  message_key,
                                  message_value
            )

            self.dispatcher_service.logger.debug(
                        f'Message produced: [topic]: "{topic}", '
                        f'[key]: {message_key}, [value]: '
                        f'"{message_value[:50]} [...]"'
            )

        response = self.accepted_response_schema.dump(job)
        return response, 202  # ACCEPTED

    def get(self, job_id):
        """HTTP GET.

        Gives a response with the job status and, in case the job
        is completed, the output text, e.g. the summary.

        Returns:
            :obj:`dict`: A 200 OK response with a JSON body containing the
            job. For info on the job fields, see :class:`data_access.schemas.Job`.
        Raises:
            :class:`http.client.HTTPException`: If there exists no job
            with the specified id.
        """

        job = self.dispatcher_service.db.get_job(job_id)
        if job is None:
            abort(404, errors=f'Job {job_id} not found.')  # NOT FOUND
        response = self.ok_response_schema.dump(job)
        return response, 200  # OK

    def _validate_post_request_json(self, json):
        """Validate JSON in a POST request body.

        The JSON will not be valid if it does not contain
        all the mandatory fields defined in the
        :class:`.schemas.PlainTextRequestSchema` class.

        Args:
            json (:obj:`dict`):
                The JSON to be validated.

        Raises:
            :class:`http.client.HTTPException`: If the JSON
            is not valid.
        """

        errors = self.request_schema.validate(json)
        if errors:
            abort(400, errors=errors)  # 400 Bad Request

    def _produce_message(self,
                         topic: str,
                         message_key: int,
                         message_value: str):
        """Produce Kafka message.

        If the local producer queue is full, the request will be
        aborted.

        Args:
            topic (:obj:`str`):
                The topic to produce the message to.
            message_key (:obj:`int`);
                The Kafka message key.
            message_value (:obj:`str`);
                The Kafka message value.
        """

        try:
            self.kafka_producer.produce(
                topic,
                key=str(message_key),
                value=message_value,
                on_delivery=self.dispatcher_service.kafka_delivery_callback
            )
        except BufferError:
            error_msg = (f"Local producer queue is full ({len(self.kafka_producer)} "
                         f"messages awaiting delivery)")
            self.dispatcher_service.logger.error(error_msg)
            abort(503, error=error_msg)  # 503 Service Unavailable

        # Wait up to 1 second for events. Callbacks will
        # be invoked during this method call.
        self.kafka_producer.poll(1)


class Health(Resource):
    """Resource for probing service liveness."""

    def __init__(self, **kwargs):
        self.dispatcher_service = kwargs['dispatcher_service']
        self.kafka_producer = kwargs['kafka_producer']

    def get(self):
        """Check service health.

        Returns:
            :obj:`dict`: A 200 OK response if everything is working, otherwise
            a 500 INTERNAL SERVER ERROR.
        """

        return 200 if (self._is_kafka_producer_alive()
                       and self._is_kafka_consumer_alive()) else 500

    def _is_kafka_producer_alive(self):
        """Check if Kafka producer is up and running.

        Returns:
            :obj:`bool`: whether the producer is alive or not.
        """

        return (self.kafka_producer is not None
                and self.kafka_producer.list_topics().topics)

    def _is_kafka_consumer_alive(self):
        """Check if Kafka consumer is up and running.

        Returns:
            :obj:`bool`: whether the consumer is alive or not.
        """
        return not self.dispatcher_service.kafka_consumerloop.stopped()


def get_unique_key(source: str) -> str:
    """Get a unique key for a message.

    This method hashes the content of :attr:`source`. SHA-256
    algorithm is used.

    Args:
        source (:obj:`str`):
            `source` field in the JSON body of the request.

    Returns:
        :obj:`str`: The unique, SHA-256 ecrypted key.
    """

    return hashlib.sha256(source.encode()).hexdigest()


def disable_healthcheck_logs():
    """Disable logs for healthcheck requests from Kubernetes/GKE."""

    health_check_endpoints = ('/', '/healthz')

    parent_log_request = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        """See `base class <https://github.com/pallets/werkzeug/blob/71cf9902012338f8ee98338fa7bba50572606637/src/werkzeug/serving.py#L378>`__."""

        if self.path not in health_check_endpoints:
            parent_log_request(self, *args, **kwargs)

    serving.WSGIRequestHandler.log_request = log_request


if __name__ == "__main__":
    args = parser.parse_args()
    info_log_level = args.info
    debug_log_level = args.debug

    log_level = logging.WARNING
    if info_log_level:
        log_level = logging.INFO
    if debug_log_level:
        log_level = logging.DEBUG
    else:
        disable_healthcheck_logs()

    dispatcher_service = DispatcherService(log_level)
    dispatcher_service.run()
