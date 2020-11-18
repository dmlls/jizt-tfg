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

"""List of current supported Hugging Face models."""

__version__ = '0.1'

from enum import Enum

class ExplicitEnum(Enum):
    """
    Enum with more explicit error message for missing values.
    """

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            (f"{value} is not a valid {cls.__name__}, please select one "
             f"of the following: {', '.join([pair.value for pair in cls])}")
        )

class SupportedModel(ExplicitEnum):
    """Supported pretrained models.

    Possible values for the ``tokenizer`` and ``model`` argument in :meth:`text_encoding.SplitterEncoder.encode`,
    and the ``tokenizer`` and ``model`` arguments in :meth:`text_summarization.Summarizer.summarize`. Useful for
    tab-completion in an IDE.

    See the
    `list of Hugging Face pretrained models <https://huggingface.co/transformers/pretrained_models.html>`__:
    for more information.
    """

    BART_BASE = "facebook/bart-base"
    BART_LARGE = "facebook/bart-large"
    BART_LARGE_MNLI = "facebook/bart-large-mnli"
    BART_LARGE_CNN = "facebook/bart-large-cnn"
    T5_SMALL = "t5-small"
    T5_BASE = "t5-base"
    T5_LARGE = "t5-large"
    T5_3B = "t5-3B"
    T5_11B = "t5-11B"

class SupportedModelFamily(ExplicitEnum):
    """Supported model `families`.

    The word `family` refers to the Hugging Face base model of a pretrained model. Currently, the supported model
    families are:

    *`BART <https://huggingface.co/transformers/model_doc/bart.html#>`__
    *`T5 <https://huggingface.co/transformers/model_doc/t5.html>`__
    """

    BART = "bart"
    T5 = "t5"