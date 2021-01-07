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

"""Summarization class with support for Hugging Face pretrained models."""

__version__ = '0.1.0'

import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from typing import List, Optional, Union, Iterable


class Summarizer:
    """T5-large text summarizer.

    This summarizer uses the :meth:`generate` method from the class
    :class:`transformers.generation_utils.GenerationMixin` to generate
    the summary ids (encodings).

    Then, it uses the :meth:`decode` method from the class :class:`decode`
    from the class
    :class:`transformers.tokenization_utils_base.PreTrainedTokenizerBase`
    to convert the ids into a string.

    For more information, see the
    `Hugging Face docs
    <https://huggingface.co/transformers/model_doc/t5.html#transformers.T5ForConditionalGeneration>`__:
    """

    def __init__(self, tokenizer_path: str, model_path: str):
        self._tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)
        self._model = T5ForConditionalGeneration.from_pretrained(model_path)

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def model(self):
        return self._model

    def summarize(self,
                  input_ids: List[Union[List[int], torch.LongTensor]],
                  max_length: Optional[int] = 300,
                  min_length: Optional[int] = 30,
                  do_sample: Optional[bool] = None,
                  early_stopping: Optional[bool] = None,
                  num_beams: Optional[int] = 4,
                  temperature: Optional[float] = None,
                  top_k: Optional[int] = None,
                  top_p: Optional[float] = None,
                  repetition_penalty: Optional[float] = None,
                  bad_words_ids: Optional[Iterable[int]] = None,
                  length_penalty: Optional[float] = None,
                  no_repeat_ngram_size: Optional[int] = 3,
                  num_return_sequences: Optional[int] = None,
                  use_cache: Optional[bool] = None,
                  skip_special_tokens: Optional[bool] = True,
                  clean_up_tokenization_spaces: Optional[bool] = True
    ) -> str:
        """Generate a summary from the encoded tokens (input_ids).

        Decoding strategies currently supported:

        * Greedy decoding.
        * Multinomial sampling.
        * Beam-search decoding.
        * Beam-search multinomial sampling.

        Most of these parameters are explained in more detail in `this blog post
        <https://huggingface.co/blog/how-to-generate>`__.

        Args:
            input_ids (:obj:`List[List[int]]` or :obj:`List[torch.LongTensor]`):
                The sequence subdivisions used as a prompt for the summary generation.
            max_length (:obj:`int`, `optional`, defaults to 300):
                The maximum length of the sequence to be generated.
            min_length (:obj:`int`, `optional`, defaults to 30):
                The minimum length of the sequence to be generated.
            do_sample (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether or not to use sampling; use greedy decoding otherwise.
            early_stopping (:obj:`bool`, `optional`, defaults to :obj:`False`):
                Whether to stop the beam search when at least ``num_beams`` sentences are
                finished per batch or not.
            num_beams (:obj:`int`, `optional`, defaults to 4):
                Number of beams for beam search. 1 means no beam search.
            temperature (:obj:`float`, `optional`, defaults tp 1.0):
                The value used to module the next token probabilities.
            top_k (:obj:`int`, `optional`, defaults to 50):
                The number of highest probability vocabulary tokens to keep for top-k-filtering.
            top_p (:obj:`float`, `optional`, defaults to 1.0):
                If set to float < 1, only the most probable tokens with probabilities that add up
                to :obj:`top_p` higher are kept for generation.
            repetition_penalty (:obj:`float`, `optional`, defaults to 1.0):
                The parameter for repetition penalty. 1.0 means no penalty. See `this paper
                <https://arxiv.org/pdf/1909.05858.pdf>`__ for more details.
            bad_words_ids(:obj:`List[List[int]]`, `optional`):
                List of token ids that are not allowed to be generated. In order to get the tokens of
                the words should not appear in the generated text, use :obj:`tokenizer(bad_word,
                add_prefix_space=True).input_ids`.
            length_penalty (:obj:`float`, `optional`, defaults to 1.0):
                Exponential penalty to the length. 1.0 means no penalty. Set to values < 1.0 in order
                to encourage the model to generate shorter sequences, to a value > 1.0 in order to
                encourage the model to produce longer sequences.
            no_repeat_ngram_size (:obj:`int`, `optional`, defaults to 3):
                If set to int > 0, all ngrams of that size can only occur once.
            num_return_sequences(:obj:`int`, `optional`, defaults to 1):
                The number of independently computed returned sequences for each element in the batch.
            use_cache: (:obj:`bool`, `optional`, defaults to :obj:`True`):
                Whether or not the model should use the past last key/values attentions (if applicable
                to the model) speed up decoding.
            skip_special_tokens (:obj:`bool`, `optional`, defaults to :obj:`True`):
                Whether or not to remove special tokens in the decoding.
            clean_up_tokenization_spaces (:obj:`bool`, `optional`, defaults to :obj:`True`):
                Whether or not to clean up the tokenization spaces.

        Returns:
            :obj:`str`: The summary generated.
        """

        summary_subdivs = []

        for ids_subdiv in input_ids:
            summary_ids = self._model.generate(input_ids=ids_subdiv,
                                               max_length=max_length,
                                               min_length=min_length,
                                               do_sample=do_sample,
                                               early_stopping=early_stopping,
                                               num_beams=num_beams,
                                               temperature=temperature,
                                               top_k=top_k,
                                               top_p=top_p,
                                               repetition_penalty=repetition_penalty,
                                               bad_words_ids=bad_words_ids,
                                               length_penalty=length_penalty,
                                               no_repeat_ngram_size=no_repeat_ngram_size,
                                               num_return_sequences=num_return_sequences,
                                               use_cache=use_cache)
            decoded_subdiv = self._tokenizer.decode(summary_ids.squeeze().tolist(),
                                                    skip_special_tokens=skip_special_tokens,
                                                    clean_up_tokenization_spaces=clean_up_tokenization_spaces)
            summary_subdivs.append(decoded_subdiv)

        return " ".join(summary_subdivs)
