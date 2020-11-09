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

"""Text preprocessor class."""

from nltk.tokenize import RegexpTokenizer
from nltk import sent_tokenize
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple, Union

class TextPreprocessor:
    """Text preprocessing utilities.
    
    This preprocessor carries out the following preprocessing tasks over
    the texts:
    - Removes characters such as '\n', '\t', etc.
    - Adds one whitespace after each sentence (relevant for the BART model).
    - Splits the text into sentences, taking into account Named Entities and
      special cases such as:
      + "I was born in 02.26.1980 in New York", "As we can see in Figure 1.1.
        the model will not fail.": despite the periods in the date and the
        Figure number, these texts will not be split into different sentences.
      + "Mr. Elster looked worried.", "London, capital of U.K., is famous
        for its red telephone boxes": the preprocessor applies Named Entity
        Recognition and does not split the previous sentences.
      + "Hello.Goodbye.", "Seriously??!That can't be true.": these sentences
        are split into: ['Hello.', 'Goodbye.'] and ['Seriously??!', 'That can't
        be true.'], respectively.
     
    """
    
    def __init__(self):
        # if next letter after period is lowercase, consider it part of the same sentence
        # ex: "As we can see in Figure 1.1. the sentence will not be split."
        self._tokenizer = RegexpTokenizer(r'[^.!?]+[.!?]+[^A-Z]*')
        self._punctuation = ".,;:!?" # punctuation that shouldn't have a whitespace before
    
    def preprocess(
        self,
        text: str,
        return_as_list: Optional[bool] = False
    ) -> Union[List[str], str]:
        """Preprocess the text.
        
        Args:
            text:
                Text to be preprocessed.
            return_as_list:
                If True the text is split into sentences and the method returns
                a list containing those sentences. If False, it returns the text
                preprocessed as a single string.
                
        Returns:
            Either a list containing the sentences of the preprocessed text, or
            the preprocessed text as a single string.
        """
        
        if text[-1] != '.': # if there's not final period, add it so the regex matches the last sentence
            text += '.'
            
        text = ' '.join(text.split()) # remove '\n', '\t', etc.
        
        # split sentences with self._tokenizer and ensure there's 1 whitespace at most
        sentences = ' '.join(self._tokenizer.tokenize(text))
        
        # remove whitespaces before self._punctuation
        for punct in self._punctuation:
            sentences = sentences.replace(' ' + punct, punct)

        sentences = sent_tokenize(sentences)

        final_sentences = [sentences[0]]

        for sent in sentences[1:]:
            # if the previous sentence doesn't end with a '.', '!' or '?'
            # we concatenate the current sentence to it
            if final_sentences[-1][-1] != '.' and \
                final_sentences[-1][-1] != '!' and \
                final_sentences[-1][-1] != '?':
                final_sentences[-1] += (' ' + sent)
            # if the next sentence doesn't start with a letter or a number,
            # we concatenate it to the previous
            elif not sent[0].isalpha() and not sent[0].isdigit():
                final_sentences[-1] += sent
            else:
                final_sentences.append(sent)

        return final_sentences if return_as_list else ' '.join(final_sentences)