user = '@@{PC.username}@@'
password = '@@{PC.secret}@@'
ip = 'localhost'
vm_uuid = '@@{PC_VM_UUID}@@'

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

if '@@{POWER_ACTION}@@' == 'Power On':
  
    get_headers = {'Accept': 'application/json'}  
    url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(ip, vm_uuid)
    r = urlreq(url, verb='GET', auth='BASIC', user=user, passwd=password, verify=False, headers=get_headers)
    print 'Response Status: ' + str(r.status_code)
    vm_json = r.json()
    print 'Response: ' + json.dumps(vm_json)
    
    del vm_json['status']

    vm_json['spec']['resources']['power_state'] = 'ON'

    url = 'https://{0}:9440/api/nutanix/v3/vms/{1}'.format(ip, vm_uuid)
    r = urlreq(url, verb='PUT', auth='BASIC', user=user, passwd=password, params=json.dumps(vm_json), verify=False, headers=headers)

else:  

    if '@@{POWER_ACTION}@@' == 'Shutdown':
        url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_shutdown'.format(ip, vm_uuid)
    else:
        url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_reboot'.format(ip, vm_uuid)
        
    r = urlreq(url, verb='POST', auth='BASIC', user=user, passwd=password, params=json.dumps({}), verify=False, headers=headers)
    
print 'Response Status: ' + str(r.status_code)
print 'Response: ', json.dumps(r.json())
