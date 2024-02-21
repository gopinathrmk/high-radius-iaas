user = '@@{PC.username}@@'
password = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{NDB_Service.PC_VM_UUID}@@'

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_shutdown'.format(ip, vm_uuid)
r = urlreq(url, verb='POST', auth='BASIC', user=user, passwd=password, params=json.dumps({}), verify=False, headers=headers)
print 'Response Status: ' + str(r.status_code)
print 'Response: ', json.dumps(r.json())
