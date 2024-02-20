# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

import requests

data =  {
  "delete": True,
  "remove": False,
  "softRemove": False,
  "forced": False,
  "deleteTimeMachine": False,
  "deleteLogicalCluster": True
}

# Cleanup the DB and get Operation ID
url = "https://@@{NDB_IP}@@:8443/era/v0.9/databases/@@{DB_ID}@@"

requests.packages.urllib3.disable_warnings()
response = requests.request("DELETE", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))

print "CLEANUP_OPERATION_ID={0}".format(response.json()['operationId'])