# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
db_entity_name = '@@{calm_application_name}@@'


#Get DB Server IP and ID
url = "https://{}:8443/era/v0.9/clones".format(era_ip)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
params = {'detailed': True, 'value-type':'name', 'value':db_entity_name}
print("Get request to {} with params {}".format(url,params))
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers, params=params)
if not resp.ok:
    print("Clone DB '{}' couldn't be retrieved !!!".format(db_entity_name))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)
print("Response : {}".format(resp_content))
if len(resp_content) == 1:
    db_detail = resp_content[0]
elif len(resp_content) == 0:
    print("Clone '{}' is not found  . Error . Exiting  ".format(db_entity_name))
    exit(1)
else:
    print("More than One clone is returned . Error . Exiting  ")
    exit(1)

db_id = db_detail['id']
tm_id = db_detail['timeMachineId']
db_srv_id = db_detail['databaseNodes'][0]['dbserver']['id']
db_srv_ip = db_detail['databaseNodes'][0]['dbserver']['ipAddresses'][0]
pc_vm_uuid = db_detail['databaseNodes'][0]['dbserver']['vmClusterUuid']
cluster_id = db_detail['databaseNodes'][0]['dbserver']['nxClusterId']

for property in db_detail['properties']:
    if property.get("name") == "db_name":
        db_name = property.get("value")
        break

print("DB_ID={0}".format(db_id))
print("TIME_MACHINE_ID={0}".format(tm_id))
print("DB_SERVER_ID={0}".format(db_srv_id))
print("DB_SERVER_IP={0}".format(db_srv_ip))
print("PC_VM_UUID={0}".format(pc_vm_uuid))
print("CLUSTER_ID={0}".format(cluster_id))
print("DB_NAME={0}".format(db_name))
print("DB_ENTITY_NAME={0}".format(db_entity_name))

