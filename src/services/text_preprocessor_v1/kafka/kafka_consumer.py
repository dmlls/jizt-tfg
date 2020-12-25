# Copyright (C) 2020 Diego Miguel Lozano <dml1001@alu.ubu.es>
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

import socket
from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer


class Consumer:
    """Wrapper class around :obj:`confluent_kafka.DeserializingConsumer`.

    It includes the specific consumer configuration. When
    a :obj:`Consumer` is instanciated, it will return
    a :obj:`confluent_kafka.DeserializingConsumer`.

    For more information, see the official Confluent Kafka
    `DeserializingConsumer documentation
    <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#deserializingconsumer>`__.
    """

    def __new__(self):
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
        return DeserializingConsumer(config)