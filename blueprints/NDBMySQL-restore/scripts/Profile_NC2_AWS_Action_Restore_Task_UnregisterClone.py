import requests

era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
clone_instance_name = '@@{CLONE_INSTANCE_NAME}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
url = "https://{}:8443/era/v0.9/clones/{}?value-type=name".format(era_ip,clone_instance_name)

resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print("Couldn't retrieve details of Clone : '{}' !!!".format(clone_instance_name))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

clone_id = resp.json()['id']

url = "https://{}:8443/era/v0.9/clones/{}".format(era_ip,clone_id)

data = {
  "softRemove": False,
  "remove": True,
  "delete": False,
  "forced": False,
  "deleteLogicalCluster": True,
  "removeLogicalCluster": False,
  "deleteTimeMachine": True
}

requests.packages.urllib3.disable_warnings()
resp = requests.request("DELETE", url, json=data, headers=headers, verify=False, auth=(era_user, era_pass))
if not resp.ok:
    print("Couldn't UnRegister Clone : '{}' !!!".format(clone_instance_name))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

print(resp.status_code)
print(resp.text)
print("CLEANUP_OPERATION_ID={0}".format(resp.json()['operationId']))

