import requests

era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
db_id = '@@{DB_ID}@@'
db_entity_name = '@@{DB_ENTITY_NAME}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = "https://{}:8443/era/v0.9/clones/{}".format(era_ip,db_id)
data =  {
    "delete": True,
    "remove": False,
    "softRemove": False,
    "forced": False,
    "deleteTimeMachine": False, #todo tocheck
    "deleteLogicalCluster": True
    }

# Cleanup the DB and get Operation ID
print("Cleanup DB Clone : '{}' with UUID '{}'".format(db_entity_name,db_id))
requests.packages.urllib3.disable_warnings()
response = requests.request("DELETE", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))

if response.status_code == 500:
    print("Database Clone Already Deleted. Proceed To DB Server Shutdown.")
    print(u"status code: {0}".format(response.status_code))
    print(u"reason: {0}".format(response.reason))
    print(u"text: {0}".format(response.text))
    print("CLEANUP_OPERATION_ID=NONE")
else:
    print("Cleanup Database Clone Initiated")
    print("CLEANUP_OPERATION_ID={0}".format(response.json()['operationId']))

