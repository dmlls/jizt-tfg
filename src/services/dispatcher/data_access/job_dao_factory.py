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

__version__ = '0.1.0'

from job_dao_postgresql import JobDAOPostgresql


class JobDAOFactory:
    """Job DAO Factory."""

    _instance = None

    def __new__(cls):
        """Pythonic singleton."""
        if cls._instance is None:
            cls._instance = JobDAOPostgresql()
        return cls._instance
