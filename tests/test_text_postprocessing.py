
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

import sys
from os.path import abspath, dirname, join

src_path = abspath(join(dirname(dirname(__file__)),
                   "src/services/text_postprocessor"))
sys.path.insert(1, src_path)

import pytest
from text_postprocessor import text_postprocessing as tp


input_and_expected_texts = [
    (('it started in a movie in the late 1950s where you have a boy '
      'sitting in his own bedroom, trying to study. his wife gives him '
      'presents, and the boy gets up and starts talking about his dream. '
      'they talk about how they want him to leave his parents, and how '
      'they want it. this has been the same thing for most of this, and '
      'i think that it has been for many, many years. and i was born and '
      'raised in a house that was kind of just the typical of what we '
      'were used to. but this time, i was sitting in the living room of '
      'that house and my parents were sitting in the living room and so '
      'i was being led upstairs, i was looking through a closet, and i '
      'looked down it and i saw a big white book with the word "saved" '
      'on it, like "we\'ve all lived here for a while, we\'ll take the '
      'books and have them back, and we\'ll go back and change out the '
      'books and try to change the way we do things for the kids." and '
      'the dad was very surprised.'),
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
      'looked down it and I saw a big white book with the word "saved" '
      'on it, like "we\'ve all lived here for a while, we\'ll take the '
      'books and have them back, and we\'ll go back and change out the '
      'books and try to change the way we do things for the kids." And '
      'the dad was very surprised.')),
    (('mikaela weisse, who helps run this site, demonstrates how it works. '
      'she zooms in on one small area of the center of Africa. it '
      'looks a bit like google\'s, except that this map is updated '
      'constantly. behind the scenes, computers sift through a flood of '
      'images collected from satellites, day by day, using techniques devised '
      'by researchers at the university of maryland and wageningen university '
      'in the netherlands. when the software notices a change - when trees '
      'have disappeared from a particular spot since the satellite last '
      'looked at it — it issues an alert, and a color-coded spot shows up '
      'on the map where trees appear to have vanished. the satellites visit '
      'each spot on the globe about once a week.'),
     ('Mikaela Weisse, who helps run this site, demonstrates how it works. '
      'She zooms in on one small area of the center of Africa. It '
      'looks a bit like Google\'s, except that this map is updated '
      'constantly. Behind the scenes, computers sift through a flood of '
      'images collected from satellites, day by day, using techniques devised '
      'by researchers at the University of Maryland and Wageningen University '
      'in the Netherlands. When the software notices a change - when trees '
      'have disappeared from a particular spot since the satellite last '
      'looked at it — it issues an alert, and a color-coded spot shows up '
      'on the map where trees appear to have vanished. The satellites visit '
      'each spot on the globe about once a week.')),
    (('spike lee has spent the last four decades making movies that force '
      'america to confront its history. his latest film, da 5 bloods, '
      'released last year on netflix, centers on veterans who served in the '
      'vietnam war. in the initial screenplay, the majority of the characters '
      'where white, but lee and kevin willmott purposefully called '
      'them black soldiers.') ,
     ('Spike Lee has spent the last four decades making movies that force '
      'America to confront its history. His latest film, Da 5 bloods, '
      'released last year on Netflix, centers on veterans who served in the '
      'Vietnam war. In the initial screenplay, the majority of the characters '
      'where white, but Lee and Kevin Willmott purposefully called '
      'them black soldiers.'))
]



@pytest.mark.parametrize("input_text, expected", input_and_expected_texts)
def test_postprocess(input_text, expected):
    text_postprocessor = tp.TextPostprocessor()
    assert text_postprocessor.postprocess(input_text) == expected
