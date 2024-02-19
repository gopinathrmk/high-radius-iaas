################################################
############ pc_tasks.py            ############
################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################

def prism_monitor_task_apiv4(api_server,username,secret,task_uuid,secure=False):

    """Given a Prism Central task uuid, loop until the task is completed
    exits if the task fails

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        task_uuid: Prism Central task uuid (generally returned by another action 
                   performed on PC).
        secure: boolean to verify or not the api server's certificate (True/False)
                   
    Returns:
        No value is returned
    """
    
    task_status_details = {}
    task_status = "RUNNING"

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/api/prism/v4.0.a1/config/tasks/{0}".format(task_uuid)
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    print("Making a {} API call to {}".format(method, url))
    
    while True:
        resp = process_request(url,method,user=username,password=secret,headers=headers,secure=secure)
        #print(json.loads(resp.content))
        if resp.ok:
            task_status_details = json.loads(resp.content)
            task_status = task_status_details.get('data',{}).get('status')
            task_prog_percent = task_status_details.get('data',{}).get('progressPercentage')
            task_sub_steps = task_status_details.get('data',{}).get('subSteps')
            if task_status == "SUCCEEDED":
                print ("Task has completed successfully")
                return task_status_details
            elif task_status == "FAILED":
                error_message = task_status_details.get("data",{}).get("errorMessages",None)
                legacy_error = task_status_details.get("data",{}).get("legacyErrorMessage",None)
                print ("Task has failed !!!\nError Message: {} \nLegacyErrorMsg: {}".format(error_message,legacy_error) )
                exit(1)
            else:
                print ("Task status is {} and percentage completion is {}. \nWaiting for 30 seconds.".format(task_status,task_prog_percent))
                if task_sub_steps:
                    print("\nSteps Completed: {}".format(task_sub_steps)) 
                sleep(30)
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
            exit(resp.status_code)


