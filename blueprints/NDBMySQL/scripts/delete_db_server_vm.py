import requests

era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
db_server_id = '@@{DB_SERVER_ID}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = "https://{}:8443/era/v0.9/dbservers/{}".format(era_ip,db_server_id)
data = {
    "softRemove": False,
    "remove": False,
    "delete": True,
    "deleteVgs": True,
    "deleteVmSnapshots": True
    }

# Cleanup the DB Server and get Operation ID
requests.packages.urllib3.disable_warnings()
response = requests.request("DELETE", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))
#response = requests.request("DELETE", url, data=data, verify=False, auth=(era_user, era_pass))

if response.status_code == 500:
    print("Cannot Delete DB VM: " + json.loads(response.content)['message'])
    print(u"status code: {0}".format(response.status_code))
    print(u"reason: {0}".format(response.reason))
    print(u"text: {0}".format(response.text))    
    exit(1)
else:
    print("Delete DB VM Request Sent")
    print("DELETE_DB_OPERATION_ID={0}".format(response.json()['operationId']))
