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

"""Text post-processor class."""

__version__ = '0.1.1'

import logging
from truecase.TrueCaser import TrueCaser
from nltk import sent_tokenize


class TextPostprocessor:
    """Text post-processing utilities.

    This post-processor carries out the following preprocessing tasks over
    the texts:

    * Formats the text correctly (e.g., removes incorrect whitespaces).
    * Performs truecasing over the text. See `this paper
      <https://www.cs.cmu.edu/~llita/papers/lita.truecasing-acl2003.pdf>`__
      for more details.
    """

    def __init__(self):
        self.truecaser = TrueCaser()
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("TextPostprocessor")

    def postprocess(self, text: str) -> str:
        """Post-processes the text.

        Args:
            text (:obj:`str`):
                The text to be post-processed.

        Returns:
            :obj:`str`: The post-processed text.
        """

        if not text:
            return text   # if text is empty just return it

        sentences = sent_tokenize(text)
        truecased_sents = list(map(self.truecaser.get_true_case, sentences))
        return ' '.join(map(self._capitalize_first_letter, truecased_sents))

    def _capitalize_first_letter(self, sent: str) -> str:
        """Capitalize the first letter of a sentence.

        Args:
            sent (:obj:`str`):
                The sentence whose first letter will be capitalized.

        Returns:
            :obj:`str`: The sentence with its first letter capitalized.
        """

        return f"{sent[0].upper()}{sent[1:]}"
