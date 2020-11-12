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

__version__ = '0.1'

from utils.tokenization import sentence_tokenize
from typing import List, Optional, Union

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
    
    def preprocess(
        self,
        text: str,
        return_as_list: Optional[bool] = False
    ) -> Union[str, List[str]]:
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
        sentences = sentence_tokenize(text)
        return sentences if return_as_list else ' '.join(sentences)