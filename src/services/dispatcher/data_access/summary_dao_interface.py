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

"""Summary Data Access Object (DAO) Interface."""

__version__ = '0.1.0'

from schemas import Summary


class SummaryDAOInterface:
    """DAO Interface for access to :obj:`Summary` objects."""

    def get_summary(self, id_: str):
        """Retrieve a summary from the database.

        Args:
            id_ (obj:`str`):
                The summary id.

        Returns:
            :obj:`Summary`: The summary with the specified id or
            :obj:`None` if there is not any summary with that id.
        """

    def insert_summary(self, summary: Summary):
        """Insert a new summary to the database.

        Args:
            summary (obj:`Summary`):
                The summary to be saved.
        """

    def update_summary(self, id_: str, **kwargs):
        """Update an existing summary.

        Args:
            id_ (obj:`str`):
                The summary id.
            **kwargs:
                Fields of the summary to be updated.

        Returns:
            :obj:`Summary`: The updated summary or :obj:`None` if
            there is not any summary with the specified id.
        """

    def summary_exists(self, id_: str):
        """Check whether a summary already exists in the DB.

        Args:
            id_ (obj:`str`):
                The summary id.

        Returns:
            :obj:`bool`: Whether the summary exists or not.
        """
