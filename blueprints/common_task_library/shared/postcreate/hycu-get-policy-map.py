import requests
from datetime import datetime

# Avoid security exceptions/warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HYCU_ENDPOINT = 'hycu.emeagso.lab'
HYCU_USER = 'admin'
HYCU_SECRET = 'Nutanix/4u!'

headers = {'Content-Type': 'application/json','Accept': 'application/json'}

def hu_get_policies(timeout=5, pagesize=100):
    """ Retrieves dictionary of event[uuid] """
    url = "https://{}:8443/rest/v1.0/policies?pageSize={}&pageNumber=1".format(HYCU_ENDPOINT, pagesize)
    repsonse = requests.get(url, auth=(HYCU_USER, HYCU_SECRET), headers=headers, timeout=timeout, verify=False)
    if repsonse.ok:
        data = repsonse.json()
        policy_dict = {}
        for p in data['entities']:
            policy_uuid = p["uuid"]
            policy_dict[policy_uuid] = p["name"]

        policy_list = []
        for key, value in policy_dict.items():
            x = {"name": value, "uuid": key}
            policy_list.append(x)
        return policy_list

# Retrieve the list of Policies from HYCU Rest API server (page by page)
policies = hu_get_policies()
policies = json.dumps(policies)
print("hycu_policy_map={}".format(policies))