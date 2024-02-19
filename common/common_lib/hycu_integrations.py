########################################################################
############       hycu_integrations.py                     ############
########################################################################


############# Calm imports #################################################################
# CALM_USES http_requests.py, hycu_entities.py
############################################################################################


def hycu_assign_policy_to_vms(api_server_endpoint,username,secret,backup_policy_name,vms_uuid_list,secure=False):
    
    """Assigns a backup policy to a list of VMs given their uuids in HYCU

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        backup_policy_name: backup policy name
        vms_uuid_list: VMs uuids
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        No value returned
    """
    
    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'
    
    policy_uuid, policy = hycu_get_entity(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                          entity_api_root='policies',entity_name=backup_policy_name,entity_uuid=None,
                                          secure=secure)
        
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "POST"
    payload = {
        "vmUuidList": vms_uuid_list
    }

    url = '{}policies/{}/assign'.format(api_server_endpoint, policy_uuid)
    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        print("INFO - backup policy vms assigned")
    else:
        print("ERROR - occured while assigning VMs to backup policy")
        print("reason: {}".format(resp.reason))
        exit(1)


def hycu_backup_vms(api_server_endpoint,username,secret,vms_list,force_full=False,secure=False):
    
    """triggers backup of a list of VMs given their uuids in HYCU
    waits for any ongoing jobs on the selected VMs before triggering the backups

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        vms_list: list of vms hycu vms in the form:
            [
                {"uuid": <uuid>, "name": <name>},
                {"uuid": <uuid>, "name": <name>},
                ...
            ]
        force_full: True/False to force full backup
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        list of backup jobs uuids
    """

    # wait for any ongoing backups
    print("INFO - Waiting for any pending jobs on the selected VMs")
    # !!! IMPORTANT !!! - don't remove this wait step. Lauching backups on VMs with already running jobs
    #   will cause the function to return correspomding VM ids instead of job ids (the HYCU API works this way)
    #   which will cause the futiure job monitoring steps to fail !!!
    hycu_wait_vm_jobs(api_server_endpoint,username,secret,
                      vms_list=vms_list, nb_retries=120, wait_interval=30, fail_on_job_failure=False,
                      secure=secure)

    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'
        
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "POST"
    payload = {
        "uuidList": [vm["uuid"] for vm in vms_list],
        "forceFull": force_full
    }
    url = '{}schedules/backup'.format(api_server_endpoint)
    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        print("INFO - backup of VMs initiated successfully")
        return json.loads(resp.content)["entities"]
    else:
        print("ERROR - occured while initiating VMs backup")
        print("reason: {}".format(resp.reason))
        exit(1)


def hycu_monitor_multiple_tasks(api_server_endpoint,username,secret,jobs_uuid_list, nb_retries=120, wait_interval=30, fail_on_job_failure=True, secure=False):

    """Given a HYCU list of jobs uuids, loop until all jobs finish or some jobs fail
    exits if one of the tasks fails, shows warnings or is aborted (depends on fail_on_job_failure)

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        jobs_uuid_list: list of jobs uuids
        nb_retries: number of retires before timeout
        wait_interval: interval between retries in seconds
        fail_on_job_failure: if set to true, exits with error if one of the jobs fails
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        No value is returned
    """

    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'

    if jobs_uuid_list == []:
        return
    for x in range(nb_retries):
        jobs_status_list = []
        for job_uuid in jobs_uuid_list:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            url = '{}jobs/{}'.format(api_server_endpoint, job_uuid)
            method = "GET"
            resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
            if resp.ok:
                resp_content = json.loads(resp.content)
                if "entities" in resp_content and resp_content["entities"]!=[]:
                    job_status = resp_content["entities"][0]["status"]
                    jobs_status_list.append(
                        {
                            "uuid": job_uuid,
                            "state": job_status
                        }
                    )
                else:
                    print("ERROR - Failed to fetch job {} ".format(job_uuid))
                    exit(1)
            else:
                print("ERROR - Failed to fetch job {} ".format(job_uuid))
                exit(1)

        print(">>>>> current jobs status:")
        print(jobs_status_list)

        overall_state = "OK"
        for job_status in jobs_status_list:
            if job_status["state"].upper() in ["ERROR", "ABORTED", "WARNING"]:
                overall_state = "FAILED"
                print("Job {} presented status {}".format(job_status["uuid"]))
            elif job_status["state"].upper() != "OK" and overall_state != "FAILED":
                overall_state = "inprogress"
        if overall_state == "FAILED":
            print("ERROR - Some Jobs failed, presented warnings or were aborted.")
            if fail_on_job_failure:
                exit(1)
        elif overall_state == "OK":
            print("INFO - All Jobs finished Successfully.")
            return
        else:
            print("INFO - Jobs are still in progress, waiting...")
            sleep(wait_interval)
    #here the monitoring times out
    print("ERROR - Jobs monitoring timed out")
    exit(1)


def hycu_wait_vm_jobs(api_server_endpoint,username,secret,vms_list, nb_retries=120, wait_interval=30, fail_on_job_failure=True, secure=False):

    """Given a HYCU list of VMs, loop until all running jobs on all VMs finish execution

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        vms_list: list of vms hycu vms in the form:
            [
                {"uuid": <uuid>, "name": <name>},
                {"uuid": <uuid>, "name": <name>},
                ...
            ]
        nb_retries: number of retires before timeout
        wait_interval: interval between retries in seconds
        fail_on_job_failure: if set to true, exits with error if one of the jobs from any VM fails
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        No value is returned
    """
    print("INFO - Checking existing jobs on following VMS")
    print([vm["name"] for vm in vms_list])

    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'

    if vms_list == []:
        return
    
    jobs_uuid_list = []

    all_jobs = hycu_get_entities(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                 entity_api_root="jobs",filter='status==QUEUED||EXECUTING',
                                 secure=secure)

    for job in all_jobs:
        job_uuid, job_details = hycu_get_entity(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                                entity_api_root="jobs",entity_name=None,entity_uuid=job["uuid"],
                                                secure=secure,print_f=False)
        job_vm_name = ""
        if "entityMap" in job_details and job_details["entityMap"] != None and "Original virtual machine" in job_details["entityMap"]:
            job_vm_name = job_details["entityMap"]["Original virtual machine"][0]
        job_status = ""
        if "status" in job_details:
            job_status  = job_details["status"]
        if job_status  in ["EXECUTING", "QUEUED", None] and job_vm_name in [vm["name"] for vm in vms_list]:
            jobs_uuid_list.append(job["uuid"])

    hycu_monitor_multiple_tasks(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                jobs_uuid_list=jobs_uuid_list, nb_retries=nb_retries, wait_interval=wait_interval, fail_on_job_failure=fail_on_job_failure,
                                secure=secure)



def hycu_add_user_to_usergroup(api_server_endpoint,username,secret,user_uuid,usergroup_uuid,role,secure=False):
    
    """Add user to usergroup in HYCU

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        user_uuid: user to be added to the HYCU group
        usergroup_uuid: usergroup where to add the user
        role: role to be assigned to user in this group
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        No value returned
    """
    
    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "POST"
    payload = None

    url = '{}users/{}/groups/{}/role/{}'.format(api_server_endpoint, user_uuid, usergroup_uuid, role)
    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        print("INFO - user added to group in HYCU")
    else:
        print("ERROR - occured while adding user to group")
        print("reason: {}".format(resp.reason))
        exit(1)


def hycu_remove_user_from_usergroup(api_server_endpoint,username,secret,user_uuid,usergroup_uuid,secure=False):
    
    """Remove user from usergroup in HYCU

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        user_uuid: user to be removed from the HYCU group
        usergroup_uuid: usergroup from which user is removed
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        No value returned
    """
    
    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "DELETE"
    payload = None

    url = '{}users/{}/groups/{}'.format(api_server_endpoint, user_uuid, usergroup_uuid)
    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        print("INFO - user removed from group in HYCU")
    else:
        print("ERROR - occured while removing user from group")
        print("reason: {}".format(resp.reason))
        exit(1)


def hycu_enable_disable_usergroup(api_server_endpoint,username,secret,group_name, action, secure=False):

    """Activate or de-activate a usergroup given its name 

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        group_name: usergroup name
        action: one value from "enable" or "disable"
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        No value is returned
    """

    group_uuid, group = hycu_get_entity(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                                entity_api_root="usergroups",entity_name=group_name,entity_uuid=None,
                                                secure=secure)
    
    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "POST"
    payload = None

    url = '{}usergroups/{}/{}'.format(api_server_endpoint, group_uuid, action)

    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        print("INFO - usergroup updated successfully")
    else:
        print("ERROR - occured while updating usergroup")
        print("reason: {}".format(resp.reason))
        exit(1)


def extract_hycu_username(user_name,id_provider_type):
    """extract the correct user name for HYCU API user creation

    Args:
        user_name: user name that may include suffixes (domain for example)
        id_provider_type: The HYCU provider type.
        
    Returns:
        Extracted user name value
    """

    if id_provider_type == "AD_USER":
        if '@' in user_name:
            return user_name.split('@')[0]
        elif '\\' in user_name:
            return user_name.split('\\')[1]
        else:
            return user_name
    else:
        return user_name


def hycu_convert_type_user_provider(provider_type):
    if provider_type == "ACTIVE_DIRECTORY":
        return "AD_USER"
    else:
        return "OIDC_USER"


def hycu_add_user_check_exists(api_server_endpoint,username,secret,user_name,id_provider,hycu_user_mfa,secure=False):

    """Add user to HYCU if user not already added

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        user_name: user to be created
        id_provider: added user's HYCU identity provider entity (HYCU API entity)
        hycu_user_mfa: dict of mfa parameters (true/false values) for the added user. In the form:
                {
                    "HYCU_USER_TOTP": false,
                    "HYCU_USER_FIDO": false,
                    "HYCU_USER_FORCEMFA": false
                }

        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        user uuid
    """
    
    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'

    print("INFO - Checking User {} already exists".format(user_name))

    check_list = []
    entity_list = hycu_get_entities(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                    entity_api_root="users",
                                    secure=secure)
    check_list = [
        user for user in entity_list if user["username"] == user_name
    ]

    if check_list == []:
        print("INFO - Adding user to HYCU.")
    else:
        print("INFO - User already in HYCU. Skipping user creation.")
        return check_list[0]["uuid"]
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "POST"
    payload = {
        "type": hycu_convert_type_user_provider(id_provider["type"]),
        "username": user_name,
        "totp": hycu_user_mfa["HYCU_USER_TOTP"],
        "fido": hycu_user_mfa["HYCU_USER_FIDO"],
        "forceMFA": hycu_user_mfa["HYCU_USER_FORCEMFA"],
        "identityProviderUuid": id_provider["uuid"]
    }

    # idp user id is same as username
    if id_provider["type"] == "OIDC_USER":
        payload["oidcTenantId"] = user_name

    url = '{}users'.format(api_server_endpoint)
    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure)
    if resp.ok:
        print("INFO - user {} added to HYCU".format(user_name))
        json_resp = json.loads(resp.content)
        return json_resp["entities"][0]["uuid"]
    else:
        print("ERROR - occured while creating user {}".format(user_name))
        print("reason: {}".format(resp.reason))
        exit(1)


def hycu_add_usergroup(api_server_endpoint,username,secret,usergroup_name,user_group_labels,secure=False,timeout=60):
 
    """Add usergroup to HYCU

    Args:
        api_server_endpoint: example: https://hycu.here.local:8443/rest/v1.0/
        username: The HYCU user name.
        secret: The HYCU user name password.
        usergroup_name: usergroup to be created
        user_group_labels: list of label assignments is the form:
            [
                {"key":"key1","value":"value1"},
                {"key":"key2","value":"value2"},
                ...
            ]
        secure: boolean to verify or not the api server's certificate (True/False) 
        
    Returns:
        Group uuid
    """
    
    if not api_server_endpoint.endswith('/'):
        api_server_endpoint += '/'
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    method = "POST"
    payload = {
        "name": usergroup_name,
        "description": "User group for tenant {}".format(usergroup_name),
        "userGroupLabelEx": user_group_labels
    }

    url = '{}usergroups'.format(api_server_endpoint)
    resp = process_request(url,method,user=username,password=secret,headers=headers,payload=payload,secure=secure,timeout=timeout)
    if resp.ok:
        print("INFO - user group {} added to HYCU".format(usergroup_name))
        json_resp = json.loads(resp.content)
    else:
        print("ERROR - occured while creating user group {}".format(usergroup_name))
        print("reason: {}".format(resp.reason))
        exit(1)
    group_uuid, group = hycu_get_entity(api_server_endpoint=api_server_endpoint,username=username,secret=secret,
                                        entity_api_root='usergroups',entity_name=usergroup_name,entity_uuid=None,
                                        secure=secure)
    return group_uuid
