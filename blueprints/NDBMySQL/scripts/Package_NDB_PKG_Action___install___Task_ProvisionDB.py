# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Set the URL and payload
url     = 'https://@@{NDB_IP}@@:8443/era/v0.9/databases/provision'

payload = {
  'name': '@@{calm_application_name}@@',
  'databaseType': 'mysql_database',
  'databaseDescription': 'MySQL Database Provisioned By NCM Self-Service App @@{calm_application_name}@@',
  'nxClusterId': '@@{CLUSTER_ID}@@',
  'softwareProfileId': '@@{SOFTWARE_PROF_ID}@@',
  'softwareProfileVersionId': '@@{SOFTWARE_PROF_VERSION_ID}@@',
  'computeProfileId': '@@{COMPUTE_PROF_ID}@@',
  'networkProfileId': '@@{NETWORK_PROF_ID}@@',
  'dbParameterProfileId': '@@{DB_PARAM_ID}@@',
  'createDbserver': True,
  'nodeCount': 1,
  'clustered': False,
  'vmPassword': '@@{DB_SERVER_BASIC.secret}@@',
  'sshPublicKey': '@@{NDB_public_key}@@',
  'autoTuneStagingDrive': True,
  'timeMachineInfo': {
    'name': '@@{calm_application_name}@@_TM',
    'description': 'Time Machine For MySQL Database Provisioned By NCM Self-Service App @@{calm_application_name}@@',
    'slaId': '@@{SLA_ID}@@',
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
      'value': '@@{DB_SIZE}@@'
    },
    {
      'name': 'auto_tune_staging_drive',
      'value': True
    },
    {
      'name': 'db_password',
      'value': '@@{DB_PASS}@@'
    },
    {
      'name': 'database_names',
      'value': '@@{DB_NAME}@@'
    },
    {
      'name': 'dbserver_description',
      'value': 'MySQL Database Server Provisioned By NDB Via NCM Self-Service App @@{calm_application_name}@@'
    }
  ],
  'nodes': [
    {
      'properties': [],
      'vmName': '@@{calm_application_name}@@',
      'networkProfileId': '@@{NETWORK_PROF_ID}@@'
    }
  ]
}

# Make the call and set the response operation ID to the variable
resp = urlreq(url, verb='POST', auth='BASIC', user=era_user, passwd=era_pass, params=json.dumps(payload), headers=headers)
print resp.text
print 'CREATE_OPERATION_ID={0}'.format(json.loads(resp.content)['operationId'])