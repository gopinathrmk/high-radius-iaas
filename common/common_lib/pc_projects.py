################################################
############ pc_projects.py         ############
################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py
############################################################################################

def prism_get_projects(api_server,username,secret,secure=False,print_f=True,filter=None):

    """Retrieve the list of Projects from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search

    Returns:
        A list of Projects (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="project",entity_api_root="projects",secure=secure,print_f=print_f,filter=filter)


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


def prism_delete_project(api_server,username,secret,project_name=None,project_uuid=None,secure=False,print_f=True):

    """Deletes a project given its name or uuid.
       If a project_uuid is specified, it will skip retrieving all projects (faster) to find the designated project name.
       this is not a cascaded deletion. Request will fails if following conditions are not met:
       - Project has no VMs (will never happen for a standalone Calm appliance)
       - Project has no applications
       - Project has no blueprints
       - Project has no runbooks
       - Project has no endpoints
       - Project has no jobs
       - Project has no approval policies

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        project_name: Name of the project (optional).
        project_uuid: uuid of the project (optional).
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors

    Returns:
        Project deletion task uuid
    """

    task_uuid = prism_delete_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="project",entity_api_root="projects",entity_name=project_name,entity_uuid=project_uuid,
                              secure=secure,print_f=print_f)
    return task_uuid


def prism_get_project_internal(api_server,username,secret,project_name,project_uuid=None,secure=False,print_f=True):
    """Returns from Prism Central the uuid and details of a given project name.
       If a project_uuid is specified, it will skip retrieving all projects (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        project_name: Name of the project.
        project_uuid: Uuid of the project (optional).
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors

    Returns:
        A string containing the UUID of the Project (project_uuid) and the json content
        of the project details (project_details)
    """
    project_details = {}

    if project_uuid is None:
        #get the list vms from Prism
        project_list = prism_get_projects(api_server,username,secret,secure,print_f=print_f)
        for project in project_list:
            if project['spec']['name'] == project_name:
                project_uuid = project['metadata']['uuid']
                #project_details = project.copy()
                break

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/projects_internal/{0}".format(project_uuid)
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
        project_details = json.loads(resp.content)
    else:
        return None,None

    return project_uuid, project_details

def add_subnet_to_project_infrastructure(api_server,username,secret,project_uuid,subnet_uuid,subnet_name,secure=False):

    ## pc_projects.py, pc_entities.py, http_requests.py
    project_uuid, project = prism_get_project(api_server=api_server,username=username,secret=secret,
                                                project_name=None,project_uuid=project_uuid,
                                                secure=secure)


    account_uuid = project['status']['resources']['account_reference_list'][0]["uuid"]

    ## pc_ssp_environments.py
    account_uuid, account = prism_ssp_get_account(api_server=api_server,username=username,secret=secret,
                                                    account_name=None,account_uuid=account_uuid,
                                                    secure=secure)
    subnet_reference = project['status']['resources']["subnet_reference_list"]
    external_network = project['status']['resources']["external_network_list"]
    subnet_reference_to_add = []
    external_network_to_add = []
    account_name = account["status"]["name"]
    if account_name == "NTNX_LOCAL_AZ":
        subnet_reference_to_add = [
                {
                    "kind": "subnet",
                    "name": subnet_name,
                    "uuid": subnet_uuid
                }
            ]
    else:
        external_network_to_add = [
                {
                    "name": subnet_name,
                    "uuid": subnet_uuid
                }
            ]
    subnet_reference.extend(subnet_reference_to_add)
    external_network.extend(external_network_to_add)
    project['spec']['resources']["subnet_reference_list"] = subnet_reference
    project['spec']['resources']["external_network_list"] = external_network

    del(project["status"])

    url = 'https://{}:9440/api/nutanix/v3/projects/{}'.format(api_server, project_uuid)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = project
    resp = process_request(url,'PUT',user=username,password=secret,headers=headers,payload=payload,secure=secure)

    if resp.status_code == 202:
        result = resp.json()
        task_uuid = result['status']['execution_context']['task_uuid']
        task_state = result['status']['state']
        project_uuid = result['metadata']['uuid']
        print('INFO - Project subnets updated with status code: {}'.format(resp.status_code))
        print('INFO - task: {}, state: {}'.format(task_uuid, task_state))
        return task_uuid
    else:
        print('ERROR - project subnets update failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
        exit(1)


def add_subnet_to_project_environment(api_server,username,secret,environment_uuid,subnet_uuid,secure=False):

    ## pc_projects.py, pc_entities.py, http_requests.py
    environment_uuid, environment = prism_get_entity(api_server=api_server,username=username,secret=secret,
                                                        entity_type="environment",entity_api_root="environments",entity_name=None,entity_uuid=environment_uuid,
                                                        secure=secure)
    subnet_references = environment['status']['resources']["infra_inclusion_list"][0]["subnet_references"]
    subnet_references.append({"uuid": subnet_uuid})

    environment['spec']['resources']["infra_inclusion_list"][0]["subnet_references"] = subnet_references
    del(environment["status"])

    url = 'https://{}:9440/api/nutanix/v3/environments/{}'.format(api_server, environment_uuid)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = environment
    resp = process_request(url,'PUT',user=username,password=secret,headers=headers,payload=payload,secure=secure)

    if resp.ok:
        print('INFO - Project environment updated with status code: {}'.format(resp.status_code))
    else:
        print('ERROR - project environment update failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
        exit(1)