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
from utils.tokenization import sentence_tokenize


passing_sentences = [
    ("How's your        day going???!It's     going...\n actually it's going \t bad.",
     ["How's your day going???!", "It's going... actually it's going bad."]),
    ("Hello.Goodbye.",
     ["Hello.", "Goodbye."]),
    ("Mr. Elster looked worried. We didn't know why.",
     ["Mr. Elster looked worried.", "We didn't know why."]),
    ("London, capital of U.K., is quite expensive.",
     ["London, capital of U.K., is quite expensive."]),
    ("I was born in 02.28.1980 in N.Y. It's been quite some time!",
     ["I was born in 02.28.1980 in N.Y.", "It's been quite some time!"]),
    ("She asked \"How's it going?\", and I said \"Great!\"",
     ["She asked \"How's it going?\", and I said \"Great!\""]),
    ("\"Everyone will be famous for 15 minutes.\" - Andy Warhol.",
     ["\"Everyone will be famous for 15 minutes.\" - Andy Warhol."]),
    ("As we can see in Figure 1.1. the model will eventually converge.",
     ["As we can see in Figure 1.1. the model will eventually converge."]),
    ("NLP (i.e. Natural Language Processing) is great!!!No kidding!",
     ["NLP (i.e. Natural Language Processing) is great!!!", "No kidding!"]),
    ("Tomorrow I can't. I work the morning shift, i.e., from 6 am to 1 pm.",
     ["Tomorrow I can't.", "I work the morning shift, i.e., from 6 am to 1 pm."]),
    ("First: grab the ingredients;don't get the salt just yet. Then, preheat oven.",
     ["First: grab the ingredients; don't get the salt just yet.", "Then, preheat oven."]),
    ("I don't like Voldemort,A.K.A.\"he-who-must-not-be-named.\"",
     ["I don't like Voldemort, A.K.A. \"he-who-must-not-be-named.\""]),
    ("Whitespaces ??!Honestly   ,not my thing ; that is , I don't get them !",
     ["Whitespaces??!", "Honesty, not my thing; that is, I don't get them!"])
]

failing_sentences = [
    ("I should be considered two sentences!but I'm not.",
     ["I should be considered two sentences!", "but I'm not."])
]


@pytest.mark.parametrize("input_sentences, expected", passing_sentences)
def test_sentence_tokenize(input_sentences, expected):
    assert sentence_tokenize(input_sentences) == expected


@pytest.mark.xfail(reason="for now, these errors cannot be fixed")
@pytest.mark.parametrize("input_sentences, expected", failing_sentences)
def test_sentence_tokenize_fail(input_sentences, expected):
    assert sentence_tokenize(input_sentences) == expected