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

"""Test Preprocessor REST API v1."""

import argparse
import logging
import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, abort
from text_preprocessing import TextPreprocessor
from schemas import PlainTextRequestSchema, PlainTextResponseSchema

__version__ = '0.1'

HOST = "0.0.0.0" # host for Flask server
PORT = 5001 # port for Flask server

parser = argparse.ArgumentParser(description='Text pre-processing service. ' + \
                                             'Default log level is WARNING.')
parser.add_argument('-i', '--info', action='store_true',
                    help='turn on python logging to INFO level')
parser.add_argument('-d', '--debug', action='store_true',
                    help='turn on python logging and flask to DEBUG level')

class TextPreprocessorService:
    """Text pre-processing service."""
    def __init__(self, log_level):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.log_level = log_level
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=self.log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )

        self.api.add_resource(PlainTextPreprocessing, '/v1/preprocessors/plain-text',
                              endpoint='preprocess_plain_text')

    def run(self):
        self.app.run(host=HOST, port=PORT, debug=(self.log_level == logging.DEBUG))


class PlainTextPreprocessing(Resource):
    """Resource for plain text preprocessing."""

    def __init__(self):
        self.request_schema = PlainTextRequestSchema()
        self.response_schema = PlainTextResponseSchema()

    def post(self):
        data = request.json
        self._validate_request_json(data)
        preprocessed_text = TextPreprocessor.preprocess(data['source'])
        response = {"preprocessed_text": preprocessed_text}
        return make_response(jsonify(response), 200)
    
    def _validate_request_json(self, json):
        """Validates the JSON in the request body.
        
        The JSON will not be valid if it does not contain
        all the mandatodry fields defined in the
        :class:`.schemas.PlainTextRequestSchema` class. 

        If the JSON is not valid, an HTTPException is raised.

        Args:
            TODO 
        """

        errors = self.request_schema.validate(json)
        if errors:
            abort(400, errors=errors) # 400 BAD REQUEST

if __name__ == "__main__":
    args = parser.parse_args()
    info_log_level = args.info
    debug_log_level = args.debug

    log_level = logging.WARNING
    if info_log_level:
        log_level = logging.INFO
    if debug_log_level:
        log_level = logging.DEBUG
    
    text_preprocessor_service = TextPreprocessorService(log_level)
    text_preprocessor_service.run()