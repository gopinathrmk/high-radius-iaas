################################################
############ pc_recovery_plan.py            ############
################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################
from datetime import datetime 

def pc_get_az_urls(api_server,username,secret,secure=False):
    """ Retrieve Availability Zone URL (UUID) from Prism Central

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password. 
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        List of AZ info containing name, type and AZ url (UUID)

    """
    az_list = []
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/groups"
    url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint)
    method = "POST"

    # Compose the json payload
    payload = {
        "entity_type": "availability_zone",
        "group_attributes": [
        ],
        "group_count": 3,
        "group_member_attributes": [
            {
                "attribute": "name"
            },
            {
                "attribute": "region"
            },
            {
                "attribute": "type"
            },
            {
                "attribute": "reachable"
            },
            {
                "attribute": "cloud_trust_uuid"
            },
            {
                "attribute": "url"
            }
        ],
        "group_member_count": 40,
        "group_member_offset": 0,
        "group_member_sort_attribute": "name",
        "group_member_sort_order": "ASCENDING",
        "group_offset": 0,
        "grouping_attribute": " "
    }

    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        json_resp = json.loads(resp.content)
        print("json_resp: {}".format(json_resp))
        for entity in json_resp['group_results'][0]['entity_results']:
            az_name = ""
            az_type = ""
            az_url = ""
            for data in entity['data']:
                if data['name'] == 'name':
                    az_name = data['values'][0]['values'][0]
                if data['name'] == 'type':
                    az_type = data['values'][0]['values'][0]
                if data['name'] == 'url':
                    az_url = data['values'][0]['values'][0]
            az = {'name': az_name, 'type': az_type, 'url': az_url}
            az_list.append(az)
        
        return(az_list)

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


def pc_create_recovery_plan(api_server,username,secret,rp_name,local_az_url,primary_cluster_uuid,recovery_cluster_uuid,tenant_vpc_uuid,subnet_nic1,subnet_nic2,vm_category=None,secure=False):
    """ Create Recovery Plan using category 

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password. 
        rp_name : Name of Recovery plan
        local_az_url : URL(UUID) of local availability zone 
        vm_category : Dict containing category key and value. VM tagged with this category will be added to RP. 
                        If category is none, RP without VM entity will be created.
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        Task execution (json response).
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/recovery_plans"
    url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint)
    method = "POST"

    # Compose the json payload
    payload = {
        "metadata": {
            "kind": "recovery_plan"
        },
        "spec": {
            "name": rp_name,
            "resources": {
                "parameters": {
                    "availability_zone_list": [
                        {
                            "availability_zone_url": local_az_url,
                            "cluster_reference_list" : [
                                {"uuid": primary_cluster_uuid,"kind": "cluster"}
                            ]
                        },
                        {
                            "availability_zone_url": local_az_url,
                            "cluster_reference_list" : [
                                {"uuid": recovery_cluster_uuid,"kind": "cluster"}
                            ]

                        }
                    ],
                    "primary_location_index": 0,
                    "network_mapping_list": [
                        {
                        "availability_zone_network_mapping_list": [
                            {
                                "cluster_reference_list": [
                                    {
                                       "kind": "cluster",
                                    #   "name": "VWDEWOBNXIVB4APP01",
                                        "uuid": primary_cluster_uuid
                                    }
                                ],
                                "recovery_network": {
                                    #"virtual_network_reference": {
                                    #    "kind": "virtual_network",
                                    #    "name": "vfr7wxq",
                                    #    "uuid": "44f0ba70-5623-437c-91bc-5ccbfcbc5c92"
                                    #},
                                    "vpc_reference": {
                                        "kind": "vpc",
                                    #    "name": "vfr7wxq",
                                        "uuid": tenant_vpc_uuid
                                    },
                                    "name": subnet_nic1,
                                    #"subnet_list": [
                                    #    {
                                    #        "gateway_ip": "10.5.0.1", #to chek how if its mandate 
                                    #        "external_connectivity_state": "DISABLED",
                                    #        "prefix_length": 28
                                    #    }
                                    #]
                                },
                                "availability_zone_url": local_az_url
                            }, 
                            {
                                "cluster_reference_list": [
                                    {
                                        "kind": "cluster",
                                    #    "name": "VWDEWOBNXIVB5APP01",
                                        "uuid": recovery_cluster_uuid
                                    }
                                ],
                                "recovery_network": {
                                    #"virtual_network_reference": {
                                    #    "kind": "virtual_network",
                                    #    "name": "vfr7wxq",
                                    #    "uuid": "44f0ba70-5623-437c-91bc-5ccbfcbc5c92"
                                    #},
                                    "vpc_reference": {
                                        "kind": "vpc",
                                    #    "name": "vfr7wxq",
                                        "uuid": tenant_vpc_uuid
                                    },
                                    "name": subnet_nic1,
                                    #"subnet_list": [
                                    #    {
                                    #        "gateway_ip": "10.5.0.1",
                                    #        "external_connectivity_state": "DISABLED",
                                    #        "prefix_length": 28
                                    #    }
                                    #]
                                },
                                "availability_zone_url": local_az_url
                            }
                        ]
                    }, 
                    {
                        "availability_zone_network_mapping_list": [
                            {
                                "cluster_reference_list": [
                                    {
                                        "kind": "cluster",
                                    #    "name": "VWDEWOBNXIVB4APP01",
                                        "uuid": primary_cluster_uuid
                                    }
                                ],
                                "recovery_network": {
                                    #"virtual_network_reference": {
                                    #    "kind": "virtual_network",
                                    #    "name": "vfr7wxq",
                                    #    "uuid": "44f0ba70-5623-437c-91bc-5ccbfcbc5c92"
                                    #},
                                    "vpc_reference": {
                                        "kind": "vpc",
                                    #    "name": "vfr7wxq",
                                        "uuid": tenant_vpc_uuid
                                    },
                                    "name": subnet_nic2,
                                    #"subnet_list": [
                                    #    {
                                    #        "gateway_ip": "10.4.7.1",
                                    #        "external_connectivity_state": "DISABLED",
                                    #        "prefix_length": 28
                                    #    }
                                    #]
                                },
                                "availability_zone_url": local_az_url
                            }, 
                            {
                                "cluster_reference_list": [
                                    {
                                        "kind": "cluster",
                                    #    "name": "VWDEWOBNXIVB5APP01",
                                        "uuid": recovery_cluster_uuid
                                    }
                                ],
                                "recovery_network": {
                                    #"virtual_network_reference": {
                                    #    "kind": "virtual_network",
                                    #    "name": "vfr7wxq",
                                    #    "uuid": "44f0ba70-5623-437c-91bc-5ccbfcbc5c92"
                                    #},
                                    "vpc_reference": {
                                        "kind": "vpc",
                                    #    "name": "vfr7wxq",
                                        "uuid": tenant_vpc_uuid
                                    },
                                    "name": subnet_nic2,
                                    #"subnet_list": [
                                    #    {
                                    #        "gateway_ip": "10.4.7.1",
                                    #        "external_connectivity_state": "DISABLED",
                                    #        "prefix_length": 28
                                    #    }
                                    #]
                                },
                                "availability_zone_url": local_az_url
                            }
                        ]
                    }
                ]
                
                },
                "stage_list": [
                    {
                        "stage_work": {
                            "recover_entities": {
                                "entity_info_list": [
                                    {
                                        "categories": vm_category
                                    }
                                ]
                            }
                        }
                    }
                ],

                
            }
        }
    }
    if not vm_category:
        del payload['spec']['resources']['stage_list']
    
    print("payload is {}".format(payload))
    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    
    if resp.ok:
        json_resp = json.loads(resp.content)
        print("json_resp: {}".format(json_resp))
        return json_resp
    
    else:
        print("Request failed!")
        print("status code: {}".format(resp.status_code))
        print("reason: {}".format(resp.reason))
        print("text: {}".format(resp.text))
        print("elapsed: {}".format(resp.elapsed))
        print("headers: {}".format(resp.headers))
        print("payload: {}".format(payload))
        print(json.dumps(
            json.loads(resp.content),
            indent=4
        ))
        raise


def pc_start_failover(api_server,username,secret,local_az_url,primary_cluster_uuid,recovery_cluster_uuid,rp_name=None,rp_uuid=None,secure=False):
    """ Initiate Failover with Recovery plan Name or UUID 

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password. 
        rp_name: Name of the Recovery Plan (optional).
        rp_uuid: Uuid of the Recovery Plan (optional).
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        Task execution (json response). 
    """

    if rp_uuid is None and rp_name is None:
        print("Either the name or UUID of Entity is required to proceed !!! ")
        return False
    
    if rp_uuid is None and rp_name:
        rp_uuid = prism_get_entity_uuid(api_server=api_server,username=username,secret=secret,
                              entity_type="recovery_plan",entity_api_root="recovery_plans",entity_name=rp_name,secure=secure)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/nutanix/v3/recovery_plan_jobs"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "POST"

    rp_job_name = "Failover " + str(datetime.today())
    payload = {
        "metadata": {
           "kind" : "recovery_plan_job"
        },
        "spec": {
            "name": rp_job_name,
            "resources": {
                "recovery_plan_reference": { "uuid": rp_uuid, "kind" : "recovery_plan" },
                "execution_parameters": {
                    "action_type": "MIGRATE",
                    "failed_availability_zone_list": [
                            {
                                "availability_zone_url": local_az_url,
                                "cluster_reference_list" : [
                                    {"uuid": primary_cluster_uuid,"kind": "cluster"}
                                ]
                            }
                        ],
                    "recovery_availability_zone_list": [
                            {
                                "availability_zone_url": local_az_url,
                                "cluster_reference_list" : [
                                    {"uuid": recovery_cluster_uuid,"kind": "cluster"}
                                ]

                            }
                        ],
                     "should_continue_on_validation_failure": True
                }
            }
        }
    }


    print("Making a {} API call to {} with secure set to {}".format(method, url, secure))
    resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure,payload=payload)

    if resp.ok:
        json_resp = json.loads(resp.content)
        print("\n\n json resp: \n {} \n\n".format(json_resp))
    else:
        print("Request failed!")
        print("status code: {}".format(resp.status_code))
        print("reason: {}".format(resp.reason))
        print("text: {}".format(resp.text))
        print("raise_for_status: {}".format(resp.raise_for_status()))
        print("elapsed: {}".format(resp.elapsed))
        print("headers: {}".format(resp.headers))
        print(json.dumps(
            json.loads(resp.content),
            indent=4
        ))
        raise

    return json_resp

