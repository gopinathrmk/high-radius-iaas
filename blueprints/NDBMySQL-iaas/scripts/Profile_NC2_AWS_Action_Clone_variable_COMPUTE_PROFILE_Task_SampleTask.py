era_ip = '@@{NDB_IP}@@'

url     = "https://" + era_ip + ":8443/era/v0.8/profiles?type=Compute"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic {}'.format(base64.b64encode('@@{NDB.username}@@:@@{NDB.secret}@@'.encode()).decode())}
resp = urlreq(url, verb='GET', headers=headers)
#print "COMPUTE_PROF_ID={0}".format(json.loads(resp.content)['id'])
a = ''
for i in resp.json():
  a = a + i['name'] + ','
print re.sub(',$', '', a)