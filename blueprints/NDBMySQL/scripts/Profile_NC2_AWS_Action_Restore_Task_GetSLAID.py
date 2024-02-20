# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get the list of SLAs
url     = "https://{}:8443/era/v0.8/slas".format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)

# Find the desired SLA, and set the corresponding ID to the variable
for sla in json.loads(resp.content):
  if sla['name'] == "@@{SLA}@@":
    print "SLA_ID={0}".format(sla['id'])