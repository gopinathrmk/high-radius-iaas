from datetime import datetime

era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

time_machine_id = '@@{TIME_MACHINE_ID}@@'
clone_instance_name = '@@{CLONE_INSTANCE_NAME}@@'
calm_application_name = '@@{calm_application_name}@@'
cluster_id='@@{CLUSTER_ID}@@'
db_server_pwd = '@@{DB_SERVER_BASIC.secret}@@'
clone_root_pass = '@@{CLONE_ROOT_PASS}@@'
ndb_public_key = '@@{NDB_public_key}@@'
clone_vm_name = '@@{CLONE_VM_NAME}@@'
compute_prof_id = '@@{COMPUTE_PROF_ID}@@'
network_prof_id = '@@{NETWORK_PROF_ID}@@'
db_param_id = '@@{DB_PARAM_ID}@@'
db_snapshot_id = '@@{DB_SNAPSHOT_ID}@@'
restore_date_time = "@@{RESTORE_DATE_TIME}@@"
restore_type = '@@{RESTORE_TYPE}@@'

# Set the URL and payload  
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url     = "https://{}:8443/era/v0.9/tms/{}/clones".format(era_ip,time_machine_id)

payload = {
  'name': clone_instance_name,
  'description': 'Clone For MySQL Database {} Provisioned By NCM Self-Service App {}'.format(calm_application_name,calm_application_name),
  'createDbserver': True,
  'clustered': False,
  'nxClusterId': cluster_id,
  'sshPublicKey': ndb_public_key,
  'dbserverId': None,
  'dbserverClusterId': None,
  'dbserverLogicalClusterId': None,
  'timeMachineId': time_machine_id,
  'snapshotId': None,
  'userPitrTimestamp': None,
  'timeZone': 'Asia/Calcutta',
  'latestSnapshot': False,
  'nodeCount': 1,
  'nodes': [
    {
      'vmName': clone_vm_name,
      'computeProfileId': compute_prof_id,
      'networkProfileId': network_prof_id,
      'newDbServerTimeZone': None,
      'nxClusterId': cluster_id,
      'properties': []
    }
  ],
  'actionArguments': [
    {
      'name': 'vm_name',
      'value': clone_vm_name
    },
    {
      'name': 'dbserver_description',
      'value': 'Clone For MySQL Database {} Provisioned By NDB Via NCM Self-Service App {}'.format(calm_application_name,calm_application_name)
    },
    {
      'name': 'db_password',
      'value': clone_root_pass
    }
  ],
  'tags': [],
  'vmPassword': db_server_pwd,
  'computeProfileId': compute_prof_id,
  'networkProfileId': network_prof_id,
  'databaseParameterProfileId': db_param_id
}

if restore_type == 'Snapshot':
    payload['snapshotId'] = db_snapshot_id
else:
    # Input date and time string
    input_str = restore_date_time

    # Convert string to datetime object
    input_datetime = datetime.strptime(input_str, "%d/%m/%Y - %H:%M:%S")

    # Format the datetime object as a string in the desired format
    output_str = input_datetime.strftime("%Y-%m-%d %H:%M:%S")

    print("Clone DB At " + output_str)

    payload['userPitrTimestamp'] = output_str

# Make the call and set the response operation ID to the variable
resp = urlreq(url, verb='POST', auth='BASIC', user=era_user, passwd=era_pass, params=json.dumps(payload), headers=headers)
if not resp.ok:
    print("Clone Operation request is not accepted !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)


print(resp.text)
print("Clone Operation Request is sent ")
print('CREATE_OPERATION_ID={0}'.format(json.loads(resp.content)['operationId']))


"""
# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Set the URL and payload  
url     = 'https://@@{NDB_IP}@@:8443/era/v0.9/tms/@@{TIME_MACHINE_ID}@@/clones'

payload = {
  'name': '@@{CLONE_INSTANCE_NAME}@@',
  'description': 'Clone For MySQL Database @@{calm_application_name}@@ Provisioned By NCM Self-Service App @@{calm_application_name}@@',
  'createDbserver': True,
  'clustered': False,
  'nxClusterId': '@@{CLUSTER_ID}@@',
  'sshPublicKey': '@@{NDB_public_key}@@',
  'dbserverId': None,
  'dbserverClusterId': None,
  'dbserverLogicalClusterId': None,
  'timeMachineId': time_machine_id,
  'snapshotId': None,
  'userPitrTimestamp': None,
  'timeZone': 'Asia/Calcutta',
  'latestSnapshot': False,
  'nodeCount': 1,
  'nodes': [
    {
      'vmName': '@@{CLONE_VM_NAME}@@',
      'computeProfileId': '@@{COMPUTE_PROF_ID}@@',
      'networkProfileId': '@@{NETWORK_PROF_ID}@@',
      'newDbServerTimeZone': None,
      'nxClusterId': '@@{CLUSTER_ID}@@',
      'properties': []
    }
  ],
  'actionArguments': [
    {
      'name': 'vm_name',
      'value': '@@{CLONE_VM_NAME}@@'
    },
    {
      'name': 'dbserver_description',
      'value': 'Clone For MySQL Database @@{calm_application_name}@@ Provisioned By NDB Via NCM Self-Service App @@{calm_application_name}@@'
    },
    {
      'name': 'db_password',
      'value': '@@{CLONE_ROOT_PASS}@@'
    }
  ],
  'tags': [],
  'vmPassword': '@@{DB_SERVER_BASIC.secret}@@',
  'computeProfileId': '@@{COMPUTE_PROF_ID}@@',
  'networkProfileId': '@@{NETWORK_PROF_ID}@@',
  'databaseParameterProfileId': '@@{DB_PARAM_ID}@@'
}

if '@@{RESTORE_TYPE}@@' == 'Snapshot':
  payload['snapshotId'] = '@@{DB_SNAPSHOT_ID}@@'
else:
	from datetime import datetime

	# Input date and time string
	input_str = "@@{RESTORE_DATE_TIME}@@"

	# Convert string to datetime object
	input_datetime = datetime.strptime(input_str, "%d/%m/%Y - %H:%M:%S")

	# Format the datetime object as a string in the desired format
	output_str = input_datetime.strftime("%Y-%m-%d %H:%M:%S")

	print "Clone DB At " + output_str

  	payload['userPitrTimestamp'] = output_str

# Make the call and set the response operation ID to the variable
resp = urlreq(url, verb='POST', auth='BASIC', user=era_user, passwd=era_pass, params=json.dumps(payload), headers=headers)
print resp.text
print 'CREATE_OPERATION_ID={0}'.format(json.loads(resp.content)['operationId'])

"""