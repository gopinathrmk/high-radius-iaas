pc_user ='@@{PC.username}@@'
pc_pwd = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
bp_name_restore = '@@{BP_NAME_RESTORE}@@' 
app_name_restore = '@@{CLONE_INSTANCE_NAME}@@'
domain_name = '@@{domain_name}@@'

#get Bp ID from name
#get Bp detail


url     = "https://{}:9440/api/nutanix/v3/blueprints/list".format(pc_ip)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = { "kind" : "blueprint" }
resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pwd, params=json.dumps(payload), headers=headers)

if not resp.ok:
    print("Couldn't retrieve List of Blueprints !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)

entities = resp_content.get("entities")

bp_uuid_restore = None
for entity in entities:
    if entity["metadata"]["name"] == bp_name_restore:
        bp_uuid_restore = entity["metadata"]["uuid"]
        break

if not bp_uuid_restore:
    print("Restore Blueprint : '{}' is not found ".format(bp_name_restore))
    exit(1)

#url = "https://{}:9440/api/nutanix/v3/blueprints/{}/export_json".format(pc_ip,bp_uuid_restore)
url = "https://{}:9440/api/nutanix/v3/blueprints/{}".format(pc_ip,bp_uuid_restore)

resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pwd, headers=headers)
if not resp.ok:
    print("Couldn't retrieve List of Database_Parameter !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

bp_details = json.loads(resp.content)

del bp_details["status"]

bp_details["spec"].update({
    "app_profile_reference" : { "kind" : "app_profile" },
    "application_name" : app_name_restore
    })

flag=False
for var in bp_details["spec"]["resources"]["app_profile_list"][0]["variable_list"]:
    if var["name"] == "domain_name":
        var["value"] = domain_name
        flag=True
        break

if not flag:
    print("Error in editing the 'domain_name' variable of Restore BP !!! ")
    exit(1)


print("Payload for launching Restore BP\n",bp_details)

url     = "https://{}:9440/api/nutanix/v3/blueprints/{}/launch".format(pc_ip,bp_uuid_restore)
payload = bp_details

resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pwd, params=json.dumps(payload), headers=headers)

if not resp.ok:
    print("Couldn't Launch Restore Blueprint !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)

#Need to add the monitoring status of Second Blueprint











