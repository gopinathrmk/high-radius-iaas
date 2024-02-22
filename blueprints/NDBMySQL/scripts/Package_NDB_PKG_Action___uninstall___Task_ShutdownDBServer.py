user = '@@{PC.username}@@'
password = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{NDB_Service.PC_VM_UUID}@@'

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_shutdown'.format(pc_ip, vm_uuid)
resp = urlreq(url, verb='POST', auth='BASIC', user=user, passwd=password, params=json.dumps({}), verify=False, headers=headers)
if not resp.ok:
    print("Cluster shutdown DB VM")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print('Response Status: ' + str(resp.status_code))
print('Response: ', json.dumps(resp.json()))
print("Cluster Shutdown Successful !! ")

"""
user = '@@{PC.username}@@'
password = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
vm_uuid = '@@{NDB_Service.PC_VM_UUID}@@'

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

url = 'https://{0}:9440/api/nutanix/v3/vms/{1}/acpi_shutdown'.format(pc_ip, vm_uuid)
r = urlreq(url, verb='POST', auth='BASIC', user=user, passwd=password, params=json.dumps({}), verify=False, headers=headers)
print 'Response Status: ' + str(r.status_code)
print 'Response: ', json.dumps(r.json())

"""