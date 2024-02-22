era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
sla_name = '@@{SLA}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get the list of SLAs
url     = "https://{}:8443/era/v0.9/slas/name/{}".format(era_ip,sla_name)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print("Couldn't retrieve Detail of SLA : '{}' !!!".format(sla_name))
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)
print("SLA_ID={0}".format(resp_content["id"]))


"""
# Find the desired SLA, and set the corresponding ID to the variable
for sla in json.loads(resp.content):
  if sla['name'] == "@@{SLA}@@":
    print "SLA_ID={0}".format(sla['id'])

"""