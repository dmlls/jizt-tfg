"""Temporary test script."""

import requests
import json

HOST = "http://0.0.0.0:5000"

text = ("GNU is       an extensive collection of wholly free software , which gave rise "
        "to the family of operating systems popularly known as Linux.  GNU is also "
        "the project   within which the free software concept originated   . most of GNU "
        "is      licensed under the GNU Project's own General Public License (GPL).")


response = requests.post(HOST + '/v1/preprocessors/plain-text', json={'source': text})
print("VALID REQUEST")
try:
    print("CODE:", response.status_code)
    print(response.json())
except json.decoder.JSONDecodeError as err:
    print(response)

bad_request_response = requests.post(HOST + '/v1/preprocessors/plain-text', json={'bad_key': text})
print("\nBAD REQUEST")
try:
    print("CODE:", bad_request_response.status_code)
    print(bad_request_response.json())
except json.decoder.JSONDecodeError as err:
    print(bad_request_response)
