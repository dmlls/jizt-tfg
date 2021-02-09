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

"""REST API tests."""


import pytest
import time
import requests
import json
import random

__version__ = '0.1.0'

API_URL = "https://api.jizt.it"
TEXT = """Social cooling refers to the idea that if “you feel you are being watched,
          you change your behavior.” And the massive amounts of data being collected,
          especially online, is exxagerating this effect. This may limit our desire
          to speak or think freely thus bring about “chilling effects” on society—or
          social cooling. Here’s a summary of how this works: 1.  Your data is
          collected and scored. Then data brokers use algorithms to reveal thousands
          of private detailsabout you—friends and acquaintances, religious and
          political beliefs, educational background, sexual orientation, reading
          habits, personality traits and flaws, economic stability,  etc. This
          derived data is protected as corporate free speech. 2. Your digital
          reputation may affect your opportunities. Facebook posts may affect
          job chances of getting or losing a job, bad friends may affect the rate
          of your loan, etc. These effects are independent of whether the data is
          good or bad. 3. People start changing their behavior to get better scores
          which have disparate outcomes. Social Cooling describes the negative side
          effects of trying to be reputable online. Some of the negative effects are:
          a) Conformity – you may hesitate to click on a link because you fear being
          tracked. This is self-censoring, which has a chilling effect. You fear
          choosing freely. b) Risk-aversion –  When physicians are scored, those who
          try to help sicker patients have lower scores than those who avoid such
          patients because sicker patients have higher mortality rates.
          c) Social rigidity – Our digital reputations limit our will to protest.
          For instance, Chinese citizens have begun to get “social credit scores,”
          which score how well-behaved they are. Such social pressure is a powerful
          form of control. 4) As your weaknesses are mapped, you become increasingly
          transparent. This leads to self-censorship, conformity, risk-aversion, and
          social rigidity becoming normal. No longer is data a matter of simple
          credit scores. All of this leads to questions like: When we become more
          well-behaved, do we also become less human? What does freedom mean in a
          world where surveillance is the dominant business model? Are we
          undermining our creative economy because people fear non-conformity? Can
          minority views still inform us?
          5) The solution? Pollution of our social environment is invisible to most
          people, just like air pollution and climate change once were. So we begin
          by increasing awareness.  But we should act quickly, as data mining and the
          secrets it reveals is increasing exponentially.
          (Example – I have an advanced degree. This simple piece of data predicts
          that: I despise and fear Donald Trump and the Republicans; I am a good
          critical thinker who understands the difference between the high
          journalistic standards of the New York Times or the Washington Post and the
          non-existent ones of Fox “News,” Breitbart, etc.; I don’t believe in alien
          abductions or faked moon landings; I know that evolution and climate change
          are true beyond any reasonable doubt; I’m not a theist, much less a
          Christian, Mormon, or Islamic fundamentalist; etc. All that from just one
          bit of data. Imagine what else others know about you and me?)
          6) Conclusion
          a) Data is not the new gold, it is the new oil, and it damages the social
          environment.
          b) Privacy is the right to be imperfect, even when judged by algorithms.
          c) Privacy is the right to be human."""


def post(json_attributes):
    """HTTP POST request."""

    url = f"{API_URL}/v1/summaries/plain-text"
    response = requests.post(url, json=json_attributes)
    return response


def get(summary_id):
    """HTTP POST request."""

    url = f"{API_URL}/v1/summaries/plain-text/{summary_id}"
    response = requests.get(url)
    return response


def pull(response):
    """Make consecutive GET requests until the summary is completed."""

    summary_id = response.json()['summary_id']
    while True:
        if response.json()['status'] == 'completed':
            return response
        time.sleep(0.2)
        response = get(summary_id)
        assert response.status_code == 200  # OK


def validate_response(response, status_code):
    """Validate HTTP response."""

    assert response.status_code == status_code
    response = pull(response).json()
    # Check that we got something as output
    assert len(response['output']) > 0
    assert all(key in response for key in ('model', 'params', 'language'))
    assert len(response['params']) == 11  # currently, there are 11 summary parameters


def test_all_tests():
    pass


def test_request_no_source():
    json_attributes = {}
    response = post(json_attributes)
    assert response.status_code == 400  # Bad Request
    assert (response.json()['errors'] == 
            {'source': ['Missing data for required field.']})


def test_request_only_source():
    # We add a hash at the end of the source to avoid caching
    json_attributes = {'source': f"{TEXT} {hash(random.random())}"}
    response = post(json_attributes)
    validate_response(response, 202)  # Accepted






#def test_request_source_and_model