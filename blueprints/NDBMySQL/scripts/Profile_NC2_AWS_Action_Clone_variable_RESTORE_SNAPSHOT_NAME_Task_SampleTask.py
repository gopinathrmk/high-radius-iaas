# Set creds and headers

if '@@{RESTORE_TYPE}@@' == 'PITR':
  print 'NA'
  exit(0)

era_ip = '@@{NDB_IP}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Basic {}'.format(base64.b64encode('@@{NDB.username}@@:@@{NDB.secret}@@'.encode()).decode())}

a = ''

# Get the list of SLAs
url ='https://{0}:8443/era/v0.9/tms/@@{NDB_Service.TIME_MACHINE_ID}@@/capability?compute-time-ranges=true&type=detailed&load-db-logs=false&time-zone=Asia/Bangkok&load-sanitised-snapshots=true&load-unknown-timestamp-logs=true&combined-capability=true'.format(era_ip)
resp = urlreq(url, verb='GET', headers=headers)
#print resp.text
for i in resp.json()['databaseCapabilities']['@@{NDB_Service.DB_ID}@@']['capability']:
  if i['snapshots'] is not None:
    for j in i['snapshots']:
      a = '{0}{1}({2}),'.format(a, j['name'], j['dateCreated'])

print a.strip(',')