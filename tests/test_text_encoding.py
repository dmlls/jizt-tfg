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

"""Text pre-processing tests."""

import pytest
import text_preprocessing as tp
import text_encoding as te
import torch
import copy
from typing import List, Optional, Union

@pytest.fixture(scope="module")
def initialize_bart():
    from transformers import BartTokenizer
    bart_tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
    bart_splitter = te.SplitterEncoder('facebook/bart-base')
    return bart_tokenizer, bart_splitter

@pytest.fixture(scope="module")
def initialize_t5():
    from transformers import T5Tokenizer
    t5_tokenizer = T5Tokenizer.from_pretrained('t5-base')
    t5_splitter = te.SplitterEncoder('t5-base')
    return t5_tokenizer, t5_splitter

@pytest.fixture(scope="module")
def word_tokenize():
    from nltk import word_tokenize
    return  word_tokenize

sentences = ["The fish dreamed of escaping the fishbowl and into the toilet " + 
             "where he saw his friend go.", # 18 words (NLTK word_tokenize)
             "Today I dressed my unicorn in preparation for the race.", # 11 words
             "The efficiency we have at removing trash has made creating " +
             "trash more acceptable.", # 14 words
             "The near-death experience brought new ideas to light.", # 9 words
             "The sky is clear; the stars are twinkling.", # 10 words
             "Joyce enjoyed eating pancakes with ketchup.", # 7 words
             "Her life in the confines of the house " +
             "became her new normal.", # 13 words
             "They say that dogs are man's best friend, but this cat was " +
             "setting out to sabotage that theory.", # 21 words
             "I’m a living furnace.", # 7 words
             "How do you best like your ice-cream?", # 8 words
             "What's the most interesting conversation " +
             "you eavesdropped on?", # 10 words
             "How would you spend $1,000 to give the most happiness to the " +
             "most number of people possible?", # 19 words
             "What part of your body currently doesn't feel 100%?", # 12 words
             "What's something you believe you'll never be " +
             "able to do well?", # 14 words
             "What's most important to you about your " +
             "school/work environment?", # 11 words
             "Arguing with a fool proves there are two.", # 9 words
             "A witty saying proves nothing.", # 6 words
             "If you tell the truth, you don’t have to remember anything.", # 15 words
             "Only the wisest and stupidest of men never change.", # 10 words
             "Never miss a good chance to shut up.", # 9 words
             "Dreams don’t work unless you do.", # 9 words
             "The only way to have a friend is to be one.", # 12 words
             "I don’t miss her; I miss who I thought she was.", # 15 words
             "Quotation is a serviceable substitute for wit.", # 8 words
             "Tact: the ability to describe others as they see themselves.", # 12 words
             "The small amount of foolery wise men have makes a great show.", # 13 words
             "Age is of no importance unless you’re a cheese.", # 12 words
             "I used to think I was indecisive, but now I’m not so sure.", # 17 words
             "Always remember that you are unique - just like everybody else.", # 12 words
             "Bad decisions make good stories.", # 6 words
             "I cannot afford to waste my time making money.", # 11 words
             "One of the keys to happiness is a bad memory."] # 11 words

# sentences divided eagerly with a max length of 25 NLTK word tokens
divided_sents = [["The fish dreamed of escaping the fishbowl and into the toilet " + 
                  "where he saw his friend go."], # 18 words]
                 ["Today I dressed my unicorn in preparation for the race.",
                  "The efficiency we have at removing trash has made creating " +
                  "trash more acceptable."], # 11 + 14 = 25 words
                 ["The near-death experience brought new ideas to light.",
                  "The sky is clear; the stars are twinkling."], # 9 + 10 = 19 words
                 ["Joyce enjoyed eating pancakes with ketchup.",
                  "Her life in the confines of the house " +
                  "became her new normal."], # 7 + 13 = 20 words
                 ["They say that dogs are man's best friend, but this cat was " +
                  "setting out to sabotage that theory."], # 21 words
                 ["I’m a living furnace.",
                  "How do you best like your ice-cream?",
                  "What's the most interesting conversation " +
                  "you eavesdropped on?"], # 7 + 8 + 10 = 25 words
                 ["How would you spend $1,000 to give the most happiness to the " +
                  "most number of people possible?"], # 19 words
                 ["What part of your body currently doesn't feel 100%?"], # 12 words
                 ["What's something you believe you'll never be " +
                  "able to do well?",
                  "What's most important to you about your " +
                  "school/work environment?"], # 14 + 11 = 25 words
                 ["Arguing with a fool proves there are two.",
                  "A witty saying proves nothing."], # 9 + 6 = 15 words
                 ["If you tell the truth, you don’t have to remember anything.",
                  "Only the wisest and stupidest of men never change."], # 15 + 10 = 25 words
                 ["Never miss a good chance to shut up.",
                  "Dreams don’t work unless you do."], # 9 + 9 = 18 words
                 ["The only way to have a friend is to be one."], # 12 words
                 ["I don’t miss her; I miss who I thought she was.", 
                  "Quotation is a serviceable substitute for wit."], # 15 + 8  = 23 words
                 ["Tact: the ability to describe others as they see themselves.",
                  "The small amount of foolery wise men have " + \
                  "makes a great show."], # 12 + 13 = 25 words
                 ["Age is of no importance unless you’re a cheese."], # 12 words
                 ["I used to think I was indecisive, but now I’m not so sure."], # 17 words
                 ["Always remember that you are unique - just like everybody else.",
                  "Bad decisions make good stories."], # 12 + 6 = 18 words
                 ["I cannot afford to waste my time making money.",
                  "One of the keys to happiness is a bad memory."]] # 11 + 11 = 22 words

def test_check_len_subdivs(initialize_bart, initialize_t5):
    bart_tokenizer, bart_splitter = initialize_bart
    t5_tokenizer, t5_splitter = initialize_t5
    _check_len_subdivs(bart_tokenizer, bart_splitter)
    _check_len_subdivs(t5_tokenizer, t5_splitter)

def _check_len_subdivs(tokenizer, splitter):
    encodings_short = tokenizer.encode(" ".join(sentences))
    encodings_past_max_len = tokenizer.encode(" ".join(sentences*3))
    assert splitter._check_len_subdivs([encodings_short])
    assert not splitter._check_len_subdivs([encodings_past_max_len])
    encodings_short_pt = tokenizer.encode(" ".join(sentences),
                                          return_tensors='pt')
    encodings_past_max_len_pt = tokenizer.encode(" ".join(sentences*3),
                                                 return_tensors='pt')
    assert splitter._check_len_subdivs([encodings_short_pt],
                                       return_tensors='pt')
    assert not splitter._check_len_subdivs([encodings_past_max_len_pt],
                                           return_tensors='pt')

def test_len_subdivision(word_tokenize):
    len_sentences = len(word_tokenize(" ".join(sentences)))
    assert te.SplitterEncoder._len_subdivision(sentences) == len_sentences

def test_len(word_tokenize):
    text = " ".join(sentences)
    assert len(word_tokenize(text)) == te.SplitterEncoder._len(text)

def test_get_max_length_subdivision(initialize_bart, initialize_t5):
    bart_tokenizer, bart_splitter = initialize_bart
    t5_tokenizer, t5_splitter = initialize_t5
    _get_max_length_subdivision(bart_tokenizer, bart_splitter,
                                te.RATIO_TOKENS_TO_BART_ENCODED_TOKENS)
    _get_max_length_subdivision(t5_tokenizer, t5_splitter,
                                te.RATIO_TOKENS_TO_T5_ENCODED_TOKENS)

def _get_max_length_subdivision(tokenizer, splitter, ratio):
    max_len_subdiv = tokenizer.model_max_length * ratio
    assert max_len_subdiv == splitter._get_max_length_subdivision()

def test_add_prefix_to_subdivs():
    prefixes = ["summarize: ", "translate: ", "answer: "]
    for pref in prefixes:
        assert [pref + sent for sent in sentences] == \
            te.SplitterEncoder._add_prefix_to_subdivs(sentences, pref)

def test_balance_subdivisions():
    subdivs = [["word"]*5]*9
    # Nothing to balance
    assert subdivs == te.SplitterEncoder._balance_subdivisions(subdivs, 5)
    #####################
    subdivs = [["word"]*5]
    # Only one subdivision
    assert subdivs == te.SplitterEncoder._balance_subdivisions(subdivs, 5)
    #####################
    subdivs = []
    for i in range(9, 0, -1):
        subdivs.append(["word"]*i) # total 45 "words" divided in 9 subdivisions
    # there should be 9 subdivisions of 5 elements each
    assert [["word"]*5]*9 == te.SplitterEncoder._balance_subdivisions(subdivs, 5)
    #####################
    subdivs = [["This sentence contains exactly seven tokens.",
                "Short sentence."], # 7 + 3 = 10 words (NLTK word_tokenize)
               ["This contains four.", "And this has six tokens."], # 4 + 6 = 10 words
               ["This is short.", "And this not too long."], # 4 + 6 = 10 words
               ["Too short."]] # 3 words

    balanced_subdivs = [["This sentence contains exactly seven tokens."],  # 7 words
                        ["Short sentence.", "This contains four."], # 3 + 4 = 7 words
                        ["And this has six tokens.", "This is short."], # 6 + 4 = 7 words 
                        ["And this not too long.", "Too short."]] # 6 + 3 = 9 words

    assert balanced_subdivs == te.SplitterEncoder._balance_subdivisions(subdivs, 10)
    #####################
    # check that the sentences passed to the function remain intact
    subdivs_before = copy.deepcopy(divided_sents)
    balanced_subdivs = te.SplitterEncoder._balance_subdivisions(divided_sents, 25)
    assert subdivs_before == divided_sents 

def test_divide_eagerly():
    assert [["word"]*5]*9 == te.SplitterEncoder._divide_eagerly(["word"]*5*9, 5)
    #####################
    print(divided_sents)
    max_len_subdiv = 25
    assert divided_sents == te.SplitterEncoder._divide_eagerly(sentences, max_len_subdiv)

def test_encode(initialize_bart, initialize_t5):
    bart_tokenizer, bart_splitter = initialize_bart
    t5_tokenizer, t5_splitter = initialize_t5
    _encode(bart_tokenizer, bart_splitter)
    _encode(t5_tokenizer, t5_splitter)

def _encode(tokenizer, splitter):
    text = " ".join(sentences*10)
    preprocessed_text = tp.TextPreprocessor.preprocess(text, return_as_list=True)

    encoded_sents = splitter.encode(text)

    # no tensors
    max_len = splitter._get_max_length_subdivision()
    divided = te.SplitterEncoder._divide_eagerly(preprocessed_text, max_len)
    balanced = te.SplitterEncoder._balance_subdivisions(divided, max_len)
    expected = [' '.join(exp) for exp in balanced]
    expected_enc_sents = [tokenizer.encode(expect) for expect in expected]
    assert expected_enc_sents == encoded_sents

    # Pytorch tensors
    encoded_sents = splitter.encode(text, return_tensors='pt')
    expected_enc_sents = [tokenizer.encode(expect, return_tensors='pt') for expect in expected]
    for encoded, expect in zip(encoded_sents, expected_enc_sents):
        assert torch.all(encoded.eq(expect))

    # Exception
    with pytest.raises(NotImplementedError):
        splitter.encode('', return_tensors='xd')

def test_init(initialize_bart, initialize_t5):
    bart_tokenizer, _ = initialize_bart
    t5_tokenizer, _ = initialize_t5
    _init(bart_tokenizer, 'facebook/bart-base') 
    _init(t5_tokenizer, 't5-base') 

    with pytest.raises(ValueError):
        te.SplitterEncoder("not-supported-model")

def _init(tokenizer, model_name):
    splitter = te.SplitterEncoder(model_name)
    assert type(splitter.tokenizer) == type(tokenizer)
