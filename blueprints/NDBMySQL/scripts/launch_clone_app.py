pc_user ='@@{PC.username}@@'
pc_pwd = '@@{PC.secret}@@'
pc_ip = '@@{PC_IP}@@'
bp_name_clone = '@@{BP_NAME_CLONE}@@' 
app_name_clone = '@@{CLONE_INSTANCE_NAME}@@'
domain_name = '@@{domain_name}@@'

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

bp_uuid_clone = None
for entity in entities:
    if entity["metadata"]["name"] == bp_name_clone:
        bp_uuid_clone = entity["metadata"]["uuid"]
        break

if not bp_uuid_clone:
    print("Clone Blueprint : '{}' is not found ".format(bp_name_clone))
    exit(1)

#url = "https://{}:9440/api/nutanix/v3/blueprints/{}/export_json".format(pc_ip,bp_uuid_clone)
url = "https://{}:9440/api/nutanix/v3/blueprints/{}/runtime_editables".format(pc_ip,bp_uuid_clone)

resp = urlreq(url, verb='GET', auth='BASIC', user=pc_user, passwd=pc_pwd, headers=headers)
if not resp.ok:
    print("Couldn't retrieve List of Database_Parameter !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)
app_profile_reference = resp_content["resources"][0]["app_profile_reference"]
runtime_editables = resp_content["resources"][0]["runtime_editables"]

flag=False
for var in runtime_editables["variable_list"]:
    if var["name"] == "domain_name":
        var["value"]["value"] = domain_name
        flag=True
        break

if not flag:
    print("Error in editing the 'domain_name' runtime variable of Clone BP !!! ")
    exit(1)


url     = "https://{}:9440/api/nutanix/v3/blueprints/{}/simple_launch".format(pc_ip,bp_uuid_clone)
payload = {
        "spec": {
            "app_name": app_name_clone,
            "app_description": "",
            "app_profile_reference":app_profile_reference,
            "runtime_editables": runtime_editables
        }
}

print("Payload for launching Clone BP\n",payload)
resp = urlreq(url, verb='POST', auth='BASIC', user=pc_user, passwd=pc_pwd, params=json.dumps(payload), headers=headers)

if not resp.ok:
    print("Couldn't Launch Clone Blueprint !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)
print("Request to launch Clone DB as a separate Application is sent ")

#Need to add the monitoring status of Second Blueprint











