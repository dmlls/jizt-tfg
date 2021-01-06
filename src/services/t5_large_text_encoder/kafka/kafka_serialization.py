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

"""Kafka Serialization and Deserialization."""

__version__ = '0.1.0'

import pickle
from confluent_kafka.serialization import Serializer, Deserializer


class TorchTensorSerializer(Serializer):
    """Serialize :obj:`torch.Tensor` to :obj:`bytes`.

    For more information on Kafka serialization, see the 
    `Python Confluent Kafka docs
    <https://docs.confluent.io/5.5.0/clients/confluent-kafka-python/index.html#confluent_kafka.serialization.Serializer>`__.
    """

    def __call__(self, obj, ctx):
        """Serialize :obj:`torch.Tensor` as :obj:`bytes`.

        Args:
            obj (:obj:`object`):
                The object to be serialized.
            ctx (:obj:`confluent_kafka.serialization.SerializationContext`):
                Metadata pertaining to the serialization operation.

        Returns:
            :obj:`bytes` or :obj:`None`: the serialized object if :attr:`obj`
            is not :obj:`None`, else :obj:`None`.
        """

        if obj is None:
            return None

        return pickle.dumps(obj)


class TorchTensorDeserializer(Deserializer):
    """Deserialize a :obj:`torch.Tensor` from :obj:`bytes`.

    For more information on Kafka deserialization, see the 
    `Python Confluent Kafka docs
    <https://docs.confluent.io/5.5.0/clients/confluent-kafka-python/index.html#confluent_kafka.serialization.Deserializer>`__.
    """

    def __call__(self, value, ctx):
        """Deserialize a :obj:`torch.Tensor` from :obj:`bytes`.

        Args:
            obj (:obj:`bytes`):
                The bytes to be deserialized.
            ctx (:obj:`confluent_kafka.serialization.SerializationContext`):
                Metadata pertaining to the serialization operation.

        Returns:
            :obj:`torch.Tensor` or :obj:`None`: the deserialized object if :attr:`obj`
            is not :obj:`None`, else :obj:`None`.
        """

        if value is None:
            return None

        return pickle.loads(value)
