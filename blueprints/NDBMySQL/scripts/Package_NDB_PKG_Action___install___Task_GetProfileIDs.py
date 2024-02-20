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