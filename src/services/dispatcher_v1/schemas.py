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

"""Marshmallow Schemas for DispatcherService."""

from marshmallow import Schema, fields

__version__ = '0.1'

class PlainTextRequestSchema(Schema):
    """Schema for the clients' plain-text REST requests.

    :code:`/v1/summaries/plain_text - POST`

    Fields:
        source (:obj:`str`):
            The text in plain format to be summarized.
        TODO: add more fields.
    """

    # length could be limited with validate=Length(max=600)
    source = fields.Str(required=True)

#TODO: class TwitterThreadRequestSchema(Schema)

class PlainTextResponseSchema(Schema):
    """Schema for the plain-text REST response.
    
    This response contains the summarized text.

    Fields:
        summary (:obj:`str`):
            The summarized text.
        TODO: add more fields.
    """

    summary = fields.Str()