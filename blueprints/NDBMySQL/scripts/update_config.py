#power on request is not workig.. due toc concurrent issue
#test others and send email.
pc_user = '@@{PC.username}@@'
pc_pass = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{PC_VM_UUID}@@'
action = '@@{action}@@'
resource = '@@{resource}@@'
final_ram = int('@@{FINAL_RAM}@@')
final_socket = int('@@{FINAL_SOCKET}@@')
#final_cores = int('@@{FINAL_CORES}@@')

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
get_headers = {'Accept': 'application/json'}

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

del vm_json['status']

vm_name = vm_json['spec']['name']
power_state = vm_json['spec']['resources']['power_state']

if resource == 'RAM' or resource == 'Both' :
    vm_json['spec']['resources']['memory_size_mib'] = final_ram
if resource == 'CPU' or resource == 'Both' :
    vm_json['spec']['resources']['num_sockets'] = final_socket
#    vm_json['spec']['resources']['num_vcpus_per_socket'] = final_cores

#Updating CPU and RAM with New Values
url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
resp = urlreq(url, verb='PUT', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(vm_json), verify=False, headers=headers)
if not resp.ok:
    print("VM:{} couldn't be updated with new value of RAM/CPU".format(vm_name))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print("Response Status: {}".format(resp.status_code))
print("Response Details: {}".format(resp.json()))
print("DB Server VM is updated wih new values of ram and cpu")

sleep(30)

#power ON VM in case of Decrease 
print("VM power state is {}".format(power_state)) #todo torem
if action == 'Decrease' and power_state == 'OFF':

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

    del vm_json['status']

    vm_json['spec']['resources']['power_state'] = 'ON'
    url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
    resp = urlreq(url, verb='PUT', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(vm_json), verify=False, headers=headers)
    if not resp.ok:
        print("VM '{}' Could not power on !!!".format(vm_uuid))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        exit(resp.status_code) 
    print("VM is powered on Successfully ")
    

