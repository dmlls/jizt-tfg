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

"""Tokenization utilities."""

__version__ = '0.2'

from nltk.tokenize import RegexpTokenizer
from blingfire import text_to_sentences
from typing import List, Optional


def sentence_tokenize(text: str,
                      tokenizer: Optional[RegexpTokenizer] = None
) -> List[str]:
    r"""Divide the text into sentences.

    The steps followed are:

        * Remove characters such as '\n', '\t', etc.
        * Splits the text into sentences, taking into account Named Entities and
        special cases such as:

            - "I was born in 02.26.1980 in New York", "As we can see in Figure 1.1.
            the model will not fail.": despite the periods in the date and the
            Figure number, these texts will not be split into different sentences.
            - "Mr. Elster looked worried.", "London, capital of U.K., is famous
            for its red telephone boxes": the pre-processor applies Named Entity
            Recognition and does not split the previous sentences.
            - "Hello.Goodbye.", "Seriously??!That can't be true.": these sentences
            are split into: ['Hello.', 'Goodbye.'] and ['Seriously??!', 'That can't
            be true.'], respectively.

    Args:
        text (:obj:`str`):
            Text to be split in sentences.
        tokenizer (:obj:`nlkt.tokenize.RegexpTokenizer`, `optional`, defaults to :obj:`None`):
            Regular expression to carry out a preliminar split (the text will be
            afterwards split once again by the :mod:`blingfire` :func:`text_to_sentences`.
            function).
    """

    # punctuation that shouldn't be preceeded by a whitespace
    PUNCT_NO_PREV_WHITESPACE = ".,;:!?"

    if tokenizer is None:
        # if next letter after period is lowercase, consider it part of the same sentence
        # ex: "As we can see in Figure 1.1. the sentence will not be split."
        # Also, take acronyms as groups, e.g., U.K., U.S., B.C., D.C., etc.
        tokenizer = RegexpTokenizer(r'[^.!?]+(?:(?:[A-Z][.])+|[.!?]+)+[^A-Z]*')

    # if there's no final period, add it (this makes the assumption that the last
    # sentence is not interrogative or exclamative, i.e., ends with '?' or '!')
    if text[-1] != '.' and text[-1] != '?' and text[-1] != '!':
        text += '.'

    text = ' '.join(text.split())  # remove '\n', '\t', etc.

    # split sentences with the regexp and ensure there's 1 whitespace at most
    sentences = ' '.join(tokenizer.tokenize(text)).replace('  ', ' ')

    # remove whitespaces before PUNCT_WITHOUT_PREV_WHITESPACE
    for punct in PUNCT_NO_PREV_WHITESPACE:
        sentences = sentences.replace(' ' + punct, punct)

    sentences = text_to_sentences(sentences).split('\n')

    final_sentences = [sentences[0]]

    for sent in sentences[1:]:
        # if the previous sentence doesn't end with a '.', '!' or '?'
        # we concatenate the current sentence to it
        if (final_sentences[-1][-1] != '.' and
                final_sentences[-1][-1] != '!' and
                final_sentences[-1][-1] != '?'):
            final_sentences[-1] += (' ' + sent)
        # if the next sentence doesn't start with a letter or a number,
        # we concatenate it to the previous
        elif not sent[0].isalpha() and not sent[0].isdigit():
            final_sentences[-1] += sent
        else:
            final_sentences.append(sent)

    return final_sentences
