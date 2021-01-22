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

"""Marshmallow Schemas for TextPreprocessorService."""

from marshmallow import Schema, fields

__version__ = '0.1.4'


class TextPreprocessingConsumedMsgSchema(Schema):
    """Schema for the consumed messages from the topic :attr:`KafkaTopic.TEXT_PREPROCESSING`.

    Fields:
        source (:obj:`str`):
            The text in plain format to be summarized.
        model (:obj:`str`):
            The model used to generate the summary.
        params (:obj:`dict`):
            The params used in the summary generation.
    """

    source = fields.Str(required=True)
    model = fields.Str(required=True)
    params = fields.Dict(required=True)


class TextEncodingProducedMsgSchema(Schema):
    """Schema for the produced messages to the topic :attr:`KafkaTopic.TEXT_ENCODING`.

    Fields:
        text_preprocessed (:obj:`str`):
            The pre-processed text.
        model (:obj:`str`):
            The model used to generate the summary.
        params (:obj:`dict`):
            The params used in the summary generation.
    """

    text_preprocessed = fields.Str(required=True)
    model = fields.Str(required=True)
    params = fields.Dict(required=True)
