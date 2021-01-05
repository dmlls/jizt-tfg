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

"""Marshmallow Schemas for TextEncoderService."""

from marshmallow import Schema, fields

__version__ = '0.1.2'


class TextEncodingConsumedMsgSchema(Schema):
    """Schema for the consumed messages from the topic :attr:`KafkaTopic.TEXT_ENCODING`.

    Fields:
        text_preprocessed (:obj:`str`):
            The text to be encoded.
    """

    text_preprocessed = fields.Str(required=True)

    class Meta:
        ordered = True


class TextSumarizationProducedMsgSchema(Schema):
    """Schema for the produced messages to the topic :attr:`KafkaTopic.TEXT_SUMMARIZATION`.

    Fields:
        text_encoded (:obj:`str`):
            The encoded text.
    """

    text_encoded = fields.Str(required=True)

    class Meta:
        ordered = True
