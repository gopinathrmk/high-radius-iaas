# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url     = "https://@@{NDB_IP}@@:8443/era/v0.8/operations/@@{REGISTER_OPERATION_ID}@@"

# Monitor the operation
for x in range(120): 

  print "Wait 60 Seconds"
  sleep(60)

  resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
  #print json.loads(resp.content)
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