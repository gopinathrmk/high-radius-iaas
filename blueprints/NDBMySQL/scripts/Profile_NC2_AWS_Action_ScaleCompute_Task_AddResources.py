era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
pc_user = '@@{PC.username}@@'
pc_pass = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{PC_VM_UUID}@@'
db_entity_name = '@@{DB_ENTITY_NAME}@@'
ram = @@{RAM}@@
cpu = @@{CPU}@@

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

url = "https://{}:8443/era/v0.9/dbservers/{}?value-type=name&detailed=true".format(era_ip,db_entity_name)

resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print("DB Details couldn't be retrieved")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

for prop in resp.json()['properties']:
    if prop['name'] == 'software_home':
        soft_dir = prop['value']
        print('DB_SOFT_DIR={}'.format(soft_dir))


get_headers = {'Accept': 'application/json'}
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, verify=False, headers=get_headers)
if not resp.ok:
    print("VM:{} Details couldn't be retrieved".format(vm_uuid))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print("Response Status: ".format(resp.status_code))
vm_json = resp.json()
print("Response VM Details : {}".format(json.dumps(vm_json)))

del vm_json['status']

if ram > 0: 
    vm_json['spec']['resources']['memory_size_mib'] = int(vm_json['spec']['resources']['memory_size_mib']) + (ram * 1024)
    innodb_pool_size = (int(vm_json['spec']['resources']['memory_size_mib']) * 1024 * 1024) / 2
    print("INNODB_POOL_SIZE={}".format(innodb_pool_size))

if cpu > 0: 
    vm_json['spec']['resources']['num_sockets'] = int(vm_json['spec']['resources']['num_sockets']) + cpu


url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
resp = urlreq(url, verb='PUT', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(vm_json), verify=False, headers=headers)
if not resp.ok:
    print("VM:{} couldn't be updated with new value of RAM/CPU".format(vm_uuid))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print("Response Status: ".format(resp.status_code))
print("DB Server VM is updated wih new values of ram and cpu")



"""
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

url = "https://@@{NDB_IP}@@:8443/era/v0.9/dbservers/@@{DB_ENTITY_NAME}@@?value-type=name&detailed=true"

resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)

for prop in resp.json()['properties']:
    if prop['name'] == 'software_home':
        soft_dir = prop['value']
        print 'DB_SOFT_DIR={}'.format(soft_dir)


user = '@@{PC.username}@@'
password = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{PC_VM_UUID}@@'

get_headers = {'Accept': 'application/json'}
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
r = urlreq(url, verb='GET', auth='BASIC', user=user, passwd=password, verify=False, headers=get_headers)
print 'Response Status: ' + str(r.status_code)
vm_json = r.json()
print 'Response: ' + json.dumps(vm_json)

del vm_json['status']

if @@{RAM}@@ > 0: 
    vm_json['spec']['resources']['memory_size_mib'] = int(vm_json['spec']['resources']['memory_size_mib']) + (@@{RAM}@@ * 1024)
    innodb_pool_size = (int(vm_json['spec']['resources']['memory_size_mib']) * 1024 * 1024) / 2
    print 'INNODB_POOL_SIZE={}'.format(innodb_pool_size)

if @@{CPU}@@ > 0: 
    vm_json['spec']['resources']['num_sockets'] = int(vm_json['spec']['resources']['num_sockets']) + @@{CPU}@@


url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
r = urlreq(url, verb='PUT', auth='BASIC', user=user, passwd=password, params=json.dumps(vm_json), verify=False, headers=headers)
print 'Response Status: ' + str(r.status_code)
print 'Response: ', json.dumps(vm_json)

"""