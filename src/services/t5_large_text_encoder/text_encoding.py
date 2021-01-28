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

"""Text encoding class with support for ``t5-large`` Hugging Face pretrained model."""

__version__ = '0.0.4'

import logging
import torch
import copy
from itertools import chain
from utils.tokenization import sentence_tokenize
from transformers import T5Tokenizer, tokenization_utils_base
from typing import List, Tuple, Optional, Union


class SplitterEncoder:
    """T5-large text encoder with splitting.

    This text encoder splits the input text to adapt it to the maximum input
    length of a specific model. The split is done in a balanced way so that
    each set contains roughly the same number of tokens, without splitting
    sentences.

    This encoder uses the
    `Hugging Face t5-large pretrained model <https://huggingface.co/t5-large>`__.

    See the
    `Hugging Face docs <https://huggingface.co/transformers/internal/tokenization_utils.html#transformers.tokenization_utils_base.PreTrainedTokenizerBasee>`__
    for further information on tokenization.
    """

    def __init__(self, tokenizer_path: str, debug: bool = False):
        self._tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)
        if not debug:
            # deactivate warnings from the tokenizer
            logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

    @property
    def tokenizer(self):
        return self._tokenizer

    def encode(
        self,
        text: str,
        prefix: Optional[str] = 'summarize: ',
        truncation: Optional[Union[bool, str, tokenization_utils_base.TruncationStrategy]] = False,
        max_length: Optional[int] = None,
        return_tensors: Optional[str] = 'pt'
    ) -> Union[List[int], torch.LongTensor]:
        """Transform a string into a sequence of ids (:obj:`int`), using the tokenizer and vocabulary.

        To avoid going over the maximum sequence length of the tokenizer, the text is first
        split (without splitting sentences) into groups containing approximately the same
        number of tokens.

        Args:
            text (:obj:`str`):
                The text to be tokenized.
            prefix (:obj:`str`, `optional`, defaults to 'summarize: '):
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
            return_tensors (:obj:`str` or :class:`~transformers.tokenization_utils_base.TensorType`, `optional`,
                            defaults to 'pt'):
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

        if return_tensors is not None and return_tensors not in ('pt'):
            raise NotImplementedError(f'{return_tensors} '
                                      f'tensors are currently not supported.')

        # If prefix is None, take the empty string
        prefix = "" if prefix is None else prefix

        sentences = sentence_tokenize(text)
        # Tokens of each sentence. We remove the last token (EOS token).
        sent_tks = [self.tokenizer.encode(sent,
                                          return_tensors=return_tensors)[0][:-1]
                    for sent in sentences]
        # Number of tokens of each sentence
        sent2ntks = [len(sent) for sent in sent_tks]
        # Tokens of the prefix
        prefix_tks = self.tokenizer.encode(prefix,
                                           return_tensors=return_tensors)[0][:-1]
        # Number of tokens of the prefix
        ntks_prefix = len(prefix_tks)

        split_points, subdiv2ntks = self._divide_eagerly(sentences,
                                                         sent2ntks,
                                                         ntks_prefix)


        split_points, subdiv2ntks = self._balance_subdivisions(split_points,
                                                               subdiv2ntks,
                                                               sent2ntks)

        encoded_subdivs = [torch.cat(
                               [prefix_tks]
                               + sent_tks[split_points[i]:split_points[i+1]]
                               + [torch.tensor([self.tokenizer.eos_token_id])]
                           ).unsqueeze(0) for i in range(len(split_points) - 1)]

        return encoded_subdivs

    def _divide_eagerly(self,
                        sentences: List[str],
                        sent2ntks: List[int],
                        ntks_prefix: int
    ) -> Tuple[List[int], List[int]]:
        """Subdivide the text eagerly.

        The sentences are divided into groups, ensuring that the
        length of any of these groups (subdivisions) is always less
        or equal than the model max. sequence length, without splitting
        sentences.

        Args:
            sentences (:obj:`List[str]`):
                The sentences to be split into subdivisions, e.g.,
                :code:`["sent_1", "sent_2", "sent_3", ...]`.
            sent2ntks (:obj:`List[int]`):
                The number of encoded tokens corresponding to each of
                the sentences. The indexes match those from :obj:`sentences`,
                so that the tokens corresponding to the first sentence would
                be :ob:`sent2ntks[0]` and so on.
            ntks_prefix (:obj:`int`):
                The number of encoded tokens corresponding to the prefix.

        Returns:
            :obj:`Tuple[List[int], List[int]]`: A tuple containing:
            
                * The points where to split in order to form the subdivisions,
                  e.g. ``[0. 15, 32, 51]`` means that the first subdivision
                  contains ``sentences[0:15]``, the second ``sentences[15:32]``,
                  and the third and last ``[sentences[32:51]``.
                * The number of tokens in each subdivision.
        """

        subdiv2ntks = []
        split_points = [0] 
        subdiv_len = ntks_prefix + sent2ntks[0] + 1
        for i in range(1, len(sentences)):
            subdiv_len += sent2ntks[i]
            if subdiv_len > self.tokenizer.model_max_length:
                split_points.append(i)
                subdiv2ntks.append(subdiv_len - sent2ntks[i])
                subdiv_len = ntks_prefix + sent2ntks[i] + 1
        split_points.append(len(sentences))
        subdiv2ntks.append(subdiv_len)
        return split_points, subdiv2ntks

    def _balance_subdivisions(self,
                              split_points: List[int],
                              subdiv2ntks: List[int],
                              sent2ntks: List[int]
    ) -> Tuple[List[int], List[int]]:
        """Balance the subdivisions in terms of length.

        This method is meant to be called after :meth:`_divide_eagerly`.
        If needed, it moves sentences from one subdivision to another in
        such way that all the subdvisions have the same length, approximately,
        and keeping the model max. length restriction.

        Args:
            split_points (:obj:`List[int]`):
                The points where to split in order to form the subdivisions,
                e.g. ``[0. 15, 32, 51]`` means that the first subdivision
                contains ``sentences[0:15]``, the second ``sentences[15:32]``,
                and the third and last ``[sentences[32:51]``.
            subdiv2ntks (:obj:`List[int]`):
                The number of tokens in each subdivision.
            sent2ntks (:obj:`List[int]`):
                The number of encoded tokens corresponding to each of
                the sentences. The indexes match those from :obj:`sentences`,
                so that the tokens corresponding to the first sentence would
                be :ob:`sent2ntks[0]` and so on.

        Returns:
            :obj:`Tuple[List[int], List[int]]`: A tuple containing:
            
                * The balanced points where to split in order to form the
                  subdivisions, being these of approximately the same length
                  in number of encoded tokens.
                * The number of tokens in each subdivision.
        """

        balanced_split_points = split_points[:]
        balanced_subdiv2ntks = subdiv2ntks[:]

        prev_balanced_split_points = balanced_split_points[:]

        while True:
            for i in range(len(balanced_split_points)-1, 1, -1):
                diff_ntks = balanced_subdiv2ntks[i-2] - balanced_subdiv2ntks[i-1]
                while diff_ntks > 0:
                    moved_sent_ntks = sent2ntks[balanced_split_points[i-1] - 1]
                    if ((balanced_subdiv2ntks[i-1]
                            + moved_sent_ntks <= self.tokenizer.model_max_length) 
                            and moved_sent_ntks <= diff_ntks):
                        balanced_split_points[i-1] -= 1
                        balanced_subdiv2ntks[i-1] += moved_sent_ntks
                        balanced_subdiv2ntks[i-2] -= moved_sent_ntks
                        diff_ntks = balanced_subdiv2ntks[i-2] - balanced_subdiv2ntks[i-1]
                    else:
                        break
            if balanced_split_points == prev_balanced_split_points:
                return balanced_split_points, balanced_subdiv2ntks

            prev_balanced_split_points = balanced_split_points[:]
