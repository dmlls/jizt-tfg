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

"""Summary Data Access Object (DAO) Implementation."""

__version__ = '0.1.3'

import logging
import psycopg2
import hashlib
from io import StringIO
from collections import OrderedDict
from psycopg2.extras import Json
from summary_dao_interface import SummaryDAOInterface
from schemas import Summary
from summary_status import SummaryStatus
from supported_models import SupportedModel
from supported_languages import SupportedLanguage


class SummaryDAOPostgresql(SummaryDAOInterface):  # TODO: manage errors in excepts
    """Summary DAO implementation for Postgresql.

    For more information, see base class.
    """

    def __init__(self, host, dbname, user, password, log_level):
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("SummaryDAOPostgresql")

        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password

    def get_summary(self, id_: str):
        """See base class."""

        SQL = """SELECT summary_id, content, summary, model_name, params,
                        status, started_at, ended_at, language_tag
                 FROM jizt.summary JOIN jizt.source USING (source_id)
                 WHERE summary_id = %s;"""

        conn = None

        try:
            conn = self._connect()
            with conn.cursor() as cur:
                cur.execute(SQL, (id_,))
                summary_row = cur.fetchone()
                if summary_row is not None:
                    return Summary(
                        id_=summary_row[0],
                        source=summary_row[1],
                        output=summary_row[2],
                        model=SupportedModel(summary_row[3]),
                        params=summary_row[4],
                        status=SummaryStatus(summary_row[5]),
                        started_at=summary_row[6],
                        ended_at=summary_row[7],
                        language=SupportedLanguage(summary_row[8])
                    )
                return None  # summary doesn't exist
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)
        finally:
            if conn is not None:
                conn.close()

    def insert_summary(self, summary: Summary):
        """See base class."""

        SQL_GET_SOURCE = """SELECT source_id
                            FROM jizt.source
                            WHERE source_id = %s;"""

        SQL_INSERT_SOURCE = """INSERT INTO jizt.source
                               VALUES (%s, %s, %s);"""

        SQL_SUMMARY = """INSERT INTO jizt.summary
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        conn = None

        try:
            conn = self._connect()
            with conn.cursor() as cur:
                source_id = self._get_unique_key(summary.source)
                cur.execute(SQL_GET_SOURCE, (source_id,))
                retrieved_source_id = cur.fetchone()
                if retrieved_source_id is None:
                    cur.execute(
                        SQL_INSERT_SOURCE,
                        (source_id, summary.source, len(summary.source))
                    )
                output_length = (len(summary.output) if summary.output is not None
                                 else None)
                cur.execute(SQL_SUMMARY, (summary.id_, source_id,
                                          summary.output, output_length,
                                          summary.model, Json(summary.params),
                                          summary.status, summary.started_at,
                                          summary.ended_at, summary.language))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def _get_unique_key(text: str) -> str:
        """Get a unique key for a text.

        SHA-256 algorithm is used.

        Args:
            text (:obj:`str`):
                The text to get the unique id from.

        Returns:
            :obj:`str`: The unique, SHA-256 ecrypted key.
        """

        return hashlib.sha256(text.encode()).hexdigest()

    def update_summary(self, id_: str, **kwargs):
        """See base class."""

        ordered_kwargs = OrderedDict(kwargs)

        # Convert dicts to Json
        dicts = [key for key in ordered_kwargs
                 if isinstance(ordered_kwargs[key], dict)]
        for key in dicts:
            ordered_kwargs[key] = Json(ordered_kwargs[key])

        keys = list(ordered_kwargs.keys())
        values = list(ordered_kwargs.values()) + [id_]
        concat = StringIO()
        concat.write("UPDATE jizt.summary SET ")
        for field in keys[:-1]:
            concat.write(f"{field} = %s, ")
        concat.write(f"{keys[-1]} = %s WHERE summary_id = %s;")

        SQL = concat.getvalue()

        if self.summary_exists(id_):
            conn = None
            try:
                conn = self._connect()
                with conn.cursor() as cur:
                    cur.execute(SQL, values)
                    if cur.rowcount == 0:  # nothing updated
                        return None
                    conn.commit()
                    return self.get_summary(id_)
            except (Exception, psycopg2.DatabaseError) as error:
                self.logger.error(error)
            finally:
                if conn is not None:
                    conn.close()
        else:
            return None

    def summary_exists(self, id_: str):
        """See base class."""

        SQL = "SELECT summary_id FROM jizt.summary WHERE summary_id = %s;"

        conn = None

        try:
            conn = self._connect()
            with conn.cursor() as cur:
                cur.execute(SQL, (id_,))
                return cur.fetchone() is not None
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)
        finally:
            if conn is not None:
                conn.close()

    def _connect(self):
        """Connect to the PostgreSQL database.

        Returns:
            :obj:`psycopg2.extensions.connection`: The connection
            to the PostgreSQL database.
        """

        try:
            return psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.error(error)
