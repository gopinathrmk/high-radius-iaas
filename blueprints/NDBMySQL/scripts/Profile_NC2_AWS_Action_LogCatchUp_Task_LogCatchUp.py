import requests

era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
time_machine_id = '@@{TIME_MACHINE_ID}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Cluster ID
url     = "https://{}/era/v0.9/tms/{}/log-catchups".format(era_ip,time_machine_id)
payload = {
  "actionHeader": [
    {
      "name": "switch_log",
      "value": "true"
    }
  ]
}


requests.packages.urllib3.disable_warnings()
resp = requests.post(url, auth=(era_user, era_pass), headers=headers, json=payload, verify=False)
if not resp.ok:
    print("Log Catch up request could not be sent !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)
print("Log Catch Up Request Sent With Operation Id {}".format(resp.json()['operationId']))

url = "https://{0}:8443/era/v0.8/operations/{1}".format(era_ip, resp.json()['operationId'])

# Monitor the operation
for x in range(60):
    print("Waiting for 30 Seconds")
    sleep(30)

    resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
    if not resp.ok:
        print("Couldn't retrieve Detail of Log catch up Operation : '{}' !!!")
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        continue

    resp_content = json.loads(resp.content)
    print("Percentage Complete: {0}".format(resp_content['percentageComplete']))

    # If complete, break out of loop
    if resp_content['percentageComplete'] == "100":
        print("Log catch up Operation Completed With Message:", resp_content['message'])
        break    

# If the operation did not complete within 10 minutes, assume it's not successful and error out
if resp_content['percentageComplete'] != "100":
    print("Waited for 60 mins and Log catch up is not completed. Exiting")
    print("Message : ",resp_content['message'])
    exit(1)

"""
# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Cluster ID
url     = "https://{0}/era/v0.9/tms/@@{TIME_MACHINE_ID}@@/log-catchups".format(era_ip)
payload = {
  "actionHeader": [
    {
      "name": "switch_log",
      "value": "true"
    }
  ]
}


import requests

requests.packages.urllib3.disable_warnings()
resp = requests.post(url, auth=(era_user, era_pass), headers=headers, json=payload, verify=False)

print "Log Catch Up Request Sent With Operation Id {}".format(resp.json()['operationId'])
url = "https://{0}:8443/era/v0.8/operations/{1}".format(era_ip, resp.json()['operationId'])

# Monitor the operation
for x in range(60):
  print "Wait 30 Seconds"
  sleep(30)
  resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
  print "Percentage Complete: {0}".format(json.loads(resp.content)['percentageComplete'])  
  if json.loads(resp.content)['status'] == '4':
    print "Operation Failed With Message:", json.loads(resp.content)['message'] 
    exit(1)  
  
  # If complete, break out of loop
  if json.loads(resp.content)['percentageComplete'] == "100":
    break    

# If the operation did not complete within 120 minutes, assume it's not successful and error out
if json.loads(resp.content)['percentageComplete'] != "100":
  exit(1)

"""