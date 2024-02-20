# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
db_entity_name = '@@{DB_ENTITY_NAME}@@'


#Get SB Server Details
url = "https://{}:8443/era/v0.9/databases".format(era_ip)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
params = {'detailed': True, 'value-type':'name', 'value':db_entity_name}
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers, params=params)
if not resp.ok:
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)
db_id = resp.content['id']
tm_id = resp.content['timeMachineId']
db_srv_id = resp.content['databaseNodes'][0]['dbserver']['id']
db_srv_ip = resp.content['databaseNodes'][0]['dbserver']['ipAddresses'][0]
pc_vm_uuid = resp.content['databaseNodes'][0]['dbserver']['vmClusterUuid']

print("DB_ID={0}".format(db_id))
print("TIME_MACHINE_ID={0}".format(tm_id))
print("DB_SERVER_ID={0}".format(db_srv_id))
print("DB_SERVER_IP={0}".format(db_srv_ip))
print("PC_VM_UUID={0}".format(pc_vm_uuid))




"""
# Get DB Server IP and ID
url = "https://@@{NDB_IP}@@:8443/era/v0.9/databases/@@{DB_ENTITY_NAME}@@?detailed=true&value-type=name"
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

db_id = resp.json()['id']
tm_id = resp.json()['timeMachineId']
db_srv_id = resp.json()['databaseNodes'][0]['dbserver']['id']
db_srv_ip = resp.json()['databaseNodes'][0]['dbserver']['ipAddresses'][0]
pc_vm_uuid = resp.json()['databaseNodes'][0]['dbserver']['vmClusterUuid']

print "DB_ID={0}".format(db_id)
print "TIME_MACHINE_ID={0}".format(tm_id)
print "DB_SERVER_ID={0}".format(db_srv_id)
print "DB_SERVER_IP={0}".format(db_srv_ip)
print "PC_VM_UUID={0}".format(pc_vm_uuid)
"""