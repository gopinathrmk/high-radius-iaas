# Set creds, headers, and URL
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
delete_db_operation_id = '@@{DELETE_DB_OPERATION_ID}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url     = "https://{}:8443/era/v0.8/operations/{}".format(era_ip,delete_db_operation_id)

# Monitor the operation
for x in range(20):
    print("Waiting for 30 Seconds")
    sleep(30)

    resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
    if not resp.ok:
        print("Couldn't retrieve Detail of Delete DB VM Operation : '{}' !!!".format(delete_db_operation_id))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        continue

    resp_content = json.loads(resp.content)
    print("Percentage Complete: {0}".format(resp_content['percentageComplete']))

    # If complete, break out of loop
    if resp_content['percentageComplete'] == "100":
        print("Delete DB VM Operation Completed With Message:", resp_content['message'])
        break    

# If the operation did not complete within 10 minutes, assume it's not successful and error out
if resp_content['percentageComplete'] != "100":
    print("Waited for 10 mins and Delete DB VM is not completed. Exiting")
    print("Message : ",resp_content['message'])
    exit(1)
