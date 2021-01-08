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

"""Kafka Consumer."""

__version__ = '0.1.0'

import logging
import socket
from datetime import datetime
from threading import Thread, Event
from kafka_topics import KafkaTopic
from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException
from confluent_kafka.serialization import StringDeserializer
from data_access.job_states import JobState
from data_access.job_dao_factory import JobDAOFactory
from data_access.schemas import TextPostprocessingConsumedMsgSchema


class StoppableThread(Thread):
    """Stoppable Thread.

    Threads that inherit from this class, once started with the method
    :meth:`Thread.start`, can be stopped calling the :meth:`StoppableThread.stop`
    method.
    """

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        """Stop the thread."""

        self._stop_event.set()

    def stopped(self):
        """Check whether the thread is stopped.

        Returns:
            :obj:`bool`: Whether the thread is stopped or not.
        """

        return self._stop_event.is_set()


class ConsumerLoop(StoppableThread):
    """Kafka consumer loop.

    This class implements a :class:`confluent_kafka.Consumer`.

    For more information, see the official Confluent Kafka
    `Consumer documentation
    <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#pythonclient-consumer>`__.
    """

    def __init__(self):
        super(ConsumerLoop, self).__init__()

        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("DispatcherConsumerLoop")

        # Consumer configuration. Must match Stimzi/Kafka configuration.
        config = {'bootstrap.servers': "jizt-cluster-kafka-bootstrap:9092",
                  'client.id': socket.gethostname(),
                  'group.id': "dispatcher",
                  'auto.offset.reset': "earliest",
                  'session.timeout.ms': 10000,
                  'enable.auto.commit': True,  # default
                  'auto.commit.interval.ms': 5000,  # default
                  'key.deserializer': StringDeserializer('utf_8'),
                  'value.deserializer': StringDeserializer('utf_8')}
        self.consumer = DeserializingConsumer(config)
        self.db = JobDAOFactory()
        self.consumed_msg_schema = TextPostprocessingConsumedMsgSchema()

    def run(self):
        try:
            topics_to_susbcribe = [KafkaTopic.READY.value]
            self.consumer.subscribe(topics_to_susbcribe)
            self.logger.debug(f'Consumer subscribed to topic(s): '
                              f'{topics_to_susbcribe}')

            while not self.stopped():
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        self.logger.error(f'{msg.topic()} in partition {msg.partition} '
                                          f'{msg.partition()} reached end at offset '
                                          f'{msg.offset()}')
                    elif msg.error():
                        self.logger.error("Undefined error in consumer loop")
                        raise KafkaException(msg.error())
                else:
                    self.logger.debug(f'Message consumed: [key]: {msg.key()}, '
                                      f'[value]: "{msg.value()[:50]} [...]"'
                    )
                    output = \
                        self.consumed_msg_schema.loads(msg.value())['text_postprocessed']
                    job = self.db.update_job(id_=msg.key(),
                                             ended_at=datetime.now(),
                                             state=JobState.COMPLETED.value,
                                             output=output
                    )
                    self.logger.debug(f"Consumer message processed. Job updated: {job}")
        finally:
            self.logger.debug("Consumer loop stopped. Closing consumer...")
            self.consumer.close()  # close down consumer to commit final offsets
