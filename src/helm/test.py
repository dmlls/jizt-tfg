"""Temporary test script."""

import time
import requests
import json
from pprint import pprint

INGRESS_URL = "https://api.jizt.it"


def post(text, model = 't5-large', params = {}, bad_request=False):
    url = f"{INGRESS_URL}/v1/summaries/plain-text"
    response = requests.post(url,
                            json={'source': text, 'model': model, 'params': params})
    print("VALID POST REQUEST to", url)
    try:
        print("CODE:", response.status_code)
        pprint(response.json())
    except json.decoder.JSONDecodeError:
        print(response)

    if bad_request:
        bad_request_response = requests.post(url, json={'bad_key': text})
        print("\nBAD POST REQUEST (bad key) to", url)
        try:
            print("CODE:", bad_request_response.status_code)
            pprint(bad_request_response.json())
        except json.decoder.JSONDecodeError:
            print(bad_request_response)

    return response.json()['summary_id']


def get(summary_id, wait=False, bad_request=False):
    url = f"{INGRESS_URL}/v1/summaries/plain-text/{summary_id}"
    response = requests.get(url)
    while wait:
        if response.json()['status'] == 'completed':
            break
        time.sleep(0.2)
        response = requests.get(url)

    print("\nVALID GET REQUEST to", url)
    try:
        print("CODE:", response.status_code)
        pprint(response.json())
    except json.decoder.JSONDecodeError:
        print(response)

    if bad_request:
        bad_url = f"{INGRESS_URL}/v1/summaries/plain-text/{99999999999}"
        bad_request_response = requests.get(bad_url)
        print("\nBAD GET REQUEST (non-existent summary) to", bad_url)
        try:
            print("CODE:", bad_request_response.status_code)
            pprint(bad_request_response.json())
        except json.decoder.JSONDecodeError:
            print(bad_request_response)


# source: https://reasonandmeaning.com/2017/10/31/what-is-social-cooling/
text = """
Social cooling refers to the idea that if “you feel you are being watched, you change your behavior.” And the massive amounts of data being collected, especially online, is exxagerating this effect. This may limit our desire to speak or think freely thus bring about “chilling effects” on society—or social cooling.

Here’s a summary of how this works: 1.  Your data is collected and scored. Then data brokers use algorithms to reveal thousands of private details about you—friends and acquaintances, religious and political beliefs, educational background, sexual orientation, reading habits, personality traits and flaws, economic stability,  etc. This derived data is protected as corporate free speech.

2. Your digital reputation may affect your opportunities. Facebook posts may affect job chances of getting or losing a job, bad friends may affect the rate of your loan, etc. These effects are independent of whether the data is good or bad.

3. People start changing their behavior to get better scores which have disparate outcomes. Social Cooling describes the negative side effects of trying to be reputable online. Some of the negative effects are:

a) Conformity – you may hesitate to click on a link because you fear being tracked. This is self-censoring, which has a chilling effect. You fear choosing freely.

b) Risk-aversion –  When physicians are scored, those who try to help sicker patients have lower scores than those who avoid such patients because sicker patients have higher mortality rates.

c) Social rigidity – Our digital reputations limit our will to protest. For instance, Chinese citizens have begun to get “social credit scores,” which score how well-behaved they are. Such social pressure is a powerful form of control.

4) As your weaknesses are mapped, you become increasingly transparent. This leads to self-censorship, conformity, risk-aversion, and social rigidity becoming normal. No longer is data a matter of simple credit scores.

All of this leads to questions like: When we become more well-behaved, do we also become less human? What does freedom mean in a world where surveillance is the dominant business model? Are we undermining our creative economy because people fear non-conformity? Can minority views still inform us?

5) The solution? Pollution of our social environment is invisible to most people, just like air pollution and climate change once were. So we begin by increasing awareness.  But we should act quickly, as data mining and the secrets it reveals is increasing exponentially.

(Example – I have an advanced degree. This simple piece of data predicts that: I despise and fear Donald Trump and the Republicans; I am a good critical thinker who understands the difference between the high journalistic standards of the New York Times or the Washington Post and the non-existent ones of Fox “News,” Breitbart, etc.; I don’t believe in alien abductions or faked moon landings; I know that evolution and climate change are true beyond any reasonable doubt; I’m not a theist, much less a Christian, Mormon, or Islamic fundamentalist; etc. All that from just one bit of data. Imagine what else others know about you and me?)

6) Conclusion

a) Data is not the new gold, it is the new oil, and it damages the social environment  .

b) Privacy is the right to be imperfect, even when judged by algorithms.

c) Privacy is the right to be human.
"""

model = 't5-large'

params = {
    "relative_max_length": 0.4,
    "relative_min_length": 0.2,
    "non_existent_param": 11  # this param will be ignored
}

print(f'ORIGINAL TEXT:\n"{text}"\n')
summary_id = post(text, model, params)

get(summary_id)

print("\nWaiting...")

get(summary_id, wait=True)
