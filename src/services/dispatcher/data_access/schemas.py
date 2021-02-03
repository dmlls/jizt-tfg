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

"""Marshmallow Schemas for DispatcherService."""

__version__ = '0.1.10'

from datetime import datetime
from marshmallow import Schema, fields, pre_dump, pre_load, EXCLUDE
from summary_status import SummaryStatus
from supported_models import SupportedModel
from supported_languages import SupportedLanguage


class Summary():
    """Summary class.

    A summary has the following attributes:

    * id_ (:obj:`str`): the id of the summary.
    * source (:obj:`str`): the source to process, e.g., a plain text
      to be summarized.
    * output (:obj:`str`): the output once the source has been
      processed, e.g., a summary.
    * model (:obj:`data_access.supported_models.SupportedModel`): the
      model with wich the summary was generated.
    * params (:obj:`dict`): the parameters with which the summary was
      generated.
    * status (:obj:`data_access.summary_status.SummaryStatus.COMPLETED`):
      the current status of the summary.
    * started_at (:obj:`datetime.datetime`): the time when the summary
      was first requested.
    * ended_at (:obj:`datetime.datetime`): the time when the summary
      first finished.
    * language (:obj:data_access.supported_languages.SupportedLanguage):
      the language of the summary.
    """

    def __init__(self,
                 id_: str,
                 source: str,
                 output: str,
                 model: SupportedModel,
                 params: dict,
                 status: SummaryStatus,
                 started_at: datetime,
                 ended_at: datetime,
                 language: SupportedLanguage
    ):  # 2020 be like
        self.id_ = id_
        self.source = source
        self.output = output
        self.model = model.value
        self.params = params
        self.status = status.value
        self.started_at = started_at
        self.ended_at = ended_at
        self.language = language.value

    def __str__(self):
        return (f'SUMMARY [id]: {self.id_}, [source]: "{self.source}", '
                f'[output]: "{self.output}", [model]: {self.model}, '
                f'[params]: {self.params}, [status]: {self.status}, '
                f'[started_at]: {self.started_at}, [ended_at]: {self.ended_at}, '
                f'[language]: {self.language}')

    def __repr__(self):
        return (f'Summary({self.id_}, {self.source}, {self.output}, '
                f'{self.model}, {self.params}, {self.status}, {self.started_at}, '
                f'{self.ended_at}, {self.language}')


class PlainTextRequestSchema(Schema):
    """Schema for the clients' plain-text REST requests.

    :code:`/v1/summaries/plain_text - POST`

    Fields:
        source (:obj:`str`):
            The text in plain format to be summarized.
        model (:obj:`str`, `optional`, defaults to :obj:`SupportedModel.T5_LARGE`):
            The model used to generate the summary.
        params (:obj:`dict`, `optional`, defaults to :obj:`{}`):
            The params used in the summary generation.
        language (:obj:`str`):
            The language of the text.
    """

    # length could be limited with validate=Length(max=600)
    source = fields.Str(required=True)
    model = fields.Str(required=True)
    params = fields.Dict(required=True)
    language = fields.Str(required=True)

    @pre_load
    def set_defaults(self, data, many, **kwargs):
        """Substitute :obj:`None` or missing fields by default values."""

        if "model" not in data or "model" in data and data["model"] is None:
            data["model"] = SupportedModel.T5_LARGE.value
        if "params" not in data or "params" in data and data["params"] is None:
            data["params"] = {}
        if "language" not in data or "language" in data and data["language"] is None:
            data["language"] = SupportedLanguage.ENGLISH.value
        return data

    class Meta:
        unknown = EXCLUDE


class ResponseSchema(Schema):
    """Schema for the response to the clients' requests.

    Some of the fields might not be available during the generation of
    the summary, e.g. ``output`` or ``ended_at``. Once the summary is
    ready, the ``status`` will change to ``completed``
    and the missing fields will be available then.

    Fields:
        started_at (:obj:`datetime.datetime`):
            The time when the summary was first created.
        ended_at (:obj:`datetime.datetime`):
            The time when the summary first finished.
        status (:obj:`str`):
            The current status of the summary.
        output (:obj:`str`):
            The processed text, e.g., the summary.
        model (:obj:`str`):
            The model with wich the summary was generated.
        params (:obj:`dict`):
            The parameters with which the summary was generated.
        language (:obj:`str`):
            The language of the summary.
    """

    summary_id = fields.Str(required=True)
    started_at = fields.DateTime(required=True)
    ended_at = fields.DateTime(required=True)
    status = fields.Str(required=True)
    output = fields.Str(required=True)
    model = fields.Str(required=True)
    params = fields.Dict(required=True)
    language = fields.Str(required=True)

    @pre_dump
    def summary_to_response(self, summary: Summary, **kwargs):
        """Transform a :obj:`Summary` object into a response.

        This method is executed when calling :meth:`Schema.dump`. Since a
        summary includes more information than it will be included in the
        response, e.g., its id, with this function we get only the necessary
        fields to form a response.

        For more information, see the
        `Marshmallow documentationn
        <https://marshmallow.readthedocs.io/en/stable/api_reference.html#marshmallow.pre_dump>`__.
        """

        return {"summary_id": summary.id_,
                "started_at": summary.started_at,
                "ended_at": summary.ended_at,
                "status": summary.status,
                "output": summary.output,
                "model": summary.model,
                "params": summary.params,
                "language": summary.language}

    class Meta:
        ordered = True


class TextPostprocessingConsumedMsgSchema(Schema):
    """Schema for the consumed messages from the topic :attr:`KafkaTopic.TEXT_POSTPROCESSING`.

    Fields:
        text_postprocessed (:obj:`str`):
            The post-processed text.
        params (:obj:`dict`):
            The valid params, onced checked by the summarizer.
    """

    text_postprocessed = fields.Str()
    params = fields.Dict(required=True)
