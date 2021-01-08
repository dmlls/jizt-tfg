"""Temporary test script."""

import time
import requests
import json
from pprint import pprint

INGRESS_URL = "http://35.186.248.210"


def post(text, bad_request=False):
    url = f"{INGRESS_URL}/v1/summaries/plain-text"
    response = requests.post(url, json={'source': text})
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

    return response.json()['job_id']


def get(job_id, wait=False, bad_request=False):
    url = f"{INGRESS_URL}/v1/summaries/plain-text/{job_id}"
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
        print("\nBAD GET REQUEST (non-existent job) to", bad_url)
        try:
            print("CODE:", bad_request_response.status_code)
            pprint(bad_request_response.json())
        except json.decoder.JSONDecodeError:
            print(bad_request_response)


text = ("GNU is          an extensive collection of wholly free software , which gave rise "
        "to the family of operating systems popularly known as Linux.  GNU is also "
        "the project     within which the free software concept originated   . most of GNU "
        "is      licensed under the GNU Project's own General Public License (GPL).")

print(f'ORIGINAL TEXT:\n"{text}"\n')
job_id = post(text)

get(job_id)

print("\nWaiting...")

get(job_id, wait=True)
