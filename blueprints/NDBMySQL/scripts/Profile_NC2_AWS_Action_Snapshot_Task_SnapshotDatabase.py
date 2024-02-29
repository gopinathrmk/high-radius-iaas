import requests

era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
time_machine_id = '@@{TIME_MACHINE_ID}@@'
db_snapshot_name = '@@{DB_SNAPSHOT_NAME}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Cluster ID
url     = "https://{0}/era/v0.9/tms/@@{TIME_MACHINE_ID}@@/snapshots".format(era_ip)
payload = {
  "name": "@@{DB_SNAPSHOT_NAME}@@"
}

import requests

requests.packages.urllib3.disable_warnings()
resp = requests.post(url, auth=(era_user, era_pass), headers=headers, json=payload, verify=False)

"""
# Get Cluster ID
url     = "https://{0}/era/v0.9/tms/{1}/snapshots".format(era_ip,time_machine_id)
payload = {
  "name": db_snapshot_name
}

resp = urlreq(url, verb='POST', auth='BASIC', user=era_user, passwd=era_pass, params=json.dumps(payload), headers=headers)
if not resp.ok:
    print("Request to take Snapshot Failed !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)
"""
resp_content = json.loads(resp.content)
snapshot_operation_id = resp_content.get("operationId",None)
print("Snapshot Request Sent With Operation Id {}".format(snapshot_operation_id))

url     = "https://{0}:8443/era/v0.8/operations/{1}".format(era_ip, snapshot_operation_id)

# Monitor the operation
for x in range(60):
    print("Waiting for 30 Seconds")
    sleep(30)

    resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
    if not resp.ok:
        print("Couldn't retrieve Detail of Snapshot Operation : '{}' !!!".format(snapshot_operation_id))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        continue

    resp_content = json.loads(resp.content)
    print("Percentage Complete: {0}".format(resp_content['percentageComplete']))
    if resp_content['status'] == '4':
        print("Operation Failed With Message:", resp_content['message'])
        exit(1)

    # If complete, break out of loop
    if resp_content['percentageComplete'] == "100":
        print("Snapshot Operation Completed With Message:", resp_content['message'])
        break    

# If the operation did not complete within 30 minutes, assume it's not successful and error out
if resp_content['percentageComplete'] != "100":
    print("Waited for 30 mins and Snapshot is not completed. Exiting !!!")
    print("Message : ",resp_content['message'])
    exit(1)

