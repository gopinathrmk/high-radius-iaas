import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime
from pprint import pprint

artifactory = "http://artifactory.emeagso.lab:8082/artifactory/"
api = "api/repositories/generic-local"
url = artifactory + api
auth = ("admin", "Nutanix/4u!")

# Note: method_whitelist parameter is marked for eventual deprecation - to be replaced with allowed_methods (but not available here yet)
retry_strategy = Retry(total=7, backoff_factor=1, status_forcelist=[403, 404, 413, 429, 500, 501, 502, 503], allowed_methods=set({'GET','POST'}))
sess = requests.Session()
sess.mount('https://', HTTPAdapter(max_retries=retry_strategy))
sess.mount('http://', HTTPAdapter(max_retries=retry_strategy))

response = sess.get(url, auth=auth, verify=False)
data = response.json()
#response = requests.get(url, auth=auth)
pprint('- Response code is {} \n- Response content is {}'.format(response.status_code, data))