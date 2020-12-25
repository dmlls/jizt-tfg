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

"""Job Data Access Object (DAO) Implementation."""

__version__ = '0.1.0'

from job_dao_interface import JobDAOInterface
from schemas import Job


class JobDAOPostgresql(JobDAOInterface):
    """Job DAO implementation for Postgresql.

    For more information, see base class.
    """

    def get_job(self, id: int):
        """See base class."""

        pass  # TODO

    def save_job(self, job: Job):
        """See base class."""

        pass  # TODO


    def job_exists(self, id: int):
        """See base class."""

        pass  # TODO