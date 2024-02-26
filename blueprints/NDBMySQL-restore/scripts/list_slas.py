# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get List of SLAs
url     = "https://{}:8443/era/v0.9/slas".format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print("Couldn't retrieve List of SLAS !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)
#print(resp_content) #todo torem
slas =[]
for sla in resp_content:
    if sla["name"].lower() != 'none':
        slas.append(sla["uniqueName"])

print(','.join(slas))


