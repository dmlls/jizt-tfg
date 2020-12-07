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

"""REST API v1 for the text preprocessor."""

import argparse
import logging
from flask import Flask, request, abort
from flask_restful import Api, Resource
from text_preprocessing import TextPreprocessor

__version__ = '0.1'

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

        self.api.add_resource(TextPreprocessing, 'v1/preprocessors/plain_text', endpoint='preprocess_plain_text')

    def run(self):
        self.app.run(debug=True)


class TextPreprocessing(Resource):
    def post(self):


if __name__ == "__main__":
    argparse = parser.parse_args()
    info_log_level = args.info
    debug_log_level = args.debug

    log_level = logging.WARNING
    if info_log_level:
        log_level = logging.INFO
    if debug_log_level:
        log_level = logging.DEBUG
    
    text_preprocessor_service = TextPreprocessorService(log_level)