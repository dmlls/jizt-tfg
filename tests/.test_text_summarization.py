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

"""Text summarization tests."""

import pytest
import text_summarization as ts


def test_init():
    # try different initializations and check no exceptions are raised
    # correct initializations
    ts.Summarizer("facebook/bart-base")
    ts.Summarizer("facebook/bart-base", "facebook/bart-base")
    ts.Summarizer("t5-base")
    ts.Summarizer("t5-base", "t5-base")

    # incorrect initializations (not supported models)
    with pytest.raises(ValueError):
        ts.Summarizer("not-supported-model")
        ts.Summarizer("not-supported-model", "not-supported-model")
        ts.Summarizer("facebook/bart-base", "not-supported-model")
        ts.Summarizer("not-supported-model", "facebook/bart-base")