# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

soft_profile = '@@{SOFT_PROFILE}@@'
compute_profile = '@@{COMPUTE_PROFILE}@@'
network_profile = '@@{NETWORK_PROFILE}@@'
db_parameters = '@@{DB_PARAMETERS}@@'

#Api Call to get Profile Details
def get_profile(params):
    url = "https://{}:8443/era/v0.8/profiles".format(era_ip)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers, params=params)
    if not resp.ok:
        print("Couldn't retrieve details of {} Profile: '{}' !!!".format(params["type"], params["name"]))
        print(u"status code: {0}".format(resp.status_code))
        print(u"reason: {0}".format(resp.reason))
        print(u"text: {0}".format(resp.text))
        exit(resp.status_code)
    return resp

# Get Software Profile ID
params = {'type':'Software', 'name':soft_profile}
resp = get_profile(params=params)
resp_content = json.loads(resp.content)
print("SOFTWARE_PROF_ID={0}".format(resp_content['id']))
print("SOFTWARE_PROF_VERSION_ID={0}".format(resp_content['latestVersionId']))

#Get Compute Profile ID
params = {'type':'Compute', 'name':compute_profile}
resp = get_profile(params=params)
resp_content = json.loads(resp.content)
print("COMPUTE_PROF_ID={0}".format(resp_content['id']))

#Get Network Profile ID
params = {'type':'Network', 'name':network_profile}
resp = get_profile(params=params)
resp_content = json.loads(resp.content)
print("NETWORK_PROF_ID={0}".format(resp_content['id']))

#Get DB Parameter ID
params = {'type':'Database_Parameter', 'name':db_parameters}
resp = get_profile(params=params)
resp_content = json.loads(resp.content)
print("DB_PARAM_ID={0}".format(resp_content['id']))


"""
# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'


headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Software Profile ID
url     = "https://{}:8443/era/v0.8/profiles?type=Software&name=@@{SOFT_PROFILE}@@".format(era_ip)

resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
print "SOFTWARE_PROF_ID={0}".format(json.loads(resp.content)['id'])
print "SOFTWARE_PROF_VERSION_ID={0}".format(json.loads(resp.content)['latestVersionId'])

# Get Compute Profile ID
url     = "https://{}:8443/era/v0.8/profiles?type=Compute&name=@@{COMPUTE_PROFILE}@@".format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
print "COMPUTE_PROF_ID={0}".format(json.loads(resp.content)['id'])

# Get Compute Profile ID
url     = "https://{}:8443/era/v0.8/profiles?type=Network&name=@@{NETWORK_PROFILE}@@".format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
print "NETWORK_PROF_ID={0}".format(json.loads(resp.content)['id'])

# Get Compute Profile ID
url     = "https://{}:8443/era/v0.8/profiles?type=Database_Parameter&name=@@{DB_PARAMETERS}@@".format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
print "DB_PARAM_ID={0}".format(json.loads(resp.content)['id'])
"""