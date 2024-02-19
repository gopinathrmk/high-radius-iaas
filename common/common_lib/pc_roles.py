################################################
############     pc_roles.py       ############
################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py, http_requests.py
############################################################################################

def prism_get_roles(api_server,username,secret,secure=False,print_f=True,filter=None):

    """Retrieve the list of Roles from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of roles (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="role",entity_api_root="roles",secure=secure,print_f=print_f,filter=filter)


def prism_get_role(api_server,username,secret,role_name=None,role_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given role name.
       If a role_uuid is specified, it will skip retrieving all roles (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        role_name: Name of the role (optional).
        role_uuid: Uuid of the role (optional).
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the role (role_uuid) and the json content
        of the role details (role)
    """

    role_uuid, role = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="role",entity_api_root="roles",entity_name=role_name,entity_uuid=role_uuid,
                              secure=secure,print_f=print_f)
    return role_uuid, role


def pc_get_role_uuid(api_server,username,secret,role_name=None,secure=False):
    """
        Retrieve a role uuid on Prism Central

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        role_name: Role name to retrieve
        secure: boolean to verify or not the api server's certificate (True/False)
        
    Returns:
        Role uuid (string).
    """

    # region prepare the api call
    headers = {'Content-Type': 'application/json','Accept': 'application/json'}
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/roles/list"
    url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint)
    method = "POST"
    payload = {'kind':'role','filter':'name=={}'.format(role_name)}
    # endregion

    # Making the call
    print("Retrieving role {} uuid on {}".format(role_name,api_server))
    print("Making a {} API call to {}".format(method, url))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        json_resp = json.loads(resp.content)
    else:
        return None 

    if json_resp['entities']:
        return json_resp['entities'][0]['metadata']['uuid']
    else:
        return None
    