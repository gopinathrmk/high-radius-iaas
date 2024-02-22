era_ip = '@@{NDB_IP}@@'

url     = "https://" + era_ip + ":8443/era/v0.8/profiles?type=Database_Parameter"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic {}'.format(base64.b64encode('@@{NDB.username}@@:@@{NDB.secret}@@'.encode()).decode())}
resp = urlreq(url, verb='GET', headers=headers)

#print "DATABASE_PARAM_ID={0}".format(json.loads(resp.content)['id'])
a = ''
for i in resp.json():
  if i['engineType'] == 'mysql_database':
    a = a + i['name'] + ','
print re.sub(',$', '', a)