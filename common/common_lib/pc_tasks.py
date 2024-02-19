################################################
############ pc_tasks.py            ############
################################################

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################

def prism_monitor_task_apiv3(api_server,username,secret,task_uuid,secure=False):

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
    api_server_endpoint = "/api/nutanix/v3/tasks/{0}".format(task_uuid)
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
            task_status = resp.json()['status']
            if task_status == "SUCCEEDED":
                print ("Task has completed successfully")
                return task_status_details
            elif task_status == "FAILED":
                print ("Task has failed: {}".format(   resp.json()['error_detail'] if 'error_detail' in resp.json() else "No Info" )       )
                exit(1)
            else:
                print ("Task status is {} and percentage completion is {}. Current step is {}. Waiting for 30 seconds.".format(task_status,resp.json()['percentage_complete'],resp.json()['progress_message']))
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

    return task_status_details


def monitor_multiple_tasks_apiv3(api_server,username,secret,task_uuid_list, nb_retries=120, wait_interval=30, secure=False):

    """Given a Prism Central list of tasks uuids, loop until all tasks finish or some task fails
    exits if the one of the tasks fails

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        task_uuid_list: comma-separated list of tasks uuids
        nb_retries: number of retires before timeout
        wait_interval: interval between retries in seconds
        secure: boolean to verify or not the api server's certificate (True/False)

    Returns:
        No value is returned
    """

    if task_uuid_list == "":
        return
    for x in range(nb_retries):
        tasks_status_list = []
        for task_uuid in task_uuid_list.split(','):
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            api_server_port = "9440"
            api_server_endpoint = "/api/nutanix/v3/tasks/{0}".format(task_uuid)
            url = "https://{}:{}{}".format(
                api_server,
                api_server_port,
                api_server_endpoint
            )
            method = "GET"
            resp = process_request(url=url,method=method,user=username,password=secret,headers=headers,secure=secure)
            if resp.ok:
                task_status = resp.json()['status']
            else:
                print("ERROR - Failed to fetch task {} ".format(task_uuid))
            tasks_status_list.append(
                {
                    "uuid": task_uuid,
                    "state": task_status
                }
            )

        print(">>>>> current tasks status:")
        print(tasks_status_list)


        overall_state = "SUCCEEDED"
        for task_status in tasks_status_list:
            if task_status["state"].upper() == "FAILED":
                overall_state = "FAILED"
                print("Task {} failed.".format(task_status["uuid"]))
            elif task_status["state"].upper() != "SUCCEEDED" and overall_state != "FAILED":
                overall_state = "inprogress"
        if overall_state == "FAILED":
            print("ERROR - Some Tasks failed.")
            exit(1)
        elif overall_state == "SUCCEEDED":
            print("INFO - All tasks finished Successfully.")
            return
        else:
            print("INFO - Tasks are still in progress, waiting...")
            sleep(wait_interval)
    #here the monitoring times out
    print("ERROR - Tasks monitoring timed out")
    exit(1)

