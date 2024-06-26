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
  'timeMachineId': '@@{TIME_MACHINE_ID}@@',
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