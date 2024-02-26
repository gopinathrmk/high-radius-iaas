era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
cleanup_operation_id = '@@{CLEANUP_OPERATION_ID}@@'

if cleanup_operation_id == 'NONE':
    print("Database Already Deleted. Proceed To DB Server Shutdown.")
    exit(0)

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url     = "https://{}:8443/era/v0.8/operations/{}".format(era_ip,cleanup_operation_id)

# Monitor the operation
for x in range(120):
    print("Waiting for 60 Seconds")
    sleep(60)

    resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
    if not resp.ok:
        print("Couldn't retrieve Detail of Unregister DB Operation : '{}' !!!".format(cleanup_operation_id))
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
        print("Unregister DB Operation Completed With Message:", resp_content['message'])
        break    

# If the operation did not complete within 10 minutes, assume it's not successful and error out
if resp_content['percentageComplete'] != "100":
    print("Waited for 120 mins and Unregister DB is not completed. Exiting")
    print("Message : ",resp_content['message'])
    exit(1)


