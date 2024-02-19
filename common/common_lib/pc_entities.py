########################################################################
############       pc_entities.py                           ############
########################################################################
# CALM_USES http_requests.py


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
            print("Making a {} API call to {} with secure set to {}".format(method, url, secure))
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
                        print("Processing results from {} to {} out of {}".format(
                            json_resp['metadata']['offset'], 
                            json_resp['metadata']['length']+json_resp['metadata']['offset'],
                            json_resp['metadata']['total_matches']))
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
            print("Making a {} API call to {} with secure set to {}".format(method, url, secure))
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


def prism_get_entity_uuid(api_server,username,secret,entity_type,entity_api_root,entity_name=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid of a given entity name.
       
    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        entity_type: kind (type) of entity as referenced in the entity json object
        entity_api_root: v3 apis root for this entity type. for example. for projects the list api is ".../api/nutanix/v3/projects/list".
                         the entity api root here is "projects"
        entity_name: Name of the entity 
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the entity (entity_uuid) and the json content
        of the entity details (entity_details)
    """
    
    #get the entities list from Prism
    entity_list = prism_get_entities(api_server=api_server,username=username,secret=secret,
                                        entity_type=entity_type,entity_api_root=entity_api_root,
                                        secure=secure,print_f=print_f)
    entity_uuid = None
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
            break
    if entity_uuid is None:
        print("Error: Enitity ID could not be retrieved for entity '{}' of kind '{}'".format(entity_name,entity_type))
        raise
    return entity_uuid


def prism_delete_entity(api_server,username,secret,entity_type,entity_api_root,entity_name=None,entity_uuid=None,secure=False,print_f=True):

    """Deletes an entity given entity uuid or entity name.
       If an entity_uuid is specified, it will skip retrieving all entities to find uuid, by specifying the uuid in the arguments (faster).

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
        Task uuid when entity deletion request returns task uuid under $.status.state.execution_context.task_uuid
        task uuid is returned as None when the returned json is of a different format for some entity type
    """

    entity_uuid, entity_details = prism_get_entity(api_server,username,secret,
                                                   entity_type,entity_api_root,
                                                   entity_name=entity_name,entity_uuid=entity_uuid,
                                                   secure=secure,print_f=print_f)
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
    method = "DELETE"
    if print_f:
        print("{} API call to {} with secure set to {}".format(entity_type, url, secure))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        if print_f:
            print("INFO - {} {} deletion task initiated with success".format(entity_type, entity_details["status"]["name"]))
        res = json.loads(resp.content)
        #when entity deletion request returns the common $.status.state.execution_context.task_uuid
        if "status" in res and "execution_context" in res["status"] \
                    and "task_uuid" in res["status"]["execution_context"]:
            return res["status"]["execution_context"]["task_uuid"]
        #otherwise return None. for example, app deletion returned json has a different format ($.status.ergon_task_uuid).
        #it has to be monitored by a specific function, not using the standard entities library
        else:
            return None
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