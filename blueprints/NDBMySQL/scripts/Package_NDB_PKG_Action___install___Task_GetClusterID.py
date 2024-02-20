# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
cluster_name = '@@{cluster_name}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Get Cluster ID
#url     = "https://{}:8443/era/v0.8/clusters".format(era_ip)
#resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
#print "CLUSTER_ID={0}".format(json.loads(resp.content)[0]['id'])
#print "CLUSTER_ID={0}".format(json.loads(resp.content)[0]['id'])

#Get Cluster by Name :

url     = "https://{}:8443/era/v0.8/clusters/name/{}/".format(era_ip,cluster_name)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)
resp_content = json.loads(resp.content)
#print(resp_content)

print "CLUSTER_ID={0}".format(resp_content["id"])








