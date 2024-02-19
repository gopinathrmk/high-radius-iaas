import requests
import re
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# VARIABLES
username = "@@{INFOBLOX_USERNAME}@@"
username_secret = "@@{INFOBLOX_SECRET}@@"
infobloxip = "@@{INFOBLOX_ADDRESS}@@"
# FUNCTION
def rest_call(url, method, payload="", username=username, username_secret=username_secret):
    headers = {'content-type': 'application/json'}
    if payload:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            auth=HTTPBasicAuth(username, username_secret),
            verify=False
        )
    else:
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(username, username_secret),
            verify=False
        )
    if response.ok:
        try:
            print("Removed {0} from InfoBlox - Status Code is {1}".format(response.content, response.status_code))
        except:
            print(response.content)
    else:
        print("Request failed")
        print("Headers: {}".format(headers))
        print("Payload: {}".format(json.dumps(payload)))
        print('Status code: {}'.format(response.status_code))
        print(response.content)
        exit(1)
# LAUNCH
url = "https://{}/wapi/v2.11.3/request".format(infobloxip)
data = [
    {
        "method": "GET",
        "object": "ipv4address",
        "data": {"ip_address": "@@{staticip}@@"},
        "assign_state": {"ipaddr_ref": "_ref"},
        "enable_substitution": True,
        "discard": True
    },
    {
        "method": "DELETE",
        "object": "##STATE:ipaddr_ref:##",
        "enable_substitution": True
    }
]
rest_call(url, method='POST', payload=data)