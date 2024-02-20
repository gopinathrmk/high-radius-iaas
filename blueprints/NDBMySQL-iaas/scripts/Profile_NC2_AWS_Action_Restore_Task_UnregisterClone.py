era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = "https://@@{NDB_IP}@@:8443/era/v0.9/clones/@@{CLONE_INSTANCE_NAME}@@?value-type=name"

resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)

clone_id = resp.json()['id']

url = "https://@@{NDB_IP}@@:8443/era/v0.9/clones/{}".format(clone_id)

data = {
  "softRemove": False,
  "remove": True,
  "delete": False,
  "forced": False,
  "deleteLogicalCluster": True,
  "removeLogicalCluster": False,
  "deleteTimeMachine": True
}

import requests

requests.packages.urllib3.disable_warnings()
response = requests.request("DELETE", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))

print(response.status_code)
print(response.text)
print "CLEANUP_OPERATION_ID={0}".format(response.json()['operationId'])