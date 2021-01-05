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

__version__ = '0.1.5'

from marshmallow import Schema, fields, pre_dump
from datetime import datetime


class Job():
    """Job class.

    A job is a request being processed.

    Jobs has the following fields:

    * id_ (:obj:`int`): the id of the job.
    * started_at (:obj:`datetime.datetime`): the time when the job
      was created.
    * ended_at (:obj:`datetime.datetime`): the time when the job
      finished.
    * state (:obj:`str`): the state of the job.
    * source (:obj:`str`): the source to process, e.g., a plain text
      to be summarized.
    * output (:obj:`str`): the output once the source has been
      processed, e.g., a summary.
    """

    def __init__(self,
                 id_: int,
                 started_at: datetime,
                 ended_at: datetime,
                 state: str,
                 source: str,
                 output: str
    ):  # 2020 be like
        self.id_ = id_
        self.started_at = started_at
        self.ended_at = ended_at
        self.state = state
        self.source = source
        self.output = output

    def __str__(self):
        source = None if self.source is None else self.source[:30]
        output = None if self.output is None else self.output[:30]
        return (f'JOB [id]: {self.id_}, [started_at]: {self.started_at}, '
                f'[ended_at]: {self.ended_at}, [state]: "{self.state}", '
                f'[source]: "{source} [...]", '
                f'[output]: "{output} [...]"')


class PlainTextRequestSchema(Schema):
    """Schema for the clients' plain-text REST requests.

    :code:`/v1/summaries/plain_text - POST`

    Fields:
        source (:obj:`str`):
            The text in plain format to be summarized.
    """

    # length could be limited with validate=Length(max=600)
    source = fields.Str(required=True)

    class Meta:
        ordered = True


class AcceptedResponseSchema(Schema):
    """Schema for the 202 ACCEPTED response.

    When a client first makes a POST request, a response is given with the
    job id. The client must then make periodic GET requests with the specific
    job id to check the job status. Once the job is completed, the GET request
    will contain the output text, e.g., the summary.

    Fields:
        job_id (:obj:`int`):
          The job id. The following GET requests be made to the proper endpoint
          containing this job id.
    """

    job_id = fields.Int(required=True)

    @pre_dump
    def job_to_response(self, job: Job, **kwargs):
        """Transform a :obj:`Job` object into a response.

        This method is executed when calling :meth:`Schema.dump`. Since a
        job includes more information than it will be included in the response,
        with this function we get only the necessary fields to form a response.

        For more information, see the
        `Marshmallow documentationn
        <https://marshmallow.readthedocs.io/en/stable/api_reference.html#marshmallow.pre_dump>`__.

        """

        return {"job_id": job.id_}

    class Meta:
        ordered = True


class OkResponseSchema(Schema):
    """Schema for the 200 OK response.

    This response contains the job status. Once the text processing
    is completed, the response will also contain the output text, e.g.,
    the summary.

    Fields:
        started_at (:obj:`datetime.datetime`):
          The time when the job was created.
        ended_at (:obj:`datetime.datetime`):
          The time when the job finished.
        state (:obj:`str`):
          The state of the job.
        output (:obj:`str`):
            The processed text, e.g., the summary.
    """

    started_at = fields.DateTime(required=True)
    ended_at = fields.DateTime(required=True)
    state = fields.Str(required=True)
    output = fields.Str(required=True)

    @pre_dump
    def job_to_response(self, job: Job, **kwargs):
        """Transform a :obj:`Job` object into a response.

        This method is executed when calling :meth:`Schema.dump`. Since a
        job includes more information than it will be included in the response,
        e.g., its id, with this function we get only the necessary fields to
        form a response.

        For more information, see the
        `Marshmallow documentationn
        <https://marshmallow.readthedocs.io/en/stable/api_reference.html#marshmallow.pre_dump>`__.
        """

        return {"started_at": job.started_at,
                "ended_at": job.ended_at,
                "state": job.state,
                "output": job.output}

    class Meta:
        ordered = True


class TextPostprocessingConsumedMsgSchema(Schema):
    """Schema for the consumed messages from the topic :attr:`KafkaTopic.TEXT_POSTPROCESSING`."""

    text_postprocessed = fields.Str()

    class Meta:
        ordered = True
