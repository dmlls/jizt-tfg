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

"""Text post-processor class."""

__version__ = '0.1'

from truecase import get_true_case
from utils.tokenization import sentence_tokenize


class TextPostprocessor:
    """Text post-processing utilities.

    This post-processor carries out the following preprocessing tasks over
    the texts:

    * Formats the text correctly (e.g., removes incorrect whitespaces).
    * Performs truecasing over the text. See `this paper
      <https://www.cs.cmu.edu/~llita/papers/lita.truecasing-acl2003.pdf>`__ for more details.
    """

    @classmethod
    def postprocess(cls, text: str) -> str:
        """Post-processes the text.

        Args:
            text (:obj:`str`):
                The text to be post-processed.

        Returns:
            :obj:`str`: The post-processed text.
        """

        txt = ' '.join(sentence_tokenize(text))
        return get_true_case(txt)
