################################################
######## infoblox_subnets.py       #############
################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################


def infoblox_reserve_next_subnet(infoblox_api_endpoint,username,secret,container_network_address,requested_subnet_cidr,extattrs=None,secure=False):

    """get and reserve the next available subnet from a containing network

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        container_network_address: get the next available subnet from this network. network container address example: 192.168.0.0/16
        requested_subnet_cidr: choose the desired cidr length for the requested subnet (should be greater than the container network cidr length)
        extattrs: extensible attributes to add. dict in the form:
            {
                "ext attr 1 name": {"value": "ext attr 1 value"},
                "ext attr 2 name": {"value": "ext attr 2 value"},
                ...
            }
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        returned result example (dict):
        {
            "_ref": "network/ZG5zLm5ldHdvcmskMTkyLjE2OC4xNy4wLzI0LzA:192.168.17.0/24/default",
            "extattrs": {},
            "members": [],
            "network": "192.168.17.0/24",
            "network_view": "default"
        }
    """

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'
    url = '{}network?_return_fields%2B=network,members,extattrs&_return_as_object=1'.format(infoblox_api_endpoint)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "network": 'func:nextavailablenetwork:{},default,{}'.format(container_network_address,requested_subnet_cidr),
        "extattrs": extattrs
    }
    resp = process_request(url,method='POST',user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        result = json.loads(resp.content)
        print('INFO - retrieved and reserved subnet {}: '.format(result["result"]["network"]))
        return result["result"]
    else:
        print('ERROR - Failed to get the next available network from container network {}'.format(container_network_address))
        exit(1)


def infoblox_get_subnet_unused_ips(infoblox_api_endpoint,username,secret,subnet_address,secure=False):

    """return a list of unused ip addresses in a given subnet

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        subnet_address: example: 192.168.5.0/24
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        returned result example (array):
        ["192.168.5.5", "192.168.5.6", "192.168.5.28", "192.168.5.55"]
    """

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'
    url = '{}ipv4address?network={}&status=UNUSED'.format(infoblox_api_endpoint, subnet_address)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    resp = process_request(url,method='GET',user=username,password=secret,headers=headers,payload=None,secure=secure)
    if resp.ok:
        result = json.loads(resp.content)
        print('INFO - retrieved unused ip addresses from subnet {}: '.format(subnet_address))
        return [ip["ip_address"] for ip in result]
    else:
        print('ERROR - Failed to fetch unused ip addresses from subnet {}: '.format(subnet_address))
        exit(1)


def infoblox_get_network_ref(infoblox_api_endpoint,username,secret,subnet_address,object_type,secure=False):

    """return the ref of some infoblox network in the form:
        "<object_type>/<id>/<subnet_cidr>/<view>"
        examples:
            "networkcontainer/ZG5zLm5ldHdvcmtfY29udGFpbmVyJDE5Mi4xNjguMC4wLzE2LzA:192.168.0.0/16/default"
            "network/ZG5zLm5ldHdvcmskMTkyLjE2OC4yMC4wLzI0LzA:192.168.20.0/24/default"

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        subnet_address: example: 192.168.5.0/24
        object_type: Infoblox network object type. A string like "network" or "networkcontainer" or a list like ["network", "networkcontainer"].
                        if a list is passed, it means that the fetched object can be one of the types included in the list
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        returns api ref for the fetched object
    """
    object_type_list = object_type
    if type(object_type) is str:
        object_type_list = [object_type]

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'

    failed = False

    for object_type_i in object_type_list:
        url = '{}{}?network={}&_return_as_object=1'.format(infoblox_api_endpoint, object_type_i, subnet_address)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        resp = process_request(url,method='GET',user=username,password=secret,headers=headers,payload=None,secure=secure)
        if resp.ok:
            result = json.loads(resp.content)
            if result["result"] != []:
                print('INFO - retrieved ref of subnet {}'.format(subnet_address))
                return result["result"][0]["_ref"]
        else:
            failed = True

    if failed:
        print('ERROR - Failed to fetch ref for subnet {}: '.format(subnet_address))
        exit(1)
    else:
        print('ERROR - subnet {} not found'.format(subnet_address))
        exit(1)


def infoblox_delete_network(infoblox_api_endpoint,username,secret,subnet_address,secure=False):

    """deletes an infoblox network given its subnet address

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        subnet_address: example: 192.168.5.0/24
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        No value returned
    """

    nw_ref = infoblox_get_network_ref(infoblox_api_endpoint=infoblox_api_endpoint,username=username,secret=secret,
                                      subnet_address=subnet_address,object_type=["network", "networkcontainer"],
                                      secure=secure)
    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'

    url = '{}{}'.format(infoblox_api_endpoint, nw_ref)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    resp = process_request(url,method='DELETE',user=username,password=secret,headers=headers,payload=None,secure=secure)
    if resp.ok:
        print('INFO - Network {} deleted'.format(subnet_address))
    else:
        print('ERROR - Failed to delet network {}: '.format(subnet_address))
        exit(1)


def infoblox_get_network(infoblox_api_endpoint,username,secret,subnet_address,object_type,return_fields,secure=False):

    """return infoblox network object given subnet address

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        subnet_address: example: 192.168.5.0/24
        object_type: Infoblox network object type. A string like "network" or "networkcontainer" or a list like ["network", "networkcontainer"].
                        if a list is passed, it means that the fetched object can be one of the types included in the list
        return_fields: comma-separated string of fields that will be returned
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        returns fetched network object
    """

    object_type_list = object_type
    if type(object_type) is str:
        object_type_list = [object_type]

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'

    failed = False

    for object_type_i in object_type_list:
        appended_return_fields = ""
        if return_fields!="" and return_fields!=None:
            appended_return_fields = '&_return_fields%2B={}'.format(return_fields)
        url = '{}{}?network={}&_return_as_object=1{}'.format(infoblox_api_endpoint, object_type_i, subnet_address, appended_return_fields)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        resp = process_request(url,method='GET',user=username,password=secret,headers=headers,payload=None,secure=secure)
        if resp.ok:
            result = json.loads(resp.content)
            if result["result"] != []:
                print('INFO - retrieved subnet {}'.format(subnet_address))
                return result["result"][0]
        else:
            failed = True

    if failed:
        print('ERROR - Failed to fetch subnet {}: '.format(subnet_address))
        exit(1)
    else:
        print('ERROR - subnet {} not found'.format(subnet_address))
        exit(1)


def infoblox_create_extensible_attribute_def(infoblox_api_endpoint,username,secret,ext_attr_name,secure=False):

    """create ext attr def in infoblox if not exists
    the type of the ext ext att created by this functiuon is STRING

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        ext_attr_name: name of the new ext attr
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        No value returned
    """

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'
    url = '{}extensibleattributedef'.format(infoblox_api_endpoint)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "name": ext_attr_name,
        "type": "STRING"
    }
    resp = process_request(url,method='GET',user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        result = json.loads(resp.content)
        if [attr for attr in result if attr["name"]==ext_attr_name] != []:
            print('INFO - Extensible attribute {} already exists. No addition is ncessary'.format(ext_attr_name))
            return
    else:
        print('ERROR - occured while checking existence of Extensible attribute {}: '.format(ext_attr_name))
        exit(1)

    resp = process_request(url,method='POST',user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        print('INFO - Extensible attribute {} created'.format(ext_attr_name))
    else:
        print('ERROR - occured while creating extensible attribute {}: '.format(ext_attr_name))
        exit(1)