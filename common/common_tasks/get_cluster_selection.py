import requests
from requests.auth import HTTPBasicAuth

def process_request(url, method, user=None, password=None, headers=None, payload=None, secure=False):
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
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'PUT':
                response = requests.put(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'PATCH':
                response = requests.patch(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout
                )
            elif method is 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout
                )

        except requests.exceptions.HTTPError as error_code:
            print ("Http Error!")
            print("status code: {}".format(response.status_code))
            print("reason: {}".format(response.reason))
            print("text: {}".format(response.text))
            print("elapsed: {}".format(response.elapsed))
            #print("headers: {}".format(response.headers))
            #if payload is not None:
            #    print("payload: {}".format(payload))
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

def prism_get_project(api_server,username,secret,project_name=None,project_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given project name.
       If a project_uuid is specified, it will skip retrieving all projects (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        project_name: Name of the project (optional).
        project_uuid: Uuid of the project (optional).
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors

    Returns:
        A string containing the UUID of the Project (project_uuid) and the json content
        of the project details (project)
    """

    project_uuid, project = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="project",entity_api_root="projects",entity_name=project_name,entity_uuid=project_uuid,
                              secure=secure,print_f=print_f)
    return project_uuid, project

def prism_get_cluster(api_server,username,secret,cluster_name,cluster_uuid=None,secure=False):
    """Returns from Prism Central the uuid and details of a given cluster name.
    If a cluster_uuid is specified, it will skip retrieving all clusters (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        cluster_name: Name of the cluster.

    Returns:
        A string containing the UUID of the VM (vm_uuid) and the json content
        of the VM details (vm_details)
    """
    cluster_details = {}

    if cluster_uuid is None:
        #get the list of clusters from Prism Central
        cluster_list = prism_get_clusters(api_server,username,secret)
        for cluster in cluster_list:
            if cluster['spec']['name'] == cluster_name:
                cluster_uuid = cluster['metadata']['uuid']
                cluster_details = cluster.copy()
                break
    else:
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }
        api_server_port = "9440"
        api_server_endpoint = "/api/nutanix/v3/clusters/{0}".format(cluster_uuid)
        url = "https://{}:{}{}".format(
            api_server,
            api_server_port,
            api_server_endpoint
        )
        method = "GET"
        #print("Making a {} API call to {}".format(method, url))
        resp = process_request(url,method,username,secret,headers,secure)
        if resp.ok:
            cluster_details = json.loads(resp.content)
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
            raise

    return cluster_uuid, cluster_details

def prism_get_entity(api_server,username,secret,entity_type,entity_api_root,entity_name=None,entity_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given entity name.
       If an entity_uuid is specified, it will skip retrieving all entities by specifying the uuid in the arguments (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        entity_type: kind (type) of entity as referenced in the entity json object
        entity_api_root: v3 apis root for this entity type. for example. for projects the list api is ".../api/nutanix/v3/projects/list".
                         the entity api root here is "projects"
        entity_name: Name of the entity (optional).
        entity_uuid: Uuid of the entity (optional).
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors

    Returns:
        A string containing the UUID of the entity (entity_uuid) and the json content
        of the entity details (entity_details)
    """

    entity_details = {}

    if entity_uuid is None:
        #get the entities list from Prism
        entity_list = prism_get_entities(api_server=api_server,username=username,secret=secret,
                                          entity_type=entity_type,entity_api_root=entity_api_root,
                                          secure=secure,print_f=print_f)

        for entity in entity_list:
            fetched_name = ""
            if "name" in entity['spec']:
                fetched_name = entity['spec']['name']
            elif "name" in entity['status']:
                fetched_name = entity['status']['name']
            else:
                print("ERROR - fetched entity name could not be extracted for entity {}".format(entity['metadata']['uuid']))
                raise
            if fetched_name == entity_name:
                entity_uuid = entity['metadata']['uuid']
                entity_details = entity.copy()
                break
        if entity_details == {} :
            print("ERROR - Entity {} not found".format(entity_name))
            exit(1)
    else:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        api_server_port = "9440"
        api_server_endpoint = "/api/nutanix/v3/{}/{}".format(entity_api_root,entity_uuid)
        url = "https://{}:{}{}".format(
            api_server,
            api_server_port,
            api_server_endpoint
        )
        method = "GET"
        if print_f:
            #print("Making a {} API call to {} with secure set to {}".format(method, url, secure))
            resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
        if resp.ok:
            entity_details = json.loads(resp.content)
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
            raise
    return entity_uuid, entity_details

def prism_get_entities(api_server,username,secret,entity_type,entity_api_root,secure=False,print_f=True,filter=None):

    """Retrieve the list of entities from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        entity_type: kind (type) of entity as referenced in the entity json object
        entity_api_root: v3 apis root for this entity type. for example. for projects the list api is ".../api/nutanix/v3/projects/list".
                         the entity api root here is "projects"
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search

    Returns:
        An array of entities (entities part of the json response).
    """

    entities = []
    #region prepare the api call
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/{}/list".format(entity_api_root)
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "POST"
    length = 100

    # Compose the json payload
    payload = {
        "kind": entity_type,
        "offset": 0,
        "length": length
    }
    if filter:
        payload["filter"] = filter
    #endregion
    while True:
        if print_f:
            #print("Making a {} API call to {} with secure set to {}".format(method, url, secure))
            resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
        # deal with the result/response
        if resp.ok:
            json_resp = json.loads(resp.content)
            #json_resp = resp
            entities.extend(json_resp['entities'])
            key = 'length'
            if key in json_resp['metadata']:
                if json_resp['metadata']['length'] == length:
                    if print_f:
                        #print("Processing results from {} to {} out of {}".format(
                            # json_resp['metadata']['offset'],
                            # json_resp['metadata']['length']+json_resp['metadata']['offset'],
                            # json_resp['metadata']['total_matches']))
                        payload = {
                            "kind": entity_type,
                            "offset": json_resp['metadata']['length'] + json_resp['metadata']['offset'] + 1,
                            "length": length
                        }
                else:
                    return entities
            else:
                return entities
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
            raise

SELF_SERVICE_ADDRESS = '@@{SELF_SERVICE_ADDRESS}@@'
SELF_SERVICE_USERNAME = '@@{SELF_SERVICE_USERNAME}@@'
SELF_SERVICE_SECRET = '@@{SELF_SERVICE_SECRET}@@'
SELF_SERVICE_SECURE = False

PC_PROVIDER_ADDRESS = "@@{PC_PROVIDER_ADDRESS}@@"
PC_PROVIDER_USERNAME = "@@{PC_PROVIDER_USERNAME}@@"
PC_PROVIDER_SECRET = "@@{PC_PROVIDER_SECRET}@@"
PC_PROVIDER_SECURE = False

CALM_PROJECT_NAME = '@@{PROJECT_NAME}@@'

project_uuid, project = prism_get_project(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,project_name=CALM_PROJECT_NAME,project_uuid=None,secure=SELF_SERVICE_SECURE)

#print("######## Getting cluster info from Prism Central provider ##################")
#print('cluster list is {}'.format(project['spec']['resources']['cluster_reference_list']))
if len(project['spec']['resources']['cluster_reference_list']) > 0:
    cluster_name_list = ['AUTO_SELECT']
    project_cluster_list = project['spec']['resources']['cluster_reference_list']
    for cluster in project_cluster_list:
        prj_cluster_uuid = cluster['uuid']
        cluster_uuid, cluster_data = prism_get_cluster(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,cluster_name=None,cluster_uuid=prj_cluster_uuid,secure=PC_PROVIDER_SECURE)
        cluster_name = cluster_data['spec']['name']
        cluster_name_list.append(cluster_name)

print(",".join(cluster_name_list))