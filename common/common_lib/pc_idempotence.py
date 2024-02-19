########################################################################
############       pc_idempotence.py                        ############
########################################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################

def pc_generate_uuid(api_server,username,secret,secure=False):

    """Generates a nww uuid.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        a new uuid
    """
 
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/idempotence_identifiers"
    url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint)
    method = "POST"
    payload = {
        "count": 1,
        "valid_duration_in_minutes": 527040
    }
    print("Making a {} API call to {}".format(method, url))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        return resp.json()['uuid_list'][0]
    else:
        print("ERROR: Failed to generate uuid")