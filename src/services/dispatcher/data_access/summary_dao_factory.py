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

"""Data Access Object (DAO) Factory."""

__version__ = '0.1.3'

import logging
from summary_dao_postgresql import SummaryDAOPostgresql


class SummaryDAOFactory:
    """Summary DAO Factory."""

    _instance = None

    def __new__(cls,
                host: str,
                dbname: str,
                user: str,
                password: str,
                log_level: int = logging.ERROR
    ) -> SummaryDAOPostgresql:
        """Singleton.

        Args:
            host (:obj:`str`):
                The database host.
            dbname (:obj:`str`):
                The database name.
            user (:obj:`str`):
                The database user.
            password (:obj:`str`):
                The user's password.
            log_level (:obj:`int`, `optional`, defaults to logging.ERROR):
                The log level.

        Returns:
            :obj:`SummaryDAOFactory`: The single instance
            of the DAO.
        """

        if cls._instance is None:
            cls._instance = SummaryDAOPostgresql(
                host,
                dbname,
                user,
                password,
                log_level
            )
        return cls._instance
