################################################
############ pc_ssp_applications.py ############
################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py, http_requests.py
############################################################################################

def prism_ssp_get_apps(api_server, username, secret, secure=False, print_f=True, filter=None):

    """Retrieve the list of Applications from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of apps (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="app",entity_api_root="apps",secure=secure,print_f=print_f,filter=filter)


def prism_ssp_get_app(api_server,username,secret,app_name=None,app_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given app name.
       If a app_uuid is specified, it will skip retrieving all apps (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        app_name: Name of the app (optional).
        app_uuid: Uuid of the app (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the app (app_uuid) and the json content
        of the app details (app)
    """

    app_uuid, app = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="app",entity_api_root="apps",entity_name=app_name,entity_uuid=app_uuid,
                              secure=secure,print_f=print_f)
    return app_uuid, app


def prism_ssp_monitor_app_provisioning(api_server, username, secret, application_uuid, nbRetiries, waitInterval, secure=False):

    """Given an application uuid, loop until the application deployment finishes
    exits with error if the deployment fails

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        application_uuid: uuid of the application for which the deployment is monitored
        nbRetiries: number of retries before timeout
        waitInterval: wait interval (in seconds) between retries
        secure: boolean to verify or not the api server's certificate (True/False)
                   
    Returns:
        No value is returned
    """
 
    for x in range(nbRetiries):
        url = "https://{}:9440/api/nutanix/v3/apps/{}".format(api_server, application_uuid)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }    
        r = process_request(url=url, method="GET", user=username, password=secret, headers=headers, payload=None, secure=secure)
        if r.ok:
            resp = json.loads(r.content)
            if resp["status"]["state"].lower() == "error" or resp["status"]["state"].lower() == "failure" :
                print("Application deployment failed.")
                exit(1)
            elif resp["status"]["state"].lower() == "running":
                print("Application deployment finished with success.")
                return
            else:
                print("Application deployment still in progress, waiting...")
                sleep(waitInterval)
        else:
            print("Could not check status for application {}. please check status on Calm interface. exiting Execution".format(application_uuid))
            exit(1)


def prism_ssp_get_apps_in_project(api_server, username, secret, project_name, secure=False, print_f=True, filter=None):

    """Retrieve the list of Applications in a specified project from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        project_name: project for which the apps are fetched
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of apps entities (entities part of the json response).
    """

    apps = prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="app",entity_api_root="apps",secure=secure,print_f=print_f,filter=filter)
    return [
        app for app in apps if app["metadata"]["project_reference"]["name"]==project_name
    ]


def prism_ssp_get_vms_in_app(api_server, username, secret, application_name=None ,app_uuid=None, hypervisor_type=None, secure=False, print_f=True, filter=None):

    """Retrieve the list of VMs platform data in a specified application from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        app_name: Name of the app for which the VMs are fetched (optional).
        app_uuid: Uuid of the app for which the VMs are fetched (optional).
        hypervisor_type: type of hypervisor to filter VMs on. Optional. Condition omitted if 'None'. for example use "AHV_VM" to return only AHV VMs
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of apps entities (entities part of the json response).
    """
    app_uuid, app = prism_ssp_get_app(api_server=api_server,username=username,secret=secret,
                                      app_name=application_name,app_uuid=app_uuid,secure=secure,print_f=print_f)
    VM_list = []
    for deployment in app["status"]["resources"]["deployment_list"]:
        VM_list.extend(
            [
                json.loads(vm["platform_data"]) for vm in deployment["substrate_configuration"]["element_list"]
                                                    if vm["type"] == (hypervisor_type if hypervisor_type else vm["type"])
            ]
        )
    return VM_list


def prism_ssp_delete_app(api_server,username,secret,app_name=None,app_uuid=None,secure=False,print_f=True):

    """Deletes an app given app uuid or app name.
       If an app_uuid is specified, it will skip retrieving all entities to find uuid, by specifying the uuid in the arguments (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        app_type: kind (type) of app as referenced in the app json object
        app_api_root: v3 apis root for this app type. for example. for projects the list api is ".../api/nutanix/v3/projects/list".
                         the app api root here is "projects"
        app_name: Name of the app (optional).
        app_uuid: Uuid of the app (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        No value is returned
    """

    prism_delete_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="app",entity_api_root="apps",entity_name=app_name,entity_uuid=app_uuid,
                              secure=secure,print_f=print_f)
