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

"""Dispatcher REST API v1."""

import argparse
import logging
import socket
import requests
import json
from flask import Flask, request
from flask_restful import Api, Resource, abort
from schemas import PlainTextRequestSchema, PlainTextResponseSchema

__version__ = '0.1.1'

# JSON containing the service configuration
SVC_CONFIG_FILE = "svc_config.json"

# Args for Python script execution.
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
        * Forward the request to the proper microservice.
        * TODO: manage asynchronism.
    """

    def __init__(self, log_level, svc_config: dict):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.log_level = log_level
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=self.log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )

        self.svc_config = svc_config

        # /v1/summaries/plain-text
        self.api.add_resource(
            PlainText,
            self.svc_config["self"]["endpoints"]["v1"]["plain-text"],
            resource_class_kwargs={'svc_config': self.svc_config}
        )

    def run(self):
        self.app.run(host="0.0.0.0",  # make the server publicly available
                     port=self.svc_config["self"]["port"],
                     debug=(self.log_level == logging.DEBUG))


class PlainText(Resource):
    """Resource for plain-text requests."""

    def __init__(self, **kwargs):
        self.request_schema = PlainTextRequestSchema()
        self.response_schema = PlainTextResponseSchema()
        self.svc_config = kwargs['svc_config']

    def post(self):
        """HTTP POST.

        Forward the request to the preprocessor.

        #TODO: update docstring.

        Returns:
            :obj:`tuple`: The text preprocessed and the
            response code 200 OK.

        Raises:
            :class:`http.client.HTTPException`: If the body
            JSON is not valid.
        """

        data = request.json
        self._validate_request_json(data)
        # DNS lookup
        text_preprocessor_svc_ip = socket.gethostbyname(
                                       self.svc_config["text-preprocessor"]["name"])
        url = (
            f"http://{text_preprocessor_svc_ip}:"
            f"{self.svc_config['text-preprocessor']['port']}"
            f"{self.svc_config['text-preprocessor']['endpoints']['v1']['plain-text']}"
        )
        response = requests.post(url, json=data).json()
        return response, 200

    def _validate_request_json(self, json):
        """Validate JSON in the request body.

        The JSON will not be valid if it does not contain
        all the mandatodry fields defined in the
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
            abort(400, errors=errors)  # 400 BAD REQUEST


if __name__ == "__main__":
    args = parser.parse_args()
    info_log_level = args.info
    debug_log_level = args.debug

    log_level = logging.WARNING
    if info_log_level:
        log_level = logging.INFO
    if debug_log_level:
        log_level = logging.DEBUG

    svc_config = {}
    with open(SVC_CONFIG_FILE, 'r') as config:
        svc_config = json.load(config)

    dispatcher_service = DispatcherService(log_level, svc_config)
    dispatcher_service.run()