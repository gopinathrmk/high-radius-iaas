# Set creds and headers
era_user = '@@{NDB.username}@@'
era_pass = '@@{NDB.secret}@@'
era_ip = '@@{NDB_IP}@@'
cluster_name = '@@{cluster_name}@@'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

#Get Cluster by Name :
url     = "https://{}:8443/era/v0.8/clusters/name/{}/".format(era_ip,cluster_name)
resp = urlreq(url, verb='GET', auth='BASIC', user=era_user, passwd=era_pass, headers=headers)

if not resp.ok:
    print("Cluster ID couldn't be retrieved")
    print(u"status code: {0}".format(resp.status_code))
    print(u"reason: {0}".format(resp.reason))
    print(u"text: {0}".format(resp.text))
    exit(resp.status_code)

cluster_detail = json.loads(resp.content)
print ("CLUSTER_ID={0}".format(cluster_detail["id"]))

