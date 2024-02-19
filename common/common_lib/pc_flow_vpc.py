########################################################################
############       pc_flow_vpc.py                           ############
########################################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py
############################################################################################

def prism_get_vpc(api_server,username,secret,project_name=None,project_uuid=None,secure=False,print_f=True):

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

def prism_flow_vpc_add_externally_routable_ips(api_server,username,secret,vpc_uuid,externally_routable_prefix_list,secure=False):

    """adds externally routable ranges to a vpc.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        vpc_uuid: uuid of the vpc to be updated
        externally_routable_prefix_list: list of ip ranges (in CIDR) that will be routed externally in the form:
            ["10.10.10.0/24", "10.10.10.0/18", ...]
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        the uuid of the vpc update task
    """

    url = 'https://{}:9440/api/nutanix/v3/vpcs/{}'.format(api_server,vpc_uuid)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    resp = process_request(url,'GET',user=username,password=secret,headers=headers,payload=None,secure=secure)
    if resp.ok:
        vpc = json.loads(resp.content)
    else:
        print("ERROR - occured while fetching VPC with uuid{}".format(vpc_uuid))
        exit(1)

    payload = vpc
    new_prefix_list = [
                        "{}/{}".format(prefix["ip"],prefix["prefix_length"])
                     for prefix in  payload["status"]["resources"]["externally_routable_prefix_list"]
                ]

    new_prefix_list.extend(externally_routable_prefix_list)
    new_prefix_list = list(set(new_prefix_list))

    new_prefix_list_payload = [
                                                                        {
                                                                            "ip": prefix.split('/')[0], "prefix_length": int(prefix.split('/')[1])
                                                                        } for prefix in  new_prefix_list
                ]

    payload["spec"]["resources"]["externally_routable_prefix_list"] = new_prefix_list_payload
    del(payload["status"])
    resp = process_request(url,'PUT',user=username,password=secret,headers=headers,payload=payload,secure=secure)

    if resp.status_code == 202:
        result = resp.json()
        task_uuid = result['status']['execution_context']['task_uuid']
        task_state = result['status']['state']
        print('INFO - VPC updated with status code: {}'.format(resp.status_code))
        print('INFO - task: {}, state: {}'.format(task_uuid, task_state))
        return task_uuid
    else:
        print('ERROR - VPC update failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
        exit(1)

def prism_flow_create_vpc(api_server,username,secret,vpc_name,ext_subnet_uuid_list,dns_list_csv,externally_routable_prefix_list,secure=False):

    """Creates a flow VPC.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        vpc_name: name of the vpc to be created
        ext_subnet_uuid_list: list (array) of uuids of the external subnets that will be associated with the created vpc
                                maximum one NATed network and one No-NAT network can be listed here
        dns_list_csv: list of DNS resolvers ip addresses to be associated with this vpc ("ip1,ip2,...")
        externally_routable_prefix_list: list of ip ranges (in CIDR) that will be routed externally in the form:
            [
                {
                    "ip": "192.168.10.0",
                    "prefix_length": 24
                },
                ...
            ]
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        the uuid of the created vpc and the uuid of the creation task
    """

    url = 'https://{}:9440/api/nutanix/v3/vpcs'.format(api_server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "api_version": "3.1.0",
        "metadata": {
            "kind": "vpc"
        },
        "spec": {
            "name": vpc_name,
            "resources": {
                "common_domain_name_server_ip_list": [
                    {
                        "ip": ip
                    } for ip in (dns_list_csv.split(',') if dns_list_csv!="" else [])
                ],
                "external_subnet_list": [
                    {
                        "external_subnet_reference": {
                            "kind": "subnet",
                            "uuid": uuid
                        }
                    } for uuid in ext_subnet_uuid_list
                ],
                "externally_routable_prefix_list": externally_routable_prefix_list
            }
        }
    }
    resp = process_request(url,'POST',user=username,password=secret,headers=headers,payload=payload,secure=secure)

    if resp.status_code == 202:
        result = json.loads(resp.content)
        task_uuid = result['status']['execution_context']['task_uuid']
        vpc_uuid = result['metadata']['uuid']
        print('INFO - VPC created with status code: {}'.format(resp.status_code))
        print('INFO - VPC uuid: {}'.format(vpc_uuid))
    else:
        print('ERROR - VPC creation failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
        exit(1)

    return vpc_uuid, task_uuid

def prism_flow_set_default_route(api_server,username,secret,vpc_uuid,ext_subnet_uuid,secure=False):

    """adds a static default route to a vpc.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        vpc_uuid: uuid of the vpc to be updated
        ext_subnet_uuid: uuid of the external subnet (must be already associated with the vpc)
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        the uuid of the vpc update task
    """

    url = 'https://{}:9440/api/nutanix/v3/vpcs/{}/route_tables'.format(api_server,vpc_uuid)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "api_version":"3.1.0",
        "metadata":{
            "kind":"vpc_route_table",
            "uuid": vpc_uuid
        },
        "spec":{
            "resources":{
                "static_routes_list":[
                ],
                "default_route_nexthop":{
                    "external_subnet_reference":{
                        "kind": "subnet",
                        "uuid": ext_subnet_uuid
                    }
                }
            }
        }
    }
    resp = process_request(url,'PUT',user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.status_code == 202:
        result = json.loads(resp.content)
        task_uuid = result['status']['execution_context']['task_uuid']
        print('INFO - VPC Updated with status code: {}'.format(resp.status_code))
    else:
        print('ERROR - VPC Update failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
        exit(1)
    return task_uuid

def prism_delete_vpc(api_server,username,secret,vpc_name=None,vpc_uuid=None,secure=False,print_f=True):

    """Deletes a vpc given its name or uuid.
       If a vpc_uuid is specified, it will skip retrieving all vpcs (faster) to find the designated vpc name.


    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        vpc_name: Name of the vpc (optional).
        vpc_uuid: uuid of the vpc (optional).
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors

    Returns:
        vpc deletion task uuid
    """

    task_uuid = prism_delete_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="vpc",entity_api_root="vpcs",entity_name=vpc_name,entity_uuid=vpc_uuid,
                              secure=secure,print_f=print_f)
    return task_uuid