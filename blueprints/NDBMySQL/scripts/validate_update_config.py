era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
pc_user = '@@{PC.username}@@'
pc_pass = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{PC_VM_UUID}@@'
db_entity_name = '@@{DB_ENTITY_NAME}@@'
action = '@@{action}@@'
resource = '@@{resource}@@'
ram = int('@@{RAM}@@')  
cpu = int('@@{CPU}@@')
final_ram = 0
final_socket = 0
#final_cores = 0

if resource == "CPU" and not(cpu>0 ):
    print("Positive values are expected in No of CPU to add/decrease")
    exit(1)
elif resource == "RAM" and not (ram>0):
    print("Positive values are expected in RAM")
    exit(1)
elif resource == "Both" and ( not(cpu>0) or not (ram>0)) :
    print("Positive values are expected in Both Cpu and RAM ")
    exit(1)
else:
    print("Good to proceed")    
    
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
get_headers = {'Accept': 'application/json'}

url = "https://{}:8443/era/v0.9/dbservers/{}?value-type=name&detailed=true".format(era_ip,db_entity_name)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print("DB Details couldn't be retrieved for '{}'".format(db_entity_name))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

soft_dir = ""
for prop in resp.json()['properties']:
    if prop['name'] == 'software_home':
        soft_dir = prop['value']



#Retrieving the current CPU and RAM Values 
url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, verify=False, headers=get_headers)
if not resp.ok:
    print("VM:{} Details couldn't be retrieved".format(vm_uuid))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print("Response Status: {}".format(resp.status_code))
vm_json = resp.json()
print("Response VM Details : {}".format(json.dumps(vm_json)))


current_ram =  int(vm_json['spec']['resources']['memory_size_mib'])
current_socket = int(vm_json['spec']['resources']['num_sockets'])
#current_cores = int(vm_json['spec']['resources']['num_vcpus_per_socket'])
power_state = vm_json['spec']['resources']['power_state']

print("Current config. CPU_SOCKET:'{}', RAM:'{}'GB, Power_state : '{}' ".format(current_socket,current_ram/1024,power_state))

if action == 'Increase':
    final_ram = current_ram + (ram * 1024)
    final_socket = current_socket + cpu
else:
    final_ram = current_ram - (ram * 1024)
    final_socket = current_socket - cpu

innodb_pool_size = (final_ram * 1024 * 1024) / 2 

print("Request Config. CPU_SOCKET:'{}', RAM:'{}'GB, ".format(final_socket,final_ram/1024))

#Validate final values are positive
if (resource == 'RAM' or resource == 'Both') and final_ram <= 0 :
    print("Error !!!.Final RAM Values should be positive post decrease.")
    print("Final State. RAM:'{}'GB".format(final_ram))
    exit(1)

if (resource == 'CPU' or resource == 'Both') and final_socket <= 0 :
    print("Error !!!.Final CPU Values should be positive post decrease.")
    print("Final State. CPU_SOCKET:'{}', ".format(final_socket))
    exit(1)

# Ensure VM is powered-on to add resources. This will not stop post update activity.
# Shutdown of VM for Decrease of Resource
if action == 'Increase' and power_state == 'OFF':
    print("DB server VM must be powered on for increasing the resources")
    exit(1)
elif action == 'Decrease' and power_state == 'ON':
    url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_shutdown'.format(pc_ip, vm_uuid)
    resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps({}), verify=False, headers=headers)
    if not resp.ok:
        print("Vm '{}' Could not Shutdown !!!".format(vm_uuid))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        exit(resp.status_code)
    print("VM Shutdown request Sent prior to config decrease")
    sleep(30)



print('DB_SOFT_DIR={}'.format(soft_dir))
print("INNODB_POOL_SIZE={}".format(innodb_pool_size))
print('FINAL_RAM={}'.format(final_ram))
print('FINAL_SOCKET={}'.format(final_socket))
#print('FINAL_CORES={}'.format(final_cores))
print('resource_service={}'.format(resource))

