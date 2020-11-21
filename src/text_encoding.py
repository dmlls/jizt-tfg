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

"""Text encoding class with support for Hugging Face pretrained models."""

__version__ = '0.1'

import logging
import torch
import copy
from text_preprocessing import TextPreprocessor
from transformers import BartTokenizer
from transformers import T5Tokenizer
from utils.supported_models import SupportedModel, SupportedModelFamily
from nltk import word_tokenize
from transformers import tokenization_utils_base
from typing import List, Optional, Union

# deactivate warnings from the tokenizers
logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

# Ratio calculated thus: len(word_tokenize(text)) / len(t5_tokenizer.encode(text))
# It shows the relation between the tokens without being encoded and the tokens
# once encoded. The higher it is, the most likely the subdivisions will exceed the
# model maximum sequence length.
RATIO_TOKENS_TO_T5_ENCODED_TOKENS = 0.7 # obtained empirically

# Ratio calculated thus: len(word_tokenize(text)) / len(bart_tokenizer.encode(text))
# It shows the relation between the tokens without being encoded and the tokens
# once encoded. The higher it is, the most likely the subdivisions will exceed the
# model maximum sequence length.
RATIO_TOKENS_TO_BART_ENCODED_TOKENS = 0.86 # obtained empirically

# Factor of variation for the RATIO_TOKENS_TO_ENCODED_TOKENS. The new ratio is
# calculated thus:
# RATIO_TOKENS_TO_ENCODED_TOKENS -= RATIO_TOKENS_TO_ENCODED_TOKENS * VARIATION_RATE_FOR_RATIO
VARIATION_RATE_FOR_RATIO = 0.015

class SplitterEncoder:
    """Encoder with splitting.
    
    This text encoder splits the input text to adapt it to the maximum input length
    of a specific model. The split is done in a balanced way so that each set contains
    roughly the same number of tokens, without splitting sentences.
    
    This summarizer is meant to be used along with the following
    `Hugging Face pretrained models <https://huggingface.co/transformers/pretrained_models.html>`__:

    * ``facebook/bart-*``
    * ``t5-*``

    See the
    `Hugging Face docs <https://huggingface.co/transformers/internal/tokenization_utils.html#transformers.tokenization_utils_base.PreTrainedTokenizerBasee>`__
    for further information on tokenization.
    """

    def __init__(self, tokenizer: str = None):
        tokenizer = SupportedModel(tokenizer.lower()) # checks if the tokenizer is supported

        if SupportedModelFamily.BART.value in tokenizer.value: # BART tokenizer
            self._tokenizer = BartTokenizer.from_pretrained(tokenizer.value)
        elif SupportedModelFamily.T5.value in tokenizer.value: # T5 tokenizer
            self._tokenizer = T5Tokenizer.from_pretrained(tokenizer.value)
        # elif future supported models

    @property
    def tokenizer(self):
        return self._tokenizer
    
    def encode(
        self,
        text: str,
        prefix: Optional[str] = None,
        truncation: Optional[Union[bool, str, tokenization_utils_base.TruncationStrategy]] = False,
        max_length: Optional[int] = None,
        return_tensors: Optional[str] = None
    ) -> Union[List[int], torch.LongTensor]:
        """Converts a string to a sequence of ids (:obj:`int`), using the tokenizer and vocabulary.
        
        To avoid going over the maximum sequence length of the tokenizer, the text is first
        split (without splitting sentences) into groups containing approximately the same
        number of tokens.
        
        The division is carried out naively and ``a piori`` (i.e., without actually encoding the
        text), so it could happen that one or more of the divisions generated exceeds the model
        maximum sequence length. In that case, the division is done again with a smaller subdivision
        length. The process is repeated until none of the divisions exceeds the model max. length.
        
        Args:
            text (:obj:`str`):
                The text to be tokenized.
            prefix (:obj:`str`, `optional`, defaults to :obj:`None`):
                String to be added at the beginning of each subdivision.
            truncation (:obj:`bool`, :obj:`str` or :class:`~transformers.tokenization_utils_base.TruncationStrategy`, `optional`,
            defaults to :obj:`False`):
                Activates and controls truncation. Accepts the following values:

                * :obj:`True` or :obj:`'longest_first'`: Truncate to a maximum length specified with the argument
                  :obj:`max_length` or to the maximum acceptable input length for the model if that argument is not
                  provided. This will truncate token by token, removing a token from the longest sequence in the pair
                  if a pair of sequences (or a batch of pairs) is provided.
                * :obj:`'only_first'`: Truncate to a maximum length specified with the argument :obj:`max_length` or to
                  the maximum acceptable input length for the model if that argument is not provided. This will only
                  truncate the first sequence of a pair if a pair of sequences (or a batch of pairs) is provided.
                * :obj:`'only_second'`: Truncate to a maximum length specified with the argument :obj:`max_length` or
                  to the maximum acceptable input length for the model if that argument is not provided. This will only
                  truncate the second sequence of a pair if a pair of sequences (or a batch of pairs) is provided.
                * :obj:`False` or :obj:`'do_not_truncate'` (default): No truncation (i.e., can output batch with
                  sequence lengths greater than the model maximum admissible input size).
            max_length (:obj:`int`, `optional`):
                Controls the maximum length to use by one of the truncation/padding parameters.

                If left unset or set to :obj:`None`, this will use the predefined model maximum length if a maximum
                length is required by one of the truncation/padding parameters. If the model has no specific maximum
                input length, truncation to a maximum length will be deactivated.
            return_tensors (:obj:`str` or :class:`~transformers.tokenization_utils_base.TensorType`, `optional`):
                If set, will return tensors instead of list of python integers. Acceptable values are:

                * :obj:`'pt'`: Return PyTorch :obj:`torch.Tensor` objects.

                .. note::
                    TensorFlow :obj:`tf.constant` and Numpy :obj:`np.ndarray` objects are not yet supported.
        
        Returns:
            :obj:`List[int]` or :obj:`torch.Tensor`: The tokenized ids of the text, split into groups, i.e.::

                [[ids_first_subdivision],
                [ids_second_subdivision],
                [ids_third_subdivision],
                ...]

        See the
        `Hugging Face docs <https://huggingface.co/transformers/_modules/transformers/tokenization_utils_base.html#PreTrainedTokenizerBase.encode>`__
        for further information.
        """
        
        if return_tensors is not None and return_tensors not in ('pt', 'np'):
            raise NotImplementedError(f'{return_tensors} tensors are currently not supported.')  
        
        textPreprocessor = TextPreprocessor()
        
        max_len_subdiv = self._get_max_length_subdivision() # max length per subdivision
        sentences = textPreprocessor.preprocess(text, return_as_list=True)
        
        while True: # do while
            subdivisions = self._divide_eagerly(sentences, max_len_subdiv)

            balanced_subdiv = self._balance_subdivisions(subdivisions, max_len_subdiv)

            # transform subdivs. from, e.g., [["sent_1", "sent_2", ...], [sent_1, sent_2, ...], ...]
            # to ["sent_1 sent_2 ...", "sent_1 sent_2 ...", ...]
            subdivs_as_str = [' '.join(subdiv) for subdiv in balanced_subdiv]
            
            if prefix is not None:
                subdivs_as_str = self._add_prefix_to_subdivs(subdivs_as_str, prefix)
                                
            encoded_subdivs = [self._tokenizer.encode(subdiv,
                                                      truncation=truncation,
                                                      max_length=max_length,
                                                      return_tensors=return_tensors
                                                      ) for subdiv in subdivs_as_str]
            
            if self._check_len_subdivs(encoded_subdivs, return_tensors):
                # all the subdivisions length is <= model max. length
                return encoded_subdivs
            
            # adjust length of subdivisions and start over
            max_len_subdiv -= max_len_subdiv * VARIATION_RATE_FOR_RATIO
        
    @classmethod
    def _divide_eagerly(cls, sentences: List[str], max_len_subdiv: int) -> List[List[str]]:
        """Subdivides the text eagerly.
        
        The sentences are divided into groups, ensuring that the length of any of these
        groups (subdivisions) is always less or equal than the model max. sequence length,
        without splitting sentences.
        
        Args:
            sentences (:obj:`List[str]`):
                The sentences to be split into subdivisions, e.g.,
                :code:`["sent_1", "sent_2", "sent_3", ...]`.
            max_len_subdiv (:obj: `int`):
                Maximum length each subdivision must have, measured in terms of NLTK word
                tokens (:func:`word_tokenize`).
                
        Returns:
            :obj:`List[List[str]]`: The generated subdivisions, e.g.::

            [[sent_1, sent_2, sent_3, ...], [sent_10, sent_11, ...], ...].       
        """
        
        subdivisions = []
        current_subdiv = []
        current_subdiv_len = 0 # in terms of tokens
        
        for sent in sentences:
            sent_len = cls._len(sent)
            if current_subdiv_len + sent_len <= max_len_subdiv:
                current_subdiv.append(sent) # append sent
                current_subdiv_len += sent_len
            else:
                subdivisions.append(current_subdiv)
                current_subdiv = [sent] # new subdivision
                current_subdiv_len = sent_len
        subdivisions.append(current_subdiv) # append last subdivision
        
        return subdivisions

    @classmethod 
    def _balance_subdivisions(cls, subdivisions: List[str], max_len_subdiv: int) -> List[List[str]]:
        """Balances the subdivisions in terms of length.
        
        This method is meant to be called after :meth:`_divide_eagerly`. If needed,
        it moves sentences from one subdivision to another in such way that all the subdvisions
        have the same length, approximately, and keeping the model max. length restriction.
        
        Args:
            subdivisions (:obj:`List[List[str]]`):
                The subdivisions to be balanced, e.g.::

                [[sent_1, sent_2, sent_3, ...], [sent_10, sent_11, ...], ...].
        
        Returns:
            :obj:`List[List[str]]`: The balanced subdivisions.
        """
        
        balanced_subdiv = copy.deepcopy(subdivisions)[::-1]
        # length (in terms of nltk word tokens) of each subdivision, e.g., [501, 498, 480, ...]
        len_prev_subdivs = [cls._len_subdivision(subdiv) for subdiv in balanced_subdiv]
        
        while True: # do while
            for i in range(len(balanced_subdiv) - 1):
                # difference in lengths
                diff_len = cls._len_subdivision(balanced_subdiv[i+1]) - \
                                cls._len_subdivision(balanced_subdiv[i])
                while diff_len > 0:
                    moved_sent_len = cls._len(balanced_subdiv[i+1][-1])
                    # check that moving the sentence doesn't result in a subdivision with
                    # n_tokens > max_len_subdiv and that the length of the moved sentence
                    # is not bigger that the difference of tokens between the subdivs
                    if cls._len_subdivision(balanced_subdiv[i]) + \
                            moved_sent_len <= max_len_subdiv and moved_sent_len <= diff_len:
                        # move sentece from balanced_subdiv[i+1] to balanced_subdiv[i]
                        balanced_subdiv[i].insert(0, balanced_subdiv[i+1][-1]) # add sent
                        balanced_subdiv[i+1] = balanced_subdiv[i+1][:-1] # remove sent
                        diff_len = cls._len_subdivision(balanced_subdiv[i+1]) - \
                                        cls._len_subdivision(balanced_subdiv[i])
                    else:
                        break
                        
            len_current_subdivs = [cls._len_subdivision(subdiv) for subdiv in balanced_subdiv]
            
            if len_prev_subdivs == len_current_subdivs: # if there are no changes, we stop
                return balanced_subdiv[::-1]
            
            len_prev_subdivs = len_current_subdivs
        
    @classmethod
    def _add_prefix_to_subdivs(cls, subdivisions_as_str: List[str], prefix: str) -> List[str]:
        """Adds a prefix to each subdivision.
        
        Args:
            subdivisions_as_str (:obj:`List[str]`):
                The strings to which the prefix will be added. Each string is considered a
                subdivision.
            prefix (:obj:`str`):
                The prefix to insert at the beginning of each subdivision.
        
        Returns:
            :obj:`List[str]`: The subdivisions with the added prefix.
        """

        return [prefix + subdiv for subdiv in subdivisions_as_str]

    def _get_max_length_subdivision(self) -> int:
        """Calculates the maximum length of each subdivision.

        The length is measured in terms of NLTK word tokens (:func:`word_tokenize`).

        Returns:
            :obj:`int`: The calculated maximum length each subdivision should have.
        """

        if SupportedModelFamily.BART.value in type(self._tokenizer).__name__.lower():
            return self._tokenizer.model_max_length * RATIO_TOKENS_TO_BART_ENCODED_TOKENS
        elif SupportedModelFamily.T5.value in type(self._tokenizer).__name__.lower():
            return self._tokenizer.model_max_length * RATIO_TOKENS_TO_T5_ENCODED_TOKENS
        # elif <future supported models>
             
    @classmethod
    def _len(cls, text: str) -> int:
        """Length of a text in terms of NLTK word tokens (:func:`word_tokenize`).

        Args:
            text (:obj:`str`):
                The text whose length will be calculated.
        
        Returns:
            :obj:`int`: The length of the text in terms of NLTK word tokens.
        """

        return len(word_tokenize(text))
    
    @classmethod
    def _len_subdivision(cls, subdivision: List[str]) -> List[int]:
        """Calculates the length of a subdivision.
        
        The length is measured in terms of NLTK word tokens (:func:`word_tokenize`).
        
        Args:
            subdivision (:obj:`List[str]`):
                The subdivision (i.e., :code:`["sent_1", "sent_2", "sent_3", ...]`)
                whose length will be calculated.
                 
        Returns:
            :obj:`int`: The length of the subdivision.
        """

        return cls._len(' '.join(subdivision))

    def _check_len_subdivs(self,
                           subdivisions: List[Union[List[int], torch.LongTensor]],
                           return_tensors: Optional[str] = None
    ) -> bool:
        """Checks the length of subdivisions.
        
        Args:
            subdivisions (:obj:`List[List[int]]` or :obj:`List[torch.LongTensor]`):
                The encoded tokens grouped in subdivisions, either as a :obj:`List`
                (e.g., :code:`[[43, 54, 23, ...], [32, 46, 76, ...], ...]`),
                or as :obj:`totch.LongTensor`
                (e.g., :code:`[tensor([[43, 54, 23, ...]]), tensor([[32, 46, 76]]), ...]`).
            return_tensors (:obj:`str` or :class:`~transformers.tokenization_utils_base.TensorType`, `optional`):
                If set, will return tensors instead of a list of python integers.
                Acceptable values are:
                    - 'pt': Return PyTorch `torch.Tensor` objects.

                .. note:
                    TensorFlow :obj:`tf.constant` and Numpy :obj:`np.ndarray` objects are not yet supported.
                
        Returns:
            (:obj:`bool`): False if any of the subdivisions has a length greater than the tokenzier
            maximum sequence length. True otherwise.
        """

        if return_tensors is None:
            return all(len(subdiv) <= self._tokenizer.model_max_length for subdiv in subdivisions)
        elif return_tensors == 'pt':
            return all(len(subdiv[0]) <= self._tokenizer.model_max_length for subdiv in subdivisions)
        # elif <future supported tensors>