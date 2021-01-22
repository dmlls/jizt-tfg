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

"""Default params."""

__version__ = '0.1.1'

import os
from distutils import util
from aenum import Enum, NoAlias


def safe_str_to_type(value: str, to_type):
    """Safe conversion from :obj:`str` to a specific type.

    This function takes care of correctly casting :obj:`None` values.

    Args:
        value :obj:`str`:
            The value to convert.
        to_type :obj:`type`:
            The type to convert the value to.

    Returns:
        :obj:`type`: The converted value.
    """

    if to_type is bool:
        return (None if value is None or value.lower() == "none"
                else bool(util.strtobool(value)))
    return None if value is None or value.lower() == "none" else to_type(value)


class DefaultParams(Enum):
    """Default params."""

    _settings_ = NoAlias

    # The max length of the summary will be at most
    # this percentage of the source length
    RELATIVE_MAX_LENGTH = safe_str_to_type(os.environ['RELATIVE_MAX_LENGTH'], float)
    # Same for the min length
    RELATIVE_MIN_LENGTH = safe_str_to_type(os.environ['RELATIVE_MIN_LENGTH'], float)
    DO_SAMPLE = safe_str_to_type(os.environ['DO_SAMPLE'], bool)
    EARLY_STOPPING = safe_str_to_type(os.environ['EARLY_STOPPING'], bool)
    NUM_BEAMS = safe_str_to_type(os.environ['NUM_BEAMS'], int)
    TEMPERATURE = safe_str_to_type(os.environ['TEMPERATURE'], float)
    TOP_K = safe_str_to_type(os.environ['TOP_K'], int)
    TOP_P = safe_str_to_type(os.environ['TOP_P'], float)
    REPETITION_PENALTY = safe_str_to_type(os.environ['REPETITION_PENALTY'], float)
    LENGTH_PENALTY = safe_str_to_type(os.environ['LENGTH_PENALTY'], float)
    NO_REPEAT_NGRAM_SIZE = safe_str_to_type(os.environ['NO_REPEAT_NGRAM_SIZE'], int)
