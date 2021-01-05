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

"""Kafka Producer."""

__version__ = '0.1.0'

import socket
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer


class Producer:
    """Wrapper class around :obj:`confluent_kafka.Producer`.

    It includes the specific producer configuration. When
    a :obj:`Producer` is instanciated, it will return
    a :obj:`confluent_kafka.Producer`.

    For more information, see the official Confluent Kafka `Producer documentation
    <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/#producer>`__.
    """

    def __new__(cls):
        # Producer configuration. Must match Stimzi/Kafka configuration.
        config = {'bootstrap.servers': "jizt-cluster-kafka-bootstrap:9092",
                  'client.id': socket.gethostname(),
                  'key.serializer': StringSerializer('utf_8'),
                  'value.serializer': StringSerializer('utf_8')}
        return SerializingProducer(config)
