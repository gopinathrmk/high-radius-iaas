import requests
from datetime import datetime

# Avoid security exceptions/warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HYCU_ENDPOINT = 'hycu.emeagso.lab'
HYCU_USER = 'admin'
HYCU_SECRET = 'Nutanix/4u!'
HYCU_POLICY_MAP = "@@{policy_map}@@"
HYCU_POLICY_NAME = "@@{hycu_policy_name}@@"
VM_NAME = "@@{hostname}@@"

headers = {'Content-Type': 'application/json','Accept': 'application/json'}

def huFindItemByValue(items, propName, propValue):
    for key in items:
        if items[key][propName] == propValue:
            return items[key]
    return None

def huGetVMs(timeout=5, pagesize=100):
    """ Retrieves dictionary of event[uuid] """
    url = "https://{}:8443/rest/v1.0/vms?forceSync=false&pageSize={}&pageNumber=1".format(HYCU_ENDPOINT, pagesize)
    repsonse = requests.get(url, auth=(HYCU_USER, HYCU_SECRET), headers=headers, timeout=timeout, verify=False)
    print(repsonse.content)
    dict = {}
    if repsonse.ok:
        data = repsonse.json()
        for item in data['entities']:
            dict[item['uuid']] = item
            print(dict)
        return dict

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

def hu_get_policy_uuid(policy_name):
    print(HYCU_POLICY_MAP)
    uuid = [x['uuid'] for x in json.loads(HYCU_POLICY_MAP) if x['name'] == policy_name][0]
    return uuid

def hu_assign_policy(pol_uuid, vm_uuid):
    url = "https://{}:8443/rest/v1.0/policies/{}/assign".format(HYCU_ENDPOINT, pol_uuid)
    data = {
        "vmUuidList": [
            "{}".format(vm_uuid)
        ]
        }
    response = requests.post(url, auth=(HYCU_USER, HYCU_SECRET), headers=headers, json=data, verify=False)
    print(response.content)
    return response.status_code

# Retrieve the list of VMs from HYCU Rest API server (page by page)
vms = huGetVMs()
hycu_vm_data = huFindItemByValue(vms, 'vmName', VM_NAME)
hycu_vm_uuid = hycu_vm_data['uuid']
print('vm uuid is {}'.format(hycu_vm_uuid))

policy_uuid = hu_get_policy_uuid(HYCU_POLICY_NAME)
print('Policy uuid is {}'.format(policy_uuid))

assign = hu_assign_policy(policy_uuid, hycu_vm_uuid)
print(assign)
