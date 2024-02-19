import requests
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
print(project_root)

repo = "generic-local"
artifactory = "http://artifactory.emeagso.lab:8082/artifactory/"
url = artifactory + repo
auth = ("admin", "Nutanix/4u!")
file_name = f"{project_root}/test/WindowsServer2019.qcow2"

response = requests.put(url + "/vm_images/windows/" + file_name, auth=auth, data=open(file_name, "rb"))
print('- Response code is {} \n- Response content is {}'.format(response.status_code, response.content))
