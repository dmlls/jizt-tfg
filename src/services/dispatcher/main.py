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

__version__ = '0.1.7'

import os
import re
import argparse
import logging
import hashlib
from datetime import datetime
from werkzeug import serving
from flask import Flask, request
from flask_restful import Api, Resource, abort
from flask_cors import CORS
from confluent_kafka import Message, KafkaError
from kafka.kafka_topics import KafkaTopic
from kafka.kafka_producer import Producer
from kafka.kafka_consumer import ConsumerLoop
from data_access.summary_status import SummaryStatus
from data_access.summary_dao_factory import SummaryDAOFactory
from data_access.schemas import Summary, PlainTextRequestSchema, ResponseSchema
from data_access.supported_models import SupportedModel
from data_access.supported_languages import SupportedLanguage
from pathlib import Path

# Flask config
FLASK_HOST = "0.0.0.0"
FLASK_PORT = os.environ['FLASK_SERVER_PORT']

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
        * Manage the completed summaries, storing them in a DB for later
          retrieval.
    """

    def __init__(self, log_level):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.cors = CORS(self.app, resources={
            r"*": {"origins": "*",
                   "allow_headers": ['Content-Type']}
        })

        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("Dispatcher")
        logging.getLogger("flask_cors").level = log_level

        # PostgreSQL connection data
        pg_username = None
        pg_password = None
        with open((Path(os.environ['PG_SECRET_PATH'])
                   / Path(os.environ['PG_USERNAME_FILE'])), 'r') as username:
            pg_username = username.readline().rstrip('\n')
        with open((Path(os.environ['PG_SECRET_PATH'])
                   / Path(os.environ['PG_PASSWORD_FILE'])), 'r') as password:
            pg_password = password.readline().rstrip('\n')

        self.db = SummaryDAOFactory(
            os.environ['PG_HOST'],
            os.environ['PG_DBNAME'],
            pg_username,
            pg_password,
            log_level
        )

        # Create Kafka Producer and ConsumerLoop
        self.kafka_producer = Producer()
        self.kafka_consumerloop = ConsumerLoop(self.db)

        # Endpoints
        self.api.add_resource(
            PlainTextSummary,
            "/v1/summaries/plain-text",
            "/v1/summaries/plain-text/<summary_id>",
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
            self.app.run(host=FLASK_HOST,
                         port=FLASK_PORT,
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


class PlainTextSummary(Resource):
    """Resource for plain-text requests."""

    def __init__(self, **kwargs):
        self.request_schema = PlainTextRequestSchema()
        self.ok_response_schema = ResponseSchema()
        self.dispatcher_service = kwargs['dispatcher_service']
        self.kafka_producer = kwargs['kafka_producer']

    def post(self):
        """HTTP POST.

        Submit a request. When a client first makes a POST request, a response
        is given with the summary id. The client must then make periodic GET requests
        with the specific summary id to check the summary status. Once the summary
        is completed, the GET request will contain the output text, e.g., the summary.

        Returns:
            :obj:`dict`: A 202 Accepted response with a JSON body containing the
            summary id, e.g., {'summary_id': 73c3de4175449987ef6047f6e0bea91c1036a8599b}.
        Raises:
            :class:`http.client.HTTPException`: If the request body
            JSON is not valid.
        """

        data = request.json
        self._validate_post_request_json(data)

        loaded_data = self.request_schema.load(data)
        source = loaded_data['source']
        model = SupportedModel(loaded_data['model'])
        params = loaded_data['params']

        message_key = get_unique_key(source, model.value, params)  # summary id

        summary = None

        if self.dispatcher_service.db.summary_exists(message_key):
            summary = self.dispatcher_service.db.get_summary(message_key)
            self.dispatcher_service.logger.debug(
                f'Summary already exists: {summary}'
            )
        else:
            summary = Summary(
                          id_=message_key,
                          source=source,
                          output=None,
                          model=model,
                          params=params,
                          status=SummaryStatus.SUMMARIZING,
                          started_at=datetime.now(),
                          ended_at=None,
                          language=SupportedLanguage.ENGLISH
                      )
            self.dispatcher_service.db.insert_summary(summary)

            topic = KafkaTopic.TEXT_PREPROCESSING.value
            message_value = self.request_schema.dumps(data)
            self._produce_message(topic,
                                  message_key,
                                  message_value
            )

            self.dispatcher_service.logger.debug(
                        f'Message produced: [topic]: "{topic}", '
                        f'[key]: {message_key}, [value]: '
                        f'"{message_value[:500]} [...]"'
            )

        response = self.ok_response_schema.dump(summary)
        return response, 202  # ACCEPTED

    def get(self, summary_id):
        """HTTP GET.

        Gives a response with the summary status and, in case the summary
        is completed, the output text, e.g. the summary.

        Returns:
            :obj:`dict`: A ``200 OK`` response with a JSON body containing the
            summary. For info on the summary fields, see
            :class:`data_access.schemas.Summary`.
        Raises:
            :class:`http.client.HTTPException`: If there exists no summary
            with the specified id.
        """

        summary = self.dispatcher_service.db.get_summary(summary_id)
        if summary is None:
            abort(404, errors=f'Summary {summary_id} not found.')  # NOT FOUND
        response = self.ok_response_schema.dump(summary)
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
            :obj:`dict`: A ``200 OK`` response if everything is working, otherwise
            a ``500 INTERNAL SERVER ERROR``.
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


def get_unique_key(source: str, model: str, params: dict) -> str:
    """Get a unique key for a message.

    This method hashes the string formed by concatenating the
    :attr:`source`, :attr:`model` and :attr:`param` attributes.
    SHA-256 algorithm is used.

    Args:
        source (:obj:`str`):
            ``source`` attribute in the JSON body of the request.
        model (:obj:`str`):
            ``model`` attribute in the JSON body of the request.
        params (:obj:`params`):
            ``params`` attribute in the JSON body of the request.

    Returns:
        :obj:`str`: The unique, SHA-256 ecrypted key.
    """

    return hashlib.sha256(
        ("".join([source, model, str(params)])).encode()
    ).hexdigest()


def disable_endpoint_logs():
    """Disable logs for requests to specific endpoints."""

    disabled_endpoints = ('/', '/healthz', '/v1/summaries/plain-text/.+')

    parent_log_request = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        """See `base class <https://github.com/pallets/werkzeug/blob/71cf9902012338f8ee98338fa7bba50572606637/src/werkzeug/serving.py#L378>`__."""

        if not any(re.match(f"{de}$", self.path) for de in disabled_endpoints):
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

    disable_endpoint_logs()

    dispatcher_service = DispatcherService(log_level)
    dispatcher_service.run()
