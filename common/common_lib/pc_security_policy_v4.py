################################################
############ pc_security_policy.py   ###########
################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################

def get_category_uuid_v4(api_server,username,secret,category,secure=False):

    """Retrieve the UUID of Category from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        category : Dictionary containing the Category Key and Value . 
        
    Returns:
        UUID (str) of Category if found or False(bool) if not found.
    """

    key = list(category.keys())[0]
    value = list(category.values())[0]
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/prism/v4.0.a1/config/categories?$filter=fqName eq '{}/{}'".format(key,value)
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"

    print("HTTP {} request to {} ".format(method,url))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)

    if resp.ok:
        json_resp = json.loads(resp.content)
        if (json_resp.get("metadata").get("totalAvailableResults") == 1 ):
            return json_resp["data"][0]["extId"]
        else:
            print("Given Category {}:{} couldn't be found !!!".format(key,value))
            return False

def pc_get_security_policy(api_server,username,secret,extId,secure=False):

    """Retrieve the Security Policy from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        extId : UUId of Security Policy. 
        
    Returns:
        Security Policy Details (response) if found. False(bool) if not found.
    """

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/microseg/v4.0.a1/config/policies/{}".format(extId)
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"

    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        return resp
    else:
        print("Failure to retrieve secuity policy with extId:{}".format(extId))
        return False
    
def pc_list_security_policy(api_server,username,secret,secure=False):

    """Retrieve the List of Security Policies from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        Security Policy List (response) if found. False(bool) if not found.
    """

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/microseg/v4.0.a1/config/policies"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"

    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        return json.loads(resp.content)
    else:
        print("Failure to retrieve list of security policy ")
        return False

def pc_get_security_policy_by_secured_category(api_server,username,secret,secured_group_uuids,secure=False):

    """Retrieve the Security Policy UUID, filtered by Secured Entity from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        secured_group_uuids : List of Category UUIds 
        
    Returns:
        UUID (str) of Security Policy if found or None if not found.
    """    

    json_resp = pc_list_security_policy(api_server=api_server,username=username,secret=secret,secure=secure)
    extId = None 
    for policy in json_resp["data"]:
        secured_group = policy["securedGroups"]
        if  set(secured_group_uuids) == set(secured_group):
            extId = policy["extId"]
            break
        
    return extId

def create_inbound_rule(secured_group_uuid,source_type,source_category_uuid,source_subnet,source_protocol,source_network_ports,description=""):

    """Create Inbound rules with the provided input.

    Args:
        secured_group_uuid: List of Category UUIDs for secured group Entity.
        source_type: 'Category' or 'Subnet' depending upon the input:.
        source_category_uuid: Single source Category UUID if type is 'Category'.
        source_subnet: Subnet if type is 'Subnet'. Ex: '10.10.2.0/24' 
        source_protocol : Protocol to be allowed by rules. 'TCP' or 'UDP' or 'ICMP' or 'All'
        source_network_ports :  Ports allowed in the above network. Ex: 5000 or 6000-7000 or Any.   
                                In case of ICMP 'type-code' . EX 10-15 or Any
        
    Returns:
        Dictionary containing the rule specification for inbound.
    """    

    if source_type == 'Category':
        if source_category_uuid != None:
            source = {"srcCategoryReferences": [source_category_uuid]}
        else:
            print("Source Category UUID is expected !!!")
            return False
    elif source_type == 'Subnet':
        if source_subnet != None:
            subnet = source_subnet.split("/")
            network = subnet[0]
            mask = int(subnet[1])
            source = {"srcSubnet" : {"value" : network,"prefixLength": mask}}
        else:
            print("Source Subnet CIDR is expected !!!")
            return False
    elif source_type == 'All':
        source = {"srcAllowSpec":"ALL"}
    else:
        print("Invalid Source Type !!!")
        return False

    if source_protocol == 'All':
        inbound_services = { "isAllProtocolAllowed" : True }
    elif source_protocol == 'TCP' or source_protocol == 'UDP' :
        protocol_mapping = {"TCP": "tcpServices","UDP":"udpServices"}
        source_start_port = source_network_ports[0]
        source_end_port = source_network_ports[1] if len(source_network_ports)>1 else source_network_ports[0]
        if source_start_port == "Any" :
            source_start_port = 0
            source_end_port = 65535
        else:
            source_start_port = int(source_start_port)
            source_end_port =  int(source_end_port)
        inbound_services = {
                    protocol_mapping[source_protocol]:[ {"startPort": source_start_port, "endPort": source_end_port} ]
                }
    elif source_protocol == 'ICMP':
        type = source_network_ports[0]
        code = source_network_ports[1] if len(source_network_ports)>1 else source_network_ports[0]
        if type == "Any" :
            inbound_services = { "icmpServices": [ {"isAllAllowed": True } ] }
        else:
            inbound_services = {
                "icmpServices": [ {"type": int(type), "code": int(code)} ]
                }

    rule = {
        "description" : description,
        "type": "APPLICATION",
        "spec": {
                "$objectType": "microseg.v4.config.ApplicationRuleSpec",   #todo change to b1 spec , now its working
                "securedGroupCategoryReferences": secured_group_uuid,         
        }

    }
    rule.get("spec").update(source)
    rule.get("spec").update(inbound_services)

    print("Inbound Rule is , {}".format(rule))
    return rule


def create_outbound_rule(secured_group_uuid,dest_type,dest_category_uuid,dest_subnet,dest_protocol,dest_network_ports,description=""):

    """Create Outbound rules with the provided input.

    Args:
        secured_group_uuid: List of Category UUIDs for secured group Entity.
        dest_type: 'Category' or 'Subnet' depending upon the input:.
        dest_category_uuid: Single source Category UUID if type is 'Category'.
        dest_subnet: Subnet if type is 'Subnet'. Ex: '10.10.2.0/24' 
        dest_protocol : Protocol to be allowed by rules. 'TCP' or 'UDP' or 'ICMP' or 'All'
        dest_network_ports :  Ports allowed in the above network. Ex: 5000 or 6000-7000 or Any.   
                                In case of ICMP 'type-code' . EX 10-15 or Any
        
    Returns:
        Dictionary containing the rule specification for outbound.
    """  

    if dest_type == 'Category':
        if dest_category_uuid != None:
            dest = {"destCategoryReferences": [dest_category_uuid]}
        else:
            print("dest Category UUID is expected !!!")
            return False
    elif dest_type == 'Subnet':
        if dest_subnet != None:
            subnet = dest_subnet.split("/")
            network = subnet[0]
            mask = int(subnet[1])
            dest = {"destSubnet" : {"value" : network,"prefixLength": mask}}
        else:
            print("dest Subnet CIDR is expected !!!")
            return False
    elif dest_type == 'All':
        dest = {"destAllowSpec":"ALL"}
    else:
        print("Invalid dest Type !!!")
        return False


    if dest_protocol == 'All':
        outbound_services = { "isAllProtocolAllowed" : True }
    elif dest_protocol == 'TCP' or dest_protocol == 'UDP' :
        protocol_mapping = {"TCP": "tcpServices","UDP":"udpServices"}
        dest_start_port = dest_network_ports[0]
        dest_end_port = dest_network_ports[1] if len(dest_network_ports)>1 else dest_network_ports[0]
        if dest_start_port == "Any" :
            dest_start_port = 0
            dest_end_port = 65535
        else:
            dest_start_port = int(dest_start_port)
            dest_end_port =  int(dest_end_port)        
                
        outbound_services = {
                    protocol_mapping[dest_protocol]:[ {"startPort": dest_start_port, "endPort": dest_end_port} ]
                }
    elif dest_protocol == 'ICMP':
        type = dest_network_ports[0]
        code = dest_network_ports[1] if len(dest_network_ports)>1 else dest_network_ports[0]
        if type == "Any" :
            outbound_services = { "icmpServices": [ {"isAllAllowed": True } ] }
        else:
            outbound_services = {
                "icmpServices": [ {"type": int(type), "code": int(code)} ]
                }

    rule = {
        "description" : description,
        "type": "APPLICATION",
        "spec": {
                "$objectType": "microseg.v4.config.ApplicationRuleSpec",
                "securedGroupCategoryReferences": secured_group_uuid,         
        }

    }
    rule.get("spec").update(dest)
    rule.get("spec").update(outbound_services)

    print("outbound Rule is , {}".format(rule))
    return rule
    
def create_intragroup_rule(secured_group_uuid,secured_group_action):

    """Create Intragroup rules with the provided input.

    Args:
        secured_group_uuid: List of Category UUIDs for secured group Entity.
        secured_group_action: "ALLOW" or "DENY".
       
    Returns:
        Dictionary containing the rule specification for Intragroup.
    """  

    if not (secured_group_action ==  "ALLOW" or secured_group_action == "DENY"):
        print("Either 'ALLOW' or 'DENY; is expected for secured_group_action")
        return False

    rule = {
        "type": "INTRA_GROUP",
        "spec" : {
            "$objectType": "microseg.v4.config.IntraEntityGroupRuleSpec",
            "securedGroupCategoryReferences" : secured_group_uuid,
            "securedGroupAction" : secured_group_action
        }
    }
    print("IntraGroup Rule is , {}".format(rule))
    return rule

def create_secuity_policy_v4(api_server,username,secret,name,rules,type="APPLICATION",description="",state="MONITOR",vpcReferences=None,isHitlogEnabled=False,isIpv6TrafficAllowed=False,secure=False):

    """Create Security Policy with the provided rules.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        name: Name of Security Policy
        rules : Rules (dict) containing inbound, intragroup and/or outbound rules.  
        type : "APPLICATION" . Currently only Application is supported
        description : Description of Security Policy
        state: "ENFORCE" or "MONITOR" or "SAVE". Default is "MONITOR"
        vpcReferences : VPC UUID to apply policy to Subnet inside a VPC
        isHitlogEnabled : bool FALSE or TRUE
        isIpv6TrafficAllowed : bool FALSE or TRUE
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        Response Content containing the task ID for security policy Creation.
    """  

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'NTNX-Request-Id' : str(uuid.uuid4())
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/microseg/v4.0.a1/config/policies"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "POST"

    # Compose the json payload
    payload = {
        "name" : name, 
        "type" : type,
        "description": description,
        "state": state,
        "isHitlogEnabled":isHitlogEnabled,
        "isIpv6TrafficAllowed" :isIpv6TrafficAllowed,
        "rules" : rules
    }    

    if vpcReferences:
        payload.update({"scope" :"VPC_LIST","vpcReferences" : vpcReferences})

    print("payload is ",payload) 

    resp = process_request(url=url,method=method,payload=payload,user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        return json.loads(resp.content)
    else:
        print("Failed to create a new security Policy")
        return False


def pc_update_security_policy_v4(api_server, username, secret, extId, rules, secure=False):

    """Update Security Policy with the provided rules.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        extId : ID of Security Policy to update
        rules : Rules (dict) containing inbound, intragroup and/or outbound rules.  
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        Response Content containing the task ID for security policy Update.
    """  


    response = pc_get_security_policy(api_server=api_server, username=username, secret=secret, secure=secure,
                                      extId=extId)
    header = dict(response.headers)
    etag = header.get("Etag", None)
    security_details = json.loads(response.content)
    data = security_details.get("data", None)
    scope = data.get("scope",None)
    vpcReferences = data.get("vpcReferences",None)


    payload = {
        "name": data.get("name", None),
        "type": data.get("type", None),
        "rules": rules
    }

    if vpcReferences:
        payload.update({"scope" :scope,"vpcReferences" : vpcReferences})

    print("payload is ", payload)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'IF-Match': etag,
        'NTNX-Request-Id': str(uuid.uuid4())
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/microseg/v4.0.a1/config/policies/{}".format(extId)
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "PUT"

    resp = process_request(url=url, method=method, payload=payload, user=username, password=secret, headers=headers,
                           secure=secure)
    if resp.ok:
        return json.loads(resp.content)
    else:
        print("Failed to update the security Policy")
        return False


def pc_delete_security_policy_v4(api_server, username, secret, extId,secure=False):

    """Delete Security Policy by ID.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        extId : ID of Security Policy to update
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        Response Content containing the task ID for security policy deletion.
    """  

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'NTNX-Request-Id' : str(uuid.uuid4())
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/microseg/v4.0.a1/config/policies/{}".format(extId)
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "DELETE"

    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        return json.loads(resp.content)
    else:
        print("Failed to delete security Policy with extID:{}".format(extId))
        return False    



####### Methods for v4.0.A1 ###############
def create_inbound_rule_a1(secured_group_uuid,source_type,source_category_uuid,source_subnet,source_protocol,source_network_ports,description=""):
    
    if source_type == 'Category':
        if source_category_uuid != None:
            source = {"sourceCategories": [source_category_uuid]}
        else:
            print("Source Category UUID is expected !!!")
            return False
    elif source_type == 'Subnet':
        if source_subnet != None:
            subnet = source_subnet.split("/")
            network = subnet[0]
            mask = int(subnet[1])
            source = {"sourceSubnet" : {"value" : network,"prefixLength": mask}}
        else:
            print("Source Subnet CIDR is expected !!!")
            return False
    elif source_type == 'All':
        source = {"sourceAllowSpec":"ALL"}
    else:
        print("Invalid Source Type !!!")
        return False

    protocol_mapping = {"TCP": "tcpServices","UDP":"udpServices"}
    source_start_port = source_network_ports[0]
    source_end_port = source_network_ports[1] if len(source_network_ports)>1 else source_network_ports[0]

    if source_protocol == 'All':
        inbound_services = { "isAllProtocolAllowed" : True }
    else:
        inbound_services = {
                    protocol_mapping[source_protocol]:[ {"startPort": int(source_start_port), "endPort": int(source_end_port)} ]
                }

    rule = {
        "description" : description,
        "type": "APPLICATION",
        "spec": {
                "$objectType": "microseg.v4.config.NSPApplicationRuleSpec",
                "securedGroup": [secured_group_uuid],         
        }

    }
    rule.get("spec").update(source)
    rule.get("spec").update(inbound_services)

    print("Inbound Rule is , {}".format(rule))
    return rule


def create_outbound_rule_a1(secured_group_uuid,dest_type,dest_category_uuid,dest_subnet,dest_protocol,dest_network_ports,description=""):
    
    if dest_type == 'Category':
        if dest_category_uuid != None:
            dest = {"destCategories": [dest_category_uuid]}
        else:
            print("dest Category UUID is expected !!!")
            return False
    elif dest_type == 'Subnet':
        if dest_subnet != None:
            subnet = dest_subnet.split("/")
            network = subnet[0]
            mask = int(subnet[1])
            dest = {"destSubnet" : {"value" : network,"prefixLength": mask}}
        else:
            print("dest Subnet CIDR is expected !!!")
            return False
    elif dest_type == 'All':
        dest = {"destAllowSpec":"ALL"}
    else:
        print("Invalid dest Type !!!")
        return False

    protocol_mapping = {"TCP": "tcpServices","UDP":"udpServices"}
    dest_start_port = dest_network_ports[0]
    dest_end_port = dest_network_ports[1] if len(dest_network_ports)>1 else dest_network_ports[0]

    if dest_protocol == 'All':
        outbound_services = { "isAllProtocolAllowed" : True }
    else:
        outbound_services = {
                    protocol_mapping[dest_protocol]:[ {"startPort": int(dest_start_port), "endPort": int(dest_end_port)} ]
                }

    rule = {
        "description" : description,
        "type": "APPLICATION",
        "spec": {
                "$objectType": "microseg.v4.config.NSPApplicationRuleSpec",
                "securedGroup": [secured_group_uuid],         
        }

    }
    rule.get("spec").update(dest)
    rule.get("spec").update(outbound_services)

    print("outbound Rule is , {}".format(rule))
    return rule
    
def create_intragroup_rule_a1(secured_group_uuid,secured_group_action):
    rule = {
        "type": "INTRA_GROUP",
        "spec" : {
            "$objectType": "microseg.v4.config.NSPIntraEntityGroupRuleSpec",
            "securedGroup" : [secured_group_uuid],
            "securedGroupAction" : secured_group_action
        }
    }
    print("IntraGroup Rule is , {}".format(rule))
    return rule


def create_secuity_policy_v4_a1(api_server,username,secret,name,rules,type="APPLICATION",description="",state="MONITOR",isHitlogEnabled=False,isIpv6TrafficAllowed=False,secure=False):

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'NTNX-Request-Id' : str(uuid.uuid4())
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/microseg/v4.0.a1/config/policies"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "POST"

    # Compose the json payload
    payload = {
        "name" : name, 
        "type" : type,
        "description": description,
        "state": state,
        "isHitlogEnabled":isHitlogEnabled,
        "isIpv6TrafficAllowed" :isIpv6TrafficAllowed,
        "rules" : rules
    }    

    print("payload is ",payload)

    resp = process_request(url=url,method=method,payload=payload,user=username,password=secret,headers=headers,secure=secure)
    if resp.ok:
        return json.loads(resp.content)
    else:
        print("Failure")
        return False
