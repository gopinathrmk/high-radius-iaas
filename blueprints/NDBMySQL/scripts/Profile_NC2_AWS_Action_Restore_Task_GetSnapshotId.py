if '@@{RESTORE_TYPE}@@' == 'PITR':
  print "DB_SNAPSHOT_ID=NA"
  exit(0)

# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

db_snapshot_name = '@@{RESTORE_SNAPSHOT_NAME}@@'.split('(')[0]
db_snapshot_date = '@@{RESTORE_SNAPSHOT_NAME}@@'.split('(')[1].strip(')')

# Get the list of SLAs
url ='https://{0}:8443/era/v0.9/tms/@@{TIME_MACHINE_ID}@@/capability?compute-time-ranges=true&type=detailed&load-db-logs=false&time-zone=Asia/Bangkok&load-sanitised-snapshots=true&load-unknown-timestamp-logs=true&combined-capability=true'.format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
#print resp.text
for i in resp.json()['databaseCapabilities']['@@{DB_ID}@@']['capability']:
  if i['snapshots'] is not None:
    for j in i['snapshots']:
      if j['name'] == db_snapshot_name and j['dateCreated'] == db_snapshot_date:
        print "DB_SNAPSHOT_ID={0}".format(j['id'])