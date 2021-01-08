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

"""Job Data Access Object (DAO) Interface."""

__version__ = '0.1.0'

from schemas import Job


class JobDAOInterface:
    """DAO Interface for access to :obj:`Job` objects."""

    def get_job(self, id_: str):
        """Retrieve a job from the database.

        Args:
            id_ (obj:`str`):
                The job id.

        Returns:
            :obj:`Job`: The job with the specified id or
            :obj:`None` if there is not any job with that id.
        """

    def insert_job(self, job: Job):
        """Insert a new job to the database.

        Args:
            job (obj:`Job`):
                The job to be saved.
        """

    def update_job(self, id_: str, **kwargs):
        """Update an existing job.

        Args:
            id_ (obj:`str`):
                The job id.
            **kwargs:
                Fields of the job to be updated.

        Returns:
            :obj:`Job`: The updated job or :obj:`None` if
            there is not any job with the specified id.
        """

    def job_exists(self, id_: str):
        """Check whether a job already exists in the DB.

        Args:
            id_ (obj:`str`):
                The job id.

        Returns:
            :obj:`bool`: Whether the job exists or not.
        """
