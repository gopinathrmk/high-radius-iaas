################################################
############ pc_subnets.py          ############
################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py
############################################################################################

def prism_get_subnets(api_server,username,secret,secure=False,print_f=True,filter=None):

    """Retrieve the list of subnets from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False)
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of subnets (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="subnet",entity_api_root="subnets",secure=secure,print_f=print_f,filter=filter)


def prism_get_subnet(api_server,username,secret,subnet_name=None,subnet_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given subnet name.
       If a subnet_uuid is specified, it will skip retrieving all subnets (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        subnet_name: Name of the subnet (optional).
        subnet_uuid: Uuid of the subnet (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the Subnet (subnet_uuid) and the json content
        of the subnet details (subnet)
    """

    subnet_uuid, subnet = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="subnet",entity_api_root="subnets",entity_name=subnet_name,entity_uuid=subnet_uuid,
                              secure=secure,print_f=print_f)
    return subnet["metadata"]["uuid"], subnet


def prism_get_subnet_uuid(api_server,username,secret,subnet_name,secure=False,print_f=True):

    """Returns from Prism Central the uuid given subnet name.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        subnet_name: Name of the subnet
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the Subnet
    """

    subnet_uuid, subnet = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="subnet",entity_api_root="subnets",entity_name=subnet_name,entity_uuid=None,
                              secure=secure,print_f=print_f)
    return subnet["metadata"]["uuid"]


def prism_create_overlay_subnet_managed(api_server,username,secret,subnet_name,
                                        subnet_ip,prefix_length,default_gateway_ip,dns_list_csv,ip_pool_start,ip_pool_end,vpc_uuid,
                                        secure=False):

    """createa an overlay subnet.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        subnet_name: Name of the subnet to be created
        subnet_ip: ip of the ip to be created. example: "192.168.35.0"
        prefix_length: mask length (string) of the subnet to be created. example: "24"
        default_gateway_ip: ip address of the default gateway to be associated with the created subnet
        dns_list_csv: list of DNS resolvers ip addresses to be associated with this subnet ("ip1,ip2,...")
        ip_pool_start: first ip address of the ip pool
        ip_pool_end: last ip address of the ip pool
        vpc_uuid: uuid of the vpc where the subnet will be created
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        the uuid of the created subnet and the uuid of the creation task
    """

    url = 'https://{}:9440/api/nutanix/v3/subnets'.format(api_server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "metadata": {
            "kind": "subnet"
        },
        "spec": {
            "name": subnet_name,
            "resources": {
                "ip_config": {
                    "subnet_ip": subnet_ip,
                    "prefix_length": int(prefix_length),
                    "default_gateway_ip": default_gateway_ip,
                    "pool_list": [
                        {
                            "range": "{} {}".format(ip_pool_start,ip_pool_end)
                        }
                    ],
                    "dhcp_options": {
                        "domain_search_list": dns_list_csv.split(','),
                    }
                },
                "subnet_type": "OVERLAY",
                "vpc_reference": {
                    "kind": "vpc",
                    "uuid": vpc_uuid
                }
            }
        },
        "api_version": "3.1.0"
    }

    print(json.dumps(payload))

    resp = process_request(url,'POST',user=username,password=secret,headers=headers,payload=payload,secure=secure)

    if resp.status_code == 202:
        result = json.loads(resp.content)
        task_uuid = result['status']['execution_context']['task_uuid']
        subnet_uuid = result['metadata']['uuid']
        print('INFO - Subnet {}/{} created with status code: {}'.format(subnet_ip,prefix_length,resp.status_code))
        print('INFO - Subnet uuid: {}'.format(subnet_uuid))
    else:
        print('ERROR - Subnet {}/{} creation failed, status code: {}, msg: {}'.format(subnet_ip,prefix_length,resp.status_code, resp.content))
        exit(1)

    return subnet_uuid, task_uuid


def prism_delete_subnet(api_server,username,secret,subnet_name=None,subnet_uuid=None,secure=False,print_f=True):

    """Deletes a subnet given its name or uuid.
       If a subnet_uuid is specified, it will skip retrieving all subnets (faster) to find the designated subnet name.


    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        subnet_name: Name of the subnet (optional).
        subnet_uuid: uuid of the subnet (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        subnet deletion task uuid
    """

    task_uuid = prism_delete_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="subnet",entity_api_root="subnets",entity_name=subnet_name,entity_uuid=subnet_uuid,
                              secure=secure,print_f=print_f)
    return task_uuid