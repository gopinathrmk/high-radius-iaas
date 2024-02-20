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
ip = 'localhost'
vm_uuid = '@@{PC_VM_UUID}@@'

get_headers = {'Accept': 'application/json'}
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(ip, vm_uuid)
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


url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(ip, vm_uuid)
r = urlreq(url, verb='PUT', auth='BASIC', user=user, passwd=password, params=json.dumps(vm_json), verify=False, headers=headers)
print 'Response Status: ' + str(r.status_code)
print 'Response: ', json.dumps(vm_json)

