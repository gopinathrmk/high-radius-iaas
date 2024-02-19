# region headers
"""
# escript-template v20190523 / stephane.bourdeaud@nutanix.com
# * author:       marija.jelicic@nutanix.com
# * version:      2024/10/01
# description:    prepares a list of VM names that are part of the given application
"""
# endregion

# region capture Calm macros
app_name = "@@{calm_application_name}@@"
app_vm_list = []
self_service_address = '@@{SELF_SERVICE_ADDRESS}@@'
self_service_username = '@@{SELF_SERVICE_USERNAME}@@'
self_service_secret = '@@{SELF_SERVICE_SECRET}@@'
self_service_secure = False
# endregion

# region prepare variables

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}
# endregion

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

# endregion

# region getting app uuid

calm_app_uuid = "https://{}:9440/api/nutanix/v3/apps/list".format(self_service_address)
payload = {
    "kind": "app",
    "filter": "name == {}".format(app_name)
}

method = 'POST'
resp = process_request(calm_app_uuid, method, self_service_username, self_service_secret, headers, payload, secure=self_service_secure)

if resp.ok:
    result = json.loads(resp.content)
    app_uuid = result["entities"][0]["metadata"]["uuid"]
else:
    exit(1)
# endregion

# region getting app details

calm_app_uuid = "https://{}:9440/api/nutanix/v3/apps/{}".format(self_service_address, app_uuid)
method = 'GET'
resp = process_request(calm_app_uuid, method, self_service_username, self_service_secret, headers, secure=self_service_secure)

if resp.ok:
    result = json.loads(resp.content)
    elements = result["status"]["resources"]["deployment_list"][0]["substrate_configuration"]["element_list"]
    for element in elements:
      app_vm_list.append(element["instance_name"])
else:
    exit(1)
# endregion

app_vm_list = sorted(dict.fromkeys(app_vm_list))
print (",".join(map(str,app_vm_list)))
exit(0)
