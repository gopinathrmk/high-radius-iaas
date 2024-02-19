################################################
############ pc_user.py             ############
################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################

def pc_get_acp_user_id(api_server,username,secret,acp_user,secure=False):
    """
        Retrieves distinguished_name user entity_id on Calm

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        acp_user: Name of user to retrieve
        
    Returns:
        distinguished_name group id (string).
    """

    # region prepare the api call
    headers = {'Content-Type': 'application/json','Accept': 'application/json'}
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/groups"
    url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint)
    method = "POST"
    payload = {
        'entity_type':'abac_user_capability',
        'group_member_attributes':[{'attribute':'user_uuid'}],
        'query_name':'prism:BaseGroupModel',
        'filter_criteria':'username=={}'.format(acp_user)
    }
    # endregion

    # Making the call
    print("Retreiving user uuid {}".format(acp_user))
    print("Making a {} API call to {}".format(method, url))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
	    json_resp = json.loads(resp.content)
    else:
        return None
   
    if json_resp['group_results']:
        return json_resp['group_results'][0]['entity_results'][0]['entity_id']
    else:
        return None

def pc_calm_search_users(api_server,username,secret,directory_service_uuid,search_name,secure=False):
    """
        Retrieves distinguished_name group on Prism Central

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        directory_service_uuid: Uuid of the directory service
        group_name: group name to retrieve on the directory service
        
    Returns:
        distinguished_name group (string).
    """
    
    # region prepare the api call
    headers = {'Content-Type': 'application/json','Accept': 'application/json'}
    api_server_port = "9440"
    api_server_endpoint = "/api/calm/v3.0/calm_users/search"
    url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint)
    method = "POST"
    payload = {
        'query':search_name,
        'provider_uuid': directory_service_uuid,
        'user_type':"ACTIVE_DIRECTORY",
        'is_wildcard_search':True
    }
    # endregion

    # Making the call
    print("Retrieving {} uuid".format(search_name))
    print("Making a {} API call to {}".format(method, url))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
	    json_resp = json.loads(resp.content)
    else:
        return None

    # filterng
    search_value = None
    for entity in json_resp['search_result_list']:
        if entity['type'] == "Group":
            for attribute in entity['attribute_list']:
                if attribute['name'] == "distinguishedName":
                    search_value = attribute['value_list'][0]
        elif entity['type'] == "Person":
            for attribute in entity['attribute_list']:
                if attribute['name'] == "userPrincipalName":
                    search_value = attribute['value_list'][0]
    
    # return
    return search_value

DEVELOPER = [
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "image"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "marketplace_item"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "app_icon"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "category"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "app_task"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "app_variable"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "virtual_network"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "resource_type"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "custom_provider"},
        "right_hand_side": {"collection": "ALL"},
    },
]

OPERATOR = [
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "app_icon"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "category"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "resource_type"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "custom_provider"},
        "right_hand_side": {"collection": "ALL"},
    },
]

CONSUMER = [
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "image"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "marketplace_item"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "app_icon"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "category"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "app_task"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "app_variable"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "virtual_network"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "resource_type"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "custom_provider"},
        "right_hand_side": {"collection": "ALL"},
    },
]

PROJECT_ADMIN = [
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "image"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "marketplace_item"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "directory_service"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "role"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"uuid_list": []},
        "left_hand_side": {"entity_type": "project"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "user"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "user_group"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "SELF_OWNED"},
        "left_hand_side": {"entity_type": "environment"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "app_icon"},
    },
    {
        "operator": "IN",
        "right_hand_side": {"collection": "ALL"},
        "left_hand_side": {"entity_type": "category"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "app_task"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "app_variable"},
        "right_hand_side": {"collection": "SELF_OWNED"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "virtual_network"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "resource_type"},
        "right_hand_side": {"collection": "ALL"},
    },
    {
        "operator": "IN",
        "left_hand_side": {"entity_type": "custom_provider"},
        "right_hand_side": {"collection": "ALL"},
    },
]

CUSTOM_ROLE_PERMISSIONS_FILTERS = [
    {
        "permission": "view_image",
        "filter": {
            "operator": "IN",
            "left_hand_side": {"entity_type": "image"},
            "right_hand_side": {"collection": "ALL"},
        },
    },
    {
        "permission": "view_app_icon",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "app_icon"},
        },
    },
    {
        "permission": "view_name_category",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "category"},
        },
    },
    {
        "permission": "create_or_update_name_category",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "category"},
        },
    },
    {
        "permission": "view_environment",
        "filter": {
            "operator": "IN",
            "left_hand_side": {"entity_type": "environment"},
            "right_hand_side": {"collection": "SELF_OWNED"},
        },
    },
    {
        "permission": "view_marketplace_item",
        "filter": {
            "operator": "IN",
            "left_hand_side": {"entity_type": "marketplace_item"},
            "right_hand_side": {"collection": "SELF_OWNED"},
        },
    },
    {
        "permission": "view_user",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "user"},
        },
    },
    {
        "permission": "view_user_group",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "user_group"},
        },
    },
    {
        "permission": "view_role",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "role"},
        },
    },
    {
        "permission": "view_directory_service",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "directory_service"},
        },
    },
    {
        "permission": "search_directory_service",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "directory_service"},
        },
    },
    {
        "permission": "view_identity_provider",
        "filter": {
            "operator": "IN",
            "right_hand_side": {"collection": "ALL"},
            "left_hand_side": {"entity_type": "identity_provider"},
        },
    },
    {
        "permission": "view_app_task",
        "filter": {
            "operator": "IN",
            "left_hand_side": {"entity_type": "app_task"},
            "right_hand_side": {"collection": "SELF_OWNED"},
        },
    },
    {
        "permission": "view_app_variable",
        "filter": {
            "operator": "IN",
            "left_hand_side": {"entity_type": "app_variable"},
            "right_hand_side": {"collection": "SELF_OWNED"},
        },
    },
    {
        "permission": "view_image",
        "filter": {
            "operator": "IN",
            "left_hand_side": {"entity_type": "resource_type"},
            "right_hand_side": {"collection": "ALL"},
        },
    },
    {
        "permission": "view_image",
        "filter": {
            "operator": "IN",
            "left_hand_side": {"entity_type": "custom_provider"},
            "right_hand_side": {"collection": "ALL"},
        },
    },
]

DEFAULT_CONTEXT = {
    "scope_filter_expression_list": [
        {
            "operator": "IN",
            "left_hand_side": "PROJECT",
            "right_hand_side": {"uuid_list": []},
        }
    ],
    "entity_filter_expression_list": [
        {
            "operator": "IN",
            "left_hand_side": {"entity_type": "ALL"},
            "right_hand_side": {"collection": "ALL"},
        }
    ],
}


def get_filter_list(role,project_uuid, cluster_uuids=None):

    # Default context for acp
    default_context = DEFAULT_CONTEXT

    # Setting project uuid in default context
    default_context["scope_filter_expression_list"][0]["right_hand_side"]["uuid_list"] = [project_uuid]

    entity_filter_expression_list = []
    if role == "Project Admin":
        entity_filter_expression_list = PROJECT_ADMIN
        entity_filter_expression_list[4]["right_hand_side"]["uuid_list"] = [
            project_uuid
        ]

    elif role == "Developer":
        entity_filter_expression_list = DEVELOPER

    elif role == "Consumer":
        entity_filter_expression_list = CONSUMER

    elif role == "Operator" and cluster_uuids:
        entity_filter_expression_list = OPERATOR

    else: #TODO work on custom Roles
        pass
        #entity_filter_expression_list = get_filters_custom_role(role_uuid, client)

    if cluster_uuids:
        entity_filter_expression_list.append(
            {
                "operator": "IN",
                "left_hand_side": {"entity_type": "cluster"},
                "right_hand_side": {"uuid_list": cluster_uuids},
            }
        )

    context_list = [default_context]
    if entity_filter_expression_list:
        context_list.append(
            {"entity_filter_expression_list": entity_filter_expression_list}
        )

    filter_list = {"context_list": context_list}
    return filter_list


def pc_set_project_acp_user(api_server,username,secret,project_uuid,acp_user_id,user_role_uuid,role_name,secure=False):
    """
        Set group and role on a given Calm project

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        project_uuid: Uuid of the project.
        acp_user_id: user entity id to add to the calm project.
        user_role_uuid: role uuid to add to the calm project.
        
    Returns:
        Task execution (json response).
    """

    #region prepare the api call
    headers = {'Content-Type': 'application/json','Accept': 'application/json'}
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/projects_internal/{}".format(project_uuid)
    url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint)
    method = "GET"
    # endregion

    # get project_json details first
    print("Retrieving project {} details on {}".format(project_uuid,api_server))
    print("Making a {} API call to {}".format(method, url))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers)
    if resp.ok:
        project_json = json.loads(resp.content)
    else:
        return None

    #project_json = resp
    
    user = {'kind': 'user','uuid': acp_user_id}
    # update existing access_control_policy_list
    found = False
    for acccess_control_policy in project_json['spec']['access_control_policy_list']:
        operation = {'operation': "UPDATE"}
        acccess_control_policy.update(operation)
        user_ref_list = acccess_control_policy['acp']['resources']['user_reference_list']
        acp_role_id = acccess_control_policy['acp']['resources']['role_reference']['uuid']
        if acp_role_id == user_role_uuid:
            user_ref_list.append(user)
            found= True 
            break
        
    
    if not found:
        #print("Not Found")
        #create new ACP payload and append to acp_list 
        filter_list = get_filter_list(role_name,project_uuid)
        add_acp_user = {
                        'operation': 'ADD',
                        'acp': {
                            'name': 'nuCalmAcp-'+str(uuid.uuid4()),
                            'description': 'ACPDescription-'+str(uuid.uuid4()),
                            'resources': {
                                'role_reference': {
                                    'uuid': user_role_uuid,
                                    'kind': 'role'
                                },
                                'user_reference_list': [
                                    {
                                        'kind': 'user',
                                        'uuid': acp_user_id
                                    }
                                ],
                                'filter_list': filter_list
                                }
                            
                            },
                        'metadata': {'kind': 'access_control_policy'}
                        }

        project_json['spec']['access_control_policy_list'].append(add_acp_user)

    project_json['spec']['project_detail']['resources']['user_reference_list'].append(user)

    # update json
    project_json.pop('status', None) # don't need status for the update
    #project_json['metadata'].pop('owner_reference', None)
    #project_json['metadata'].pop('create_time', None)
    payload = project_json
    
    #print("The payload is \n")
    #print(payload)
    
    # Making the call
    method = "PUT"
    print("Updating project {} details on {}".format(project_uuid,api_server))
    print("Making a {} API call to {}".format(method, url))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,payload=payload)

    if resp.ok:
        return json.loads(resp.content)
    else:
        return None