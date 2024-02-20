era_ip = '@@{NDB_IP}@@'

url     = "https://" + era_ip + ":8443/era/v0.9/slas"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic {}'.format(base64.b64encode('@@{NDB.username}@@:@@{NDB.secret}@@'.encode()).decode())}
resp = urlreq(url, verb='GET', headers=headers)

#print "SLA_ID={0}".format(json.loads(resp.content)['id'])
a = ''
for i in resp.json():
  if i['name'].lower() != 'none': 
    a = a + i['name'] + ','
print re.sub(',$', '', a)