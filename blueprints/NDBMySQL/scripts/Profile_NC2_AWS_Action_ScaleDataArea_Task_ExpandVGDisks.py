pc_vm_uuid = '@@{PC_VM_UUID}@@'
pc_user = '@@{PC.username}@@'
pc_pass = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
disk_size = @@{DISK}@@

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = "https://{}:9440/api/nutanix/v3/vms/{}".format(pc_ip,pc_vm_uuid)

resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)

if not resp.ok:
    print("VM Details couldn't be retrieved")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

for disk in resp.json()['spec']['resources']['disk_list']:
    if disk['device_properties']['device_type'] == 'VOLUME_GROUP':
        vg_uuid = disk['volume_group_reference']['uuid']
        url = "https://{}:9440/api/storage/v4.0.a4/config/volume-groups/{}".format(pc_ip,vg_uuid)
        resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)
        if not resp.ok:
            print("VG Details couldn't be retrieved")
            print(u"status code: {0}".format(resp.status_code))
            print(u"reason: {0}".format(resp.reason))
            print(u"text: {0}".format(resp.text))
            exit(resp.status_code)


        if 'DG_VG' in resp.json()['data']['name']:
            print('Expand Disks For VG ' + resp.json()['data']['name'])
            url = "https://{}:9440/api/storage/v4.0.a4/config/volume-groups/{}/disks".format(pc_ip,vg_uuid)
            resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)
            if not resp.ok:
                print("VG Details couldn't be retrieved")
                print(u"status code: {0}".format(resp.status_code))
                print(u"reason: {0}".format(resp.reason))
                print(u"text: {0}".format(resp.text))
                exit(resp.status_code)           

            disk_nos = len(resp.json()['data'])
            total_add_bytes = disk_size * 1024 * 1024 * 1024
            add_per_disk = total_add_bytes / disk_nos    
            
            for count, vg_disk in enumerate(resp.json()['data']):
                print('Expand Disk {}'.format(count))
                            
                vg_disk_id = vg_disk['extId']
                
                url = "https://{}:9440/api/storage/v4.0.a4/config/volume-groups/{}/disks/{}".format(pc_ip,vg_uuid, vg_disk_id)
                resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)               
                if not resp.ok:
                    print("Disk Details couldn't be retrieved")
                    print(u"status code: {0}".format(resp.status_code))
                    print(u"reason: {0}".format(resp.reason))
                    print(u"text: {0}".format(resp.text))
                    exit(resp.status_code)                  
                payload = {
                    'diskSizeBytes': resp.json()['data']['diskSizeBytes'] + add_per_disk,
                    'extId': vg_disk_id,
                    '$reserved': {
                        '$fqObjectType': 'storage.v4.r0.a4.config.VolumeDisk',
                        'ETag': resp.headers['ETag']
                     },
                    '$objectType': 'storage.v4.config.VolumeDisk'
                }
                
                generated_uuid = uuid.uuid4()
                
                formatted_string = "{}-{}-{}-{}-{}".format(
                    generated_uuid.hex[:8],
                    generated_uuid.hex[8:12],
                    generated_uuid.hex[12:16],
                    generated_uuid.hex[16:20],
                    generated_uuid.hex[20:]
                )
                
                patch_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'If-Match': resp.headers['ETag'], 'Ntnx-Request-Id': formatted_string}
                
                resp = urlreq(url, verb='PATCH', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=patch_headers)
                if not resp.ok:
                    print("Disk Details couldn't be retrieved")
                    print(u"status code: {0}".format(resp.status_code))
                    print(u"reason: {0}".format(resp.reason))
                    print(u"text: {0}".format(resp.text))
                    exit(resp.status_code) 

                print('Response: ' + json.dumps(resp.status_code))



"""
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

pc_vm_uuid = '@@{PC_VM_UUID}@@'
pc_user = '@@{PC.username}@@'
pc_pass = '@@{PC.secret}@@'

url = "https://localhost:9440/api/nutanix/v3/vms/{}".format(pc_vm_uuid)
resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)

for disk in resp.json()['spec']['resources']['disk_list']:
    if disk['device_properties']['device_type'] == 'VOLUME_GROUP':
        vg_uuid = disk['volume_group_reference']['uuid']
        url = "https://localhost:9440/api/storage/v4.0.a4/config/volume-groups/{}".format(vg_uuid)
        resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)
        if 'DG_VG' in resp.json()['data']['name']:
            print 'Expand Disks For VG ' + resp.json()['data']['name']
            url = "https://localhost:9440/api/storage/v4.0.a4/config/volume-groups/{}/disks".format(vg_uuid)
            resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)
            
            disk_nos = len(resp.json()['data'])
            total_add_bytes = @@{DISK}@@ * 1024 * 1024 * 1024
            add_per_disk = total_add_bytes / disk_nos    
            
            for count, vg_disk in enumerate(resp.json()['data']):
                print 'Expand Disk {}'.format(count)
                            
                vg_disk_id = vg_disk['extId']
                
                url = "https://localhost:9440/api/storage/v4.0.a4/config/volume-groups/{}/disks/{}".format(vg_uuid, vg_disk_id)
                resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pass, headers=headers)               
                
                payload = {
                    'diskSizeBytes': resp.json()['data']['diskSizeBytes'] + add_per_disk,
                    'extId': vg_disk_id,
                    '$reserved': {
                        '$fqObjectType': 'storage.v4.r0.a4.config.VolumeDisk',
                        'ETag': resp.headers['ETag']
                     },
                    '$objectType': 'storage.v4.config.VolumeDisk'
                }
                
                generated_uuid = uuid.uuid4()
                
                formatted_string = "{}-{}-{}-{}-{}".format(
                    generated_uuid.hex[:8],
                    generated_uuid.hex[8:12],
                    generated_uuid.hex[12:16],
                    generated_uuid.hex[16:20],
                    generated_uuid.hex[20:]
                )
                
                patch_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'If-Match': resp.headers['ETag'], 'Ntnx-Request-Id': formatted_string}
                
                resp = urlreq(url, verb='PATCH', auth='BASIC', user=pc_user, passwd=pc_pass, params=json.dumps(payload), headers=patch_headers)
                print 'Response: ' + json.dumps(resp.status_code)

                
"""        

