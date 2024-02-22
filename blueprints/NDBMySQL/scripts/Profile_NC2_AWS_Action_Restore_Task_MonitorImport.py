era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
register_operation_id = '@@{REGISTER_OPERATION_ID}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url     = "https://{}:8443/era/v0.8/operations/{}".format(era_ip,register_operation_id)


for x in range(120): 
    print("Waiting for 60 Seconds")
    sleep(60)

    resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
    if not resp.ok:
        print("Couldn't retrieve Detail of Register DB Operation : '{}' !!!".format(register_operation_id))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        continue
   
    #print json.loads(resp.content)
    resp_content = json.loads(resp.content)
    print("Percentage Complete: {0}".format(resp_content['percentageComplete']))
    if resp_content['status'] == '4':
        print("Operation Failed With Message:", resp_content['message'])
        exit(1)

    # If complete, break out of loop
    if resp_content['percentageComplete'] == "100":
        print("Operation Completed With Message:", resp_content['message'])
        break    

# If the operation did not complete within 120 minutes, assume it's not successful and error out
if resp_content['percentageComplete'] != "100":
    print("Waited for 120 mins and Register DB operation is not completed. Exiting")
    print("Message : ",resp_content['message'])
    exit(1)





"""
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
"""