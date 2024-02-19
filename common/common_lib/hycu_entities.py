########################################################################
############       hycu_entities.py                         ############
########################################################################


############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################


def hycu_get_entities(api_server_endpoint,username,secret,entity_api_root,secure=False,filter=None,print_f=True):

    """Retrieve the list of entities from HYCU.

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        entity_api_root: api root for this entity type. for example. for users the list api is "...rest/v1.0/users".
                         the entity api root here is "users"
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        An array of entities (entities part of the json response).
    """

    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'

    entities = []
    #region prepare the api call
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "GET"
    payload = None
    page_size = 100
    page_number = 1
    url = '{}{}?pageSize={}&pageNumber={}'.format(api_server_endpoint, entity_api_root, page_size, page_number)
    if filter!= None and filter!= "":
        url = '{}&filter={}'.format(url,filter)
    #endregion

    while True:
        if print_f:
            print("Making a {} API call to {} with secure set to {}".format(method, url, secure))
        resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
        # deal with the result/response
        if resp.ok:
            json_resp = json.loads(resp.content)
            entities.extend(json_resp['entities'])
            key = 'totalEntityCount'
            if key in json_resp['metadata']:
                if len(entities) < json_resp['metadata']['totalEntityCount']:
                    if print_f:
                        print("Processing results from {} to {} out of {}".format(
                            page_size*page_number+1, 
                            min(page_size*(page_number+1), json_resp['metadata']['totalEntityCount']),
                            json_resp['metadata']['totalEntityCount']))
                    page_number += 1
                    url = '{}{}?pageSize={}&pageNumber={}'.format(api_server_endpoint, entity_api_root, page_size, page_number) 
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


def hycu_get_entity(api_server_endpoint,username,secret,entity_api_root,entity_name=None,entity_uuid=None,secure=False,print_f=True):

    """Returns from HYCU the uuid and details of a given entity name.
       If an entity_uuid is specified, it will skip retrieving all entities by specifying the uuid in the arguments (faster).

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        entity_api_root: api root for this entity type. for example. for users the list api is "...rest/v1.0/users".
                         the entity api root here is "users"
        entity_name: Name of the entity (optional).
        entity_uuid: Uuid of the entity (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the entity (entity_uuid) and the json content
        of the entity details (entity_details)
    """
    
    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'

    entity_details = {}

    if entity_uuid is None:
        #get the entities list from HYCU
        entity_list = hycu_get_entities(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                        entity_api_root=entity_api_root,
                                        secure=secure,print_f=print_f)
        att_name = "name"
        if entity_api_root == 'users':
            att_name = "username"
        for entity in entity_list:
            fetched_name = ""
            if att_name in entity:
                fetched_name = entity[att_name]
            else:
                print("ERROR - fetched entity name could not be extracted for entity {}".format(entity['uuid']))
                raise
            if fetched_name == entity_name:
                entity_uuid = entity['uuid']
                entity_details = entity.copy()
                break
        if entity_details == {}:
            print("ERROR - Entity {} not found".format(entity_name))
            exit(1)
    else:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        method = "GET"
        payload = None
        url = '{}{}/{}'.format(api_server_endpoint, entity_api_root, entity_uuid)

        if print_f:
            print("Making a {} API call to {} with secure set to {}".format(method, url, secure))
        resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
        if resp.ok:
            entity_details = json.loads(resp.content)["entities"][0]
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


def hycu_delete_entity(api_server_endpoint,username,secret,entity_api_root,entity_name=None,entity_uuid=None,secure=False,print_f=True):

    """Deletes an entity given entity uuid or entity name.
       If an entity_uuid is specified, it will skip retrieving all entities to find uuid, by specifying the uuid in the arguments (faster).

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        entity_api_root: api root for this entity type. for example. for users the list api is "...rest/v1.0/users".
                         the entity api root here is "users"
        entity_name: Name of the entity (optional).
        entity_uuid: Uuid of the entity (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        No value returned
    """

    entity_uuid, entity_details = hycu_get_entity(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                                  entity_api_root=entity_api_root,entity_name=entity_name,entity_uuid=entity_uuid,
                                                  secure=secure,print_f=print_f)
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "DELETE"
    payload = None
    url = '{}{}/{}'.format(api_server_endpoint, entity_api_root, entity_uuid)

    if print_f:
        print("{} API call to {} with secure set to {}".format(entity_api_root, url, secure))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        if print_f:
            print("INFO - {} {} deletion initiated with success".format(entity_api_root, entity_details["name"]))
        res = json.loads(resp.content)
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