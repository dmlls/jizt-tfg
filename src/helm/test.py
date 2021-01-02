"""Temporary test script."""

import time
import requests
import json

# HOST = "http://api.jizt.it"
HOST = "http://35.186.248.210"

text = ("GNU is       an extensive collection of wholly free software , which gave rise "
        "to the family of operating systems popularly known as Linux.  GNU is also "
        "the project   within which the free software concept originated   . most of GNU "
        "is      licensed under the GNU Project's own General Public License (GPL).")

url = f"{HOST}/v1/summaries/plain-text"
response = requests.post(url, json={'source': text})
print("VALID POST REQUEST to", url)
try:
    print("CODE:", response.status_code)
    print(response.json())
except json.decoder.JSONDecodeError as err:
    print(response)

bad_request_response = requests.post(url, json={'bad_key': text})
print("\nBAD POST REQUEST (bad key) to", url)
try:
    print("CODE:", bad_request_response.status_code)
    print(bad_request_response.json())
except json.decoder.JSONDecodeError as err:
    print(bad_request_response)

print("\nWaiting...")
time.sleep(3)

url = f"{HOST}/v1/summaries/plain-text/{response.json()['job_id']}"
response = requests.get(url)
print("\nVALID GET REQUEST to", url)
try:
    print("CODE:", response.status_code)
    print(response.json())
except json.decoder.JSONDecodeError as err:
    print(response)

bad_url = f"{HOST}/v1/summaries/plain-text/{99999999999}"
bad_request_response = requests.get(bad_url)
print("\nBAD GET REQUEST (non-existent job) to", bad_url)
try:
    print("CODE:", bad_request_response.status_code)
    print(bad_request_response.json())
except json.decoder.JSONDecodeError as err:
    print(bad_request_response)