
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

"""Text post-processing tests."""

import pytest
import text_postprocessing as tp


input_and_expected_texts = [
    (('it started in a movie in the late 1950s where you have a boy '
      'sitting in his own bedroom, trying to study.his wife gives him '
      'presents, and the boy gets up and starts talking about his dream. '
      'they talk about how they want him to leave his parents, and how '
      'they want it.this has been the same thing for most of this, and '
      'i think that it has been for many, many years.and i was born and '
      'raised in a house that was kind of just the typical of what we were '
      'used to. but this time, i was sitting in the living room of that '
      'house and my parents were sitting in the living room and so i was '
      'being led upstairs, i was looking through a closet, and i looked '
      'down it and i saw a big white book with the word "saved" on it, '
      'like, "we\'ve all lived here for a while, we\'ll take the books and '
      'have them back, then we\'ll go back and change out the books and '
      'try to change the \t way we do things for the kids." and the dad was '
      'very surprised.he was actually quite appalled by how little money '
      'he had for his children.so he took his father and walked outside '
      'saying, "we don\'t understand why you\'re so excited about this. '
      'what\'s the best way to move forward for our generation, to change '
      'the whole landscape of how life is for children?" and he looked up '
      'at me and said,     "yes, yes."'),
     ('It started in a movie in the late 1950s where you have a boy '
      'sitting in his own bedroom, trying to study. His wife gives him '
      'presents, and the boy gets up and starts talking about his dream. '
      'They talk about how they want him to leave his parents, and how '
      'they want it. This has been the same thing for most of this, and '
      'I think that it has been for many, many years. And I was born and '
      'raised in a house that was kind of just the typical of what we '
      'were used to. But this time, I was sitting in the living room of '
      'that house and my parents were sitting in the living room and so '
      'I was being led upstairs, I was looking through a closet, and I '
      'looked down it and I saw a big white book with the word "Saved" '
      'On it, like, "We\'ve all lived here for a while, we\'ll take the '
      'books and have them back, then we\'ll go back and change out the '
      'books and try to change the way we do things for the kids." And '
      'the dad was very surprised. He was actually quite appalled by how '
      'little money he had for his children. So he took his father and '
      'walked outside saying, "We dont understand why youre so excited '
      'about this. What\'s the best way to move forward for our generation, '
      'to change the whole landscape of how life is for children?" And '
      'he looked up at me and said, "Yes, yes.\"')),
    (('new jersey had 4 governors in the span of 8 days in early 2002. '
      'The shortest term of those was served by John Farmer jr. for 90 '
      'minutes. The stockholm archipelago has more islands than the '
      'pacific Ocean at around 30,000.The money for the Statue of Liberty '
      'came from fundraising from auctions, a lottery, and boxing matches '
      'in Europe and the U.S.The Statue cost the French about $250,000, '
      'which nowadays would be over $5.5 million dollars.Comets only '
      'reflect 4% of the light that falls on them, the rest is absorbed. '
      'Until 2007, slavery was legal in mauritania. Even still, 1-4% of '
      'the population is still living as slaves. The average american '
      'child is given $3.70 per tooth that falls out. the largest known '
      'prime number has 17,425,170 digits. when shuffling a deck of cards, '
      'the number of possible arrangements is approximately 8×1067. An '
      'adult’s kidney weighs about 5 ounces (142 grams) and is the size of '
      'a fist. justin bieber’s first tweet was at 8:27 pm on May 11, 2009. '
      'alaska is the only state in America that can be typed on one row of '
      'a traditional        English     QWERTY   keyboard.'),
     ('New Jersey had 4 Governors in the span of 8 days in early 2002. '
      'The shortest term of those was served by John Farmer Jr. for 90 '
      'minutes. The Stockholm archipelago has more islands than the '
      'Pacific Ocean at around 30,000. The money for the Statue of Liberty '
      'came from fundraising from auctions, a lottery, and boxing matches '
      'in Europe and the U.S. The Statue cost the French about $250,000, '
      'which nowadays would be over $5.5 million dollars. Comets only '
      'reflect 4% of the light that falls on them, the rest is absorbed. '
      'Until 2007, slavery was legal in Mauritania. Even still, 1-4% of '
      'the population is still living as slaves. The average American '
      'child is given $3.70 per tooth that falls out. The largest known '
      'prime number has 17,425,170 digits. When shuffling a deck of cards, '
      'the number of possible arrangements is approximately 8×1067. An '
      'adult’s kidney weighs about 5 ounces (142 grams) and is the size of '
      'a fist. Justin Bieber’s first tweet was at 8:27 pm on May 11, 2009. '
      'Alaska is the only state in America that can be typed on one row of '
      'a traditional English QWERTY keyboard.')),
    (('had an awful day today :( hope it gets better soon. yesterday, '
      'however, was super nice ^^ can\'t wait to repeat the experience asap'
      'here goes a happy face :-) and a sad one :-(, another happy one =) '
      'and finally a funny one :P'),
     ('Had an awful day today :( hope it gets better soon. Yesterday,'
      'however, was super nice ^^ can\'t wait to repeat the experience asap'
      'here goes a happy face :-) and a sad one :-(, another happy one =) '
      'and finally a funny one :P'))
]


@pytest.mark.parametrize("input_text, expected", input_and_expected_texts)
def test_postprocess(input_text, expected):
    assert tp.TextPostprocessor.postprocess(input_text) == expected
