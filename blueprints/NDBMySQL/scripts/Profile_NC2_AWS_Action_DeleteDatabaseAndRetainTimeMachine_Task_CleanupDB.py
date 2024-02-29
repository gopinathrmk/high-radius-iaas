import requests

era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
db_id = '@@{DB_ID}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = "https://{}:8443/era/v0.9/databases/{}".format(era_ip,db_id)
data =  {
    "delete": False, #Need to use DB Later
    "remove": True,
    "softRemove": False,
    "forced": False,
    "deleteTimeMachine": False,
    "deleteLogicalCluster": True
    }

# Cleanup the DB and get Operation ID
requests.packages.urllib3.disable_warnings()
response = requests.request("DELETE", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))

if response.ok:
    print("Cleanup Database Initiated. Time machine and DB VM will not be deleted")
    print("CLEANUP_OPERATION_ID={0}".format(response.json()['operationId']))
else:
    print("Database Instance could not be deleted : '{}' !!!".format(json.loads(response.content)['message']))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))    
    exit(1)