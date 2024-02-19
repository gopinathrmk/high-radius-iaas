################################################
######## infoblox_ips.py           #############
################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################

def infoblox_add_fixed_address_reservation(infoblox_api_endpoint,username,secret,ip_address,hostname,extattrs=None,secure=False):

    """reserve a given ip address

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        ip_address: example: 192.168.5.99
        extattrs: extensible attributes to add. dict in the form:
            {
                "ext attr 1 name": {"value": "ext attr 1 value"},
                "ext attr 2 name": {"value": "ext attr 2 value"},
                ...
            }
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        The api result json.
    """

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'
    url = '{}fixedaddress'.format(infoblox_api_endpoint)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "ipv4addr":"{}".format(ip_address),
        "mac":"00:00:00:00:00:00",
        "extattrs": extattrs,
        "comment": "Created by Nutanix Self-Service (Calm) for VM: {}".format(hostname),
        "name": "{}.sddc.vwgroup.com".format(hostname)
    }
    resp = process_request(url,method='POST',user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        result = json.loads(resp.content)
        print('INFO - created fixed IP reservation for address {}: '.format(ip_address))
        return result
    else:
        print('ERROR - Failed to create fixed IP reservation for address {}: '.format(ip_address))
        exit(1)

def infoblox_release_fixed_address_reservation(infoblox_api_endpoint,username,secret,ip_address,extattrs=None,secure=False):

    """release a given ip address

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        ip_address: example: 192.168.5.99
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        The api result json.
    """

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'
    url = '{}request'.format(infoblox_api_endpoint)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = [
    {
        "method": "GET",
        "object": "ipv4address",
        "data": {"ip_address": ip_address},
        "assign_state": {"ipaddr_ref": "_ref"},
        "enable_substitution": True,
        "discard": True
    },
    {
        "method": "DELETE",
        "object": "##STATE:ipaddr_ref:##",
        "enable_substitution": True
    }
]
    resp = process_request(url,method='POST',user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        result = json.loads(resp.content)
        print('INFO - released fixed IP reservation for address {}: '.format(ip_address))
        return result
    else:
        print('ERROR - Failed to release fixed IP reservation for address {}: '.format(ip_address))
        exit(1)

def infoblox_check_fixed_address_reservation(infoblox_api_endpoint,username,secret,ip_address,extattrs=None,secure=False):

    """checks a given ip address reservation status

    Args:
        infoblox_api_endpoint: example: https://infoblox.here.local/wapi/v2.10/
        username: Infoblox user name.
        secret: Infoblox user name password.
        ip_address: example: 192.168.5.99
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        The api result json and reservation status.
    """

    if not infoblox_api_endpoint.endswith('/'):
        infoblox_api_endpoint += '/'
    url = '{}ipv4address?ip_address={}'.format(infoblox_api_endpoint, ip_address)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    resp = process_request(url,method='GET',user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        result = json.loads(resp.content)
        ip_status = result[0]['status']
        print('INFO - The reservation status for IP {} is {}: '.format(ip_address, ip_status))
        return result, ip_status
    else:
        print('ERROR - Failed to get the status of the IP address {}: '.format(ip_address))
        exit(1)