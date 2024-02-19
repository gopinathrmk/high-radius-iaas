# region headers
"""
# escript-template v20190523 / stephane.bourdeaud@nutanix.com
# * author:       marija.jelicic@nutanix.com
# * version:      2024/08/01
# task_name:      cloneVM
# description:    This script clones VM with disabled network adapters.
"""
# endregion

# region capture Calm macros
app_uuid = "@@{calm_application_uuid}@@"
vm_replica_name = "@@{name}@@"
vm_name = "@@{VM_NAME}@@"

self_service_address = '@@{SELF_SERVICE_ADDRESS}@@'
self_service_username = '@@{SELF_SERVICE_USERNAME}@@'
self_service_secret = '@@{SELF_SERVICE_SECRET}@@'
self_service_secure = False

pc_provider_address = '@@{PC_PROVIDER_ADDRESS}@@'
pc_provder_username = '@@{PC_PROVIDER_USERNAME}@@'
pc_provder_secret = '@@{PC_PROVIDER_SECRET}@@'
pc_provder_secure = False

# endregion

# region prepare variables

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}
# endregion

if vm_name is not vm_replica_name:
    print ("Clone not needed for vm {}, skipping...").format(vm_replica_name)
    exit (0)


# region functions
import requests

def process_request(url, method, user, password, headers, payload=None, secure=False):
    """
    Processes a web request and handles result appropriately with retries.
    Returns the content of the web request if successfull.
    """
    if payload is not None:
        payload = json.dumps(payload)

    #configuring web request behavior
    timeout=10
    retries = 5
    sleep_between_retries = 5

    while retries > 0:
        try:

            if method is 'GET':
                response = requests.get(
                    url,
                    headers=headers,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'PUT':
                response = requests.put(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'PATCH':
                response = requests.patch(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )

        except requests.exceptions.HTTPError as error_code:
            print ("Http Error!")
            print("status code: {}".format(response.status_code))
            print("reason: {}".format(response.reason))
            print("text: {}".format(response.text))
            print("elapsed: {}".format(response.elapsed))
            print("headers: {}".format(response.headers))
            if payload is not None:
                print("payload: {}".format(payload))
            print(json.dumps(
                json.loads(response.content),
                indent=4
            ))
            exit(response.status_code)
        except requests.exceptions.ConnectionError as error_code:
            print ("Connection Error!")
            if retries == 1:
                print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
                exit(1)
            else:
                print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
                sleep(sleep_between_retries)
                retries -= 1
                print ("retries left: {}".format(retries))
                continue
            print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
            exit(1)
        except requests.exceptions.Timeout as error_code:
            print ("Timeout Error!")
            if retries == 1:
                print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
                exit(1)
            print('Error! Code: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
            sleep(sleep_between_retries)
            retries -= 1
            print ("retries left: {}".format(retries))
            continue
        except requests.exceptions.RequestException as error_code:
            print ("Error!")
            exit(response.status_code)
        break

    if response.ok:
        return response
    if response.status_code == 401:
        print("status code: {0}".format(response.status_code))
        print("reason: {0}".format(response.reason))
        exit(response.status_code)
    elif response.status_code == 500:
        print("status code: {0}".format(response.status_code))
        print("reason: {0}".format(response.reason))
        print("text: {0}".format(response.text))
        exit(response.status_code)
    else:
        print("Request failed!")
        print("status code: {0}".format(response.status_code))
        print("reason: {0}".format(response.reason))
        print("text: {0}".format(response.text))
        print("raise_for_status: {0}".format(response.raise_for_status()))
        print("elapsed: {0}".format(response.elapsed))
        print("headers: {0}".format(response.headers))
        if payload is not None:
            print("payload: {0}".format(payload))
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        exit(response.status_code)

def prism_monitor_task_apiv3(api_server,username,secret,task_uuid,secure=False):

    """Given a Prism Central task uuid, loop until the task is completed
    exits if the task fails

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        task_uuid: Prism Central task uuid (generally returned by another action 
                   performed on PC).
        secure: boolean to verify or not the api server's certificate (True/False)
                   
    Returns:
        No value is returned
    """
    
    task_status_details = {}
    task_status = "RUNNING"

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/tasks/{0}".format(task_uuid)
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    print("Making a {} API call to {}".format(method, url))
    
    while True:
        resp = process_request(url,method,user=username,password=secret,headers=headers,secure=secure)
        #print(json.loads(resp.content))
        if resp.ok:
            task_status_details = json.loads(resp.content)
            task_status = resp.json()['status']
            if task_status == "SUCCEEDED":
                print ("Task has completed successfully")
                return task_status_details
            elif task_status == "FAILED":
                print ("Task has failed: {}".format(   resp.json()['error_detail'] if 'error_detail' in resp.json() else "No Info" )       )
                exit(1)
            else:
                print ("Task status is {} and percentage completion is {}. Current step is {}. Waiting for 30 seconds.".format(task_status,resp.json()['percentage_complete'],resp.json()['progress_message']))
                sleep(30)
        else:
            print("Request failed!")
            print("status code: {}".format(resp.status_code))
            print("reason: {}".format(resp.reason))
            print("text: {}".format(resp.text))
            print("raise_for_status: {}".format(resp.raise_for_status()))
            print("elapsed: {}".format(resp.elapsed))
            print("headers: {}".format(resp.headers))
            print("payload: {}".format(payload))
            print(json.dumps(
                json.loads(resp.content),
                indent=4
            ))
            exit(resp.status_code)

    return task_status_details
# endregion

# region getting app details

calm_app_uuid_url = "https://{}:9440/api/nutanix/v3/apps/{}".format(self_service_address, app_uuid)
method = 'GET'
print("Getting app details...")
print("Making a {} API call to {}".format(method, calm_app_uuid_url))

resp = process_request(calm_app_uuid_url, method, self_service_username, self_service_secret, headers, self_service_secure)

if resp.ok:
    result = json.loads(resp.content)
    # print the content of the response
    # print(json.dumps(
    #     json.loads(resp.content),
    #     indent=4
    # ))
    elements = result["status"]["resources"]["deployment_list"][0]["substrate_configuration"]["element_list"]
    #print "elemnts: {}".format(elements)
    for element in elements:
      if element["instance_name"] == vm_name:
         vm_uuid = element["instance_id"]
         vm_nic_list = element["create_spec"]["resources"]["nic_list"]
         #print element["create_spec"]["resources"]["nic_list"][0]["subnet_reference"]["uuid"]
    #print("VM uuid is {}".format(vm_uuid))
else:
    exit(1)
# endregion

# region clone VM
method = 'POST'
clone_vm_url = "https://{}:9440/api/nutanix/v3/vms/{}/clone".format(pc_provider_address, vm_uuid)
print("Clonig VM...")
print("Making a {} API call to {}".format(method, clone_vm_url))

nic_list = []
for nic in vm_nic_list:
  subnet_reference = {
                "is_connected": False,
                "subnet_reference": {
                    "uuid": "{}".format(nic["subnet_reference"]["uuid"]),
                    "kind": "subnet"
                }
            }
  nic_list.append(subnet_reference)
  
payload = {
    "override_spec": {
        "name": vm_name + "-clone-@@{calm_now}@@",
        "nic_list": nic_list
    }
}
resp = process_request(clone_vm_url, method, self_service_username, pc_provder_secret, headers, payload, pc_provder_secure)

if resp.status_code == 202:
    result = resp.json()
    task_uuid = result["task_uuid"]
    print('INFO - task: {}'.format(task_uuid))
    prism_monitor_task_apiv3(api_server=pc_provider_address,username=pc_provder_username,secret=pc_provder_secret,secure=pc_provder_secure,task_uuid=task_uuid)

else:
    print('ERROR - cloning VM failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
    exit(1)

