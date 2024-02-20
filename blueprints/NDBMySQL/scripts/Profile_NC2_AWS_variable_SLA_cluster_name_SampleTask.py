# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Cluster ID
url     = "https://{}:8443/era/v0.8/clusters".format(era_ip)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
if resp.ok:
    resp_content = json.loads(resp.content)
else:
    print("Error in retreiving Cluster Details !!!")
    exit(0)
#print "CLUSTER_ID={0}".format(json.loads(resp.content)[0]['id'])

clusters =[]
for cluster in resp_content:
    clusters.append(cluster["uniqueName"])

print(','.join(clusters))
