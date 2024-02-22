import requests
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
sla_id = '@@{SLA_ID}@@'
clone_instance_name = '@@{CLONE_INSTANCE_NAME}@@'
calm_application_name = '@@{calm_application_name}@@'
db_name = '@@{DB_NAME}@@'
clone_root_pass = '@@{CLONE_ROOT_PASS}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = "https://{}:8443/era/v0.9/dbservers/{}?value-type=name&detailed=true".format(era_ip,clone_instance_name)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print("DB Server IP couldn't be retreived !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)


vm_ip = resp.json()['ipAddresses'][0]

for prop in resp.json()['properties']:
    if prop['name'] == 'software_home':
        soft_dir = prop['value']

url = "https://{}:8443/era/v0.9/databases/register".format(era_ip)

data = {
  "actionArguments": [
    {
      "name": "listener_port",
      "value": "3306"
    },
    {
      "name": "db_user",
      "value": "root"
    },
    {
      "name": "backup_policy",
      "value": "primary_only"
    },
    {
      "name": "software_home",
      "value": soft_dir
    },
    {
      "name": "db_name",
      "value": db_name
    },
    {
      "name": "db_password",
      "value": clone_root_pass
    }
  ],
  "databaseType": "mysql_database",
  "databaseName": clone_instance_name,
  "description": "Restored DB {} For MySQL Database {} Provisioned By NCM Self-Service App {}".format(clone_instance_name,calm_application_name,calm_application_name),
  "clustered": False,
  "forcedInstall": True,
  "category": "DEFAULT",
  "vmIp": vm_ip,
  "vmUsername": "",
  "vmPassword": "",
  "vmSshkey": "",
  "vmDescription": "",
  "resetDescriptionInNxCluster": False,
  "autoTuneStagingDrive": True,
  "workingDirectory": "/tmp",
  "timeMachineInfo": {
    "autoTuneLogDrive": True,
    "slaId": sla_id,
    "schedule": {
      "snapshotTimeOfDay": {
        "hours": 1,
        "minutes": 0,
        "seconds": 0
      },
      "continuousSchedule": {
        "enabled": True,
        "logBackupInterval": 30,
        "snapshotsPerDay": 1
      },
      "weeklySchedule": {
        "enabled": True,
        "dayOfWeek": "SUNDAY"
      },
      "monthlySchedule": {
        "enabled": True,
        "dayOfMonth": "19"
      },
      "quartelySchedule": {
        "enabled": True,
        "startMonth": "JANUARY",
        "dayOfMonth": "19"
      },
      "yearlySchedule": {
        "enabled": False,
        "dayOfMonth": 31,
        "month": "DECEMBER"
      }
    },
    "tags": [],
    "name": clone_instance_name + "_TM",
    "description": "Time Machine For Restored DB {} Provisioned By NCM Self-Service App {}".format(clone_instance_name,calm_application_name)
  },
  "tags": []
}



print(json.dumps(data))

requests.packages.urllib3.disable_warnings()
resp = requests.request("POST", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))
if not resp.ok:
    print("Clone Operation request is not accepted !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print(resp.status_code)
print(resp.text)
print("Register Operation request is sent")
print("REGISTER_OPERATION_ID={0}".format(resp.json()['operationId']))

"""
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

url = "https://@@{NDB_IP}@@:8443/era/v0.9/dbservers/@@{CLONE_INSTANCE_NAME}@@?value-type=name&detailed=true"

resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)

vm_ip = resp.json()['ipAddresses'][0]

for prop in resp.json()['properties']:
    if prop['name'] == 'software_home':
        soft_dir = prop['value']

url = "https://@@{NDB_IP}@@:8443/era/v0.9/databases/register"

data = {
  "actionArguments": [
    {
      "name": "listener_port",
      "value": "3306"
    },
    {
      "name": "db_user",
      "value": "root"
    },
    {
      "name": "backup_policy",
      "value": "primary_only"
    },
    {
      "name": "software_home",
      "value": soft_dir
    },
    {
      "name": "db_name",
      "value": "@@{DB_NAME}@@"
    },
    {
      "name": "db_password",
      "value": "@@{CLONE_ROOT_PASS}@@"
    }
  ],
  "databaseType": "mysql_database",
  "databaseName": "@@{CLONE_INSTANCE_NAME}@@",
  "description": "Restored DB @@{CLONE_INSTANCE_NAME}@@ For MySQL Database @@{calm_application_name}@@ Provisioned By NCM Self-Service App @@{calm_application_name}@@",
  "clustered": False,
  "forcedInstall": True,
  "category": "DEFAULT",
  "vmIp": vm_ip,
  "vmUsername": "",
  "vmPassword": "",
  "vmSshkey": "",
  "vmDescription": "",
  "resetDescriptionInNxCluster": False,
  "autoTuneStagingDrive": True,
  "workingDirectory": "/tmp",
  "timeMachineInfo": {
    "autoTuneLogDrive": True,
    "slaId": "@@{SLA_ID}@@",
    "schedule": {
      "snapshotTimeOfDay": {
        "hours": 1,
        "minutes": 0,
        "seconds": 0
      },
      "continuousSchedule": {
        "enabled": True,
        "logBackupInterval": 30,
        "snapshotsPerDay": 1
      },
      "weeklySchedule": {
        "enabled": True,
        "dayOfWeek": "SUNDAY"
      },
      "monthlySchedule": {
        "enabled": True,
        "dayOfMonth": "19"
      },
      "quartelySchedule": {
        "enabled": True,
        "startMonth": "JANUARY",
        "dayOfMonth": "19"
      },
      "yearlySchedule": {
        "enabled": False,
        "dayOfMonth": 31,
        "month": "DECEMBER"
      }
    },
    "tags": [],
    "name": "@@{CLONE_INSTANCE_NAME}@@_TM",
    "description": "Time Machine For Restored DB @@{CLONE_INSTANCE_NAME}@@ Provisioned By NCM Self-Service App @@{calm_application_name}@@"
  },
  "tags": []
}

import requests

print json.dumps(data)

requests.packages.urllib3.disable_warnings()
response = requests.request("POST", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))
print(response.status_code)
print(response.text)
print "REGISTER_OPERATION_ID={0}".format(response.json()['operationId'])
"""