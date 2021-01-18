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

"""Extensions to psygopg2 module."""

__version__ = '0.1.0'

import psycopg2
import psycopg2.extensions
import logging


class LoggingCursor(psycopg2.extensions.cursor):
    """Cursor with logging capacities."""

    def __init__(self, log_level, *args, **kwargs):
        super(LoggingCursor, self).__init__(*args, **kwargs)
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level= log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger('Dispatcher-DB')

    def execute(self, sql, args=None):
        """See base class."""

        self.logger.debug(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as ex:
            self.logger.error(ex)
            raise
