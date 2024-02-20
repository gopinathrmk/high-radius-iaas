# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Cleanup the DB and get Operation ID
url = "https://@@{NDB_IP}@@:8443/era/v0.9/dbservers/@@{DB_SERVER_ID}@@"

data = '''
{
  "softRemove": false,
  "remove": false,
  "delete": true,
  "deleteVgs": true,
  "deleteVmSnapshots": true
}
'''


skip_delete = '''
import requests

requests.packages.urllib3.disable_warnings()
response = requests.request("DELETE", url, data=data, verify=False, auth=(era_user, era_pass))

if response.status_code == 500:
  print "Cannot Deregister: " + json.loads(response.content)['message']
else:
  print "Deregister Request Sent"
  url = "https://@@{NDB_IP}@@:8443/era/v0.8/operations/{}".format(response.json()['operationId'])

# Monitor the operation
  for x in range(20):  
    print "Wait 30 Seconds"
    sleep(30)
    resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
    print "Percentage Complete: {0}".format(json.loads(resp.content)['percentageComplete'])
  
    # If complete, break out of loop
    if json.loads(resp.content)['percentageComplete'] == "100":
      break    

  # If the operation did not complete within 10 minutes, assume it's not successful and error out
  if json.loads(resp.content)['percentageComplete'] != "100":
    exit(1)
'''