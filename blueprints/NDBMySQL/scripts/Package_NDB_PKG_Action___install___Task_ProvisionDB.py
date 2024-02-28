# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
calm_application_name = '@@{calm_application_name}@@'
cluster_id='@@{CLUSTER_ID}@@'
software_prof_id = '@@{SOFTWARE_PROF_ID}@@'
software_prof_ver_id = '@@{SOFTWARE_PROF_VERSION_ID}@@'
compute_prof_id = '@@{COMPUTE_PROF_ID}@@'
network_prof_id = '@@{NETWORK_PROF_ID}@@'
db_param_id = '@@{DB_PARAM_ID}@@'
sla_id = '@@{SLA_ID}@@'
db_server_pwd = '@@{DB_SERVER_BASIC.secret}@@'
ndb_public_key = '@@{NDB_public_key}@@'
db_size = '@@{DB_SIZE}@@'
db_pass = '@@{DB_PASS}@@'
db_name = '@@{DB_NAME}@@'

# Set the URL and payload
url     = "https://{}:8443/era/v0.9/databases/provision".format(era_ip)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {
  'name': calm_application_name,
  'databaseType': 'mysql_database',
  'databaseDescription': 'MySQL Database Provisioned By NCM Self-Service App : {}'.format(calm_application_name),
  'nxClusterId': cluster_id,
  'softwareProfileId': software_prof_id,
  'softwareProfileVersionId': software_prof_ver_id,
  'computeProfileId': compute_prof_id,
  'networkProfileId': network_prof_id,
  'dbParameterProfileId': db_param_id,
  'createDbserver': True,
  'nodeCount': 1,
  'clustered': False,
  'vmPassword': db_server_pwd,
  'sshPublicKey': ndb_public_key,
  'autoTuneStagingDrive': True,
  'timeMachineInfo': {
    'name': calm_application_name + '_TM',
    'description': 'Time Machine For MySQL Database Provisioned By NCM Self-Service App : {}'.format(calm_application_name),
    'slaId': sla_id,
    'schedule': {
      'snapshotTimeOfDay': {
        'hours': 22,
        'minutes': 0,
        'seconds': 0
      },
      'continuousSchedule': {
        'enabled': True,
        'logBackupInterval': 30,
        'snapshotsPerDay': 1
      },
      'weeklySchedule': {
        'enabled': True,
        'dayOfWeek': 'THURSDAY'
      },
      'monthlySchedule': {
        'enabled': True,
        'dayOfMonth': '23'
      },
      'quartelySchedule': {
        'enabled': True,
        'startMonth': 'JANUARY',
        'dayOfMonth': '23'
      },
      'yearlySchedule': {
        'enabled': False,
        'dayOfMonth': 31,
        'month': 'DECEMBER'
      }
    },
    'tags': [],
    'autoTuneLogDrive': True
  },
  'actionArguments': [
    {
      'name': 'listener_port',
      'value': '3306'
    },
    {
      'name': 'database_size',
      'value': db_size
    },
    {
      'name': 'auto_tune_staging_drive',
      'value': True
    },
    {
      'name': 'db_password',
      'value': db_pass
    },
    {
      'name': 'database_names',
      'value': db_name
    },
    {
      'name': 'dbserver_description',
      'value': 'MySQL Database Server Provisioned By NDB Via NCM Self-Service App : {}'.format(calm_application_name)
    }
  ],
  'nodes': [
    {
      'properties': [],
      'vmName': calm_application_name,
      'networkProfileId': network_prof_id
    }
  ]
}


# Make the call and set the response operation ID to the variable
resp = urlreq(url, verb='POST', auth='BASIC', user=era_user, passwd=era_pass, params=json.dumps(payload), headers=headers)
if not resp.ok:
    print("Database Couldn't be provisioned !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print(resp.text)
print('CREATE_OPERATION_ID={0}'.format(json.loads(resp.content)['operationId']))

