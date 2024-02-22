# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
params = {'type':'Software'}

# Get List of Software Profiles
url     = "https://{}:8443/era/v0.8/profiles".format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers, params=params)
if not resp.ok:
    print("Couldn't retrieve List of Software !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

resp_content = json.loads(resp.content)
#print(resp_content) #todo torem
profiles =[]
for profile in resp_content:
    if profile["engineType"] == 'mysql_database':
        profiles.append(profile["name"])

print(','.join(profiles))

