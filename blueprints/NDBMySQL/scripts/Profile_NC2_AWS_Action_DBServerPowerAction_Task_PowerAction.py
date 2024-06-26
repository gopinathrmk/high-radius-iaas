user = '@@{PC.username}@@'
password = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{PC_VM_UUID}@@'
power_action = '@@{POWER_ACTION}@@'

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

if power_action == 'Power On':

    get_headers = {'Accept': 'application/json'}  
    url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
    resp = urlreq(url, verb='GET', auth='BASIC', user=user, passwd=password, verify=False, headers=get_headers)
    if not resp.ok:
        print("VM Details couldn't be retrieved for '{}'".format(vm_uuid))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        exit(resp.status_code)    

    print("Response Status: {}".format(resp.status_code))
    vm_json = resp.json()
    print("Response: {}".format(json.dumps(vm_json)))
    
    del vm_json['status']

    vm_json['spec']['resources']['power_state'] = 'ON'

    url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(pc_ip, vm_uuid)
    resp = urlreq(url, verb='PUT', auth='BASIC', user=user, passwd=password, params=json.dumps(vm_json), verify=False, headers=headers)
    if not resp.ok:
        print("VM '{}' Could not power on !!!".format(vm_uuid))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        exit(resp.status_code) 
    print("VM is powered on Successfully ")
else:  
    if power_action == 'Shutdown':
        url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_shutdown'.format(pc_ip, vm_uuid)
    else:
        url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_reboot'.format(pc_ip, vm_uuid)
        
    resp = urlreq(url, verb='POST', auth='BASIC', user=user, passwd=password, params=json.dumps({}), verify=False, headers=headers)
    if not resp.ok:
        print("Vm '{}' Could not {} !!!".format(vm_uuid,power_action))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        exit(resp.status_code)
    print("{} of VM: '{}' is Successfull".format(power_action,vm_uuid))

print("Response Status: {}".format(resp.status_code))
print("Response: {}".format(json.dumps(resp.json())))

