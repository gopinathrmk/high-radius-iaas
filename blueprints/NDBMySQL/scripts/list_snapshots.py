era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
restore_type = '@@{RESTORE_TYPE}@@'
time_machine_id = '@@{NDB_Service.TIME_MACHINE_ID}@@'

if restore_type == 'PITR':
    print('NA')
    exit(0)

# Get the list of SLAs
url ='https://{}:8443/era/v0.9/tms/{}/capability?compute-time-ranges=true&type=detailed&load-db-logs=false&time-zone=Asia/Bangkok&load-sanitised-snapshots=true&load-unknown-timestamp-logs=true&combined-capability=true'.format(era_ip,time_machine_id)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if not resp.ok:
    print("Couldn't retrieve List of Snapshots !!!")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

a = ''
#print(resp.json())  #todo torem
for i in resp.json()['databaseCapabilities']['@@{NDB_Service.DB_ID}@@']['capability']:
  if i['snapshots'] is not None:
    for j in i['snapshots']:
      a = '{0}{1}({2}),'.format(a, j['name'], j['dateCreated'])

print(a.strip(','))

