################################################
############     pc_clusters.py     ############
################################################
### CALM_USES pc_entities.py

def prism_get_clusters(api_server,username,secret,secure=False,print_f=True,filter=None):

    """Retrieve the list of clusters from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
    Returns:
        A list of clusters (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="cluster",entity_api_root="clusters",secure=secure,print_f=print_f,filter=filter)


def prism_get_cluster(api_server,username,secret,cluster_name=None,cluster_uuid=None,secure=False,print_f=True):
    
    """Returns from Prism Central the uuid and details of a given cluster name.
       If a cluster_uuid is specified, it will skip retrieving all clusters (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        cluster_name: Name of the cluster(optional).
        cluster_uuid: Uuid of the cluster (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the cluster (cluster_uuid) and the json content
        of the cluster details (cluster_details)
    """

    cluster_uuid, cluster = prism_get_entity(api_server=api_server,username=username,secret=secret,
                                             entity_type="cluster",entity_api_root="clusters",entity_name=cluster_name,entity_uuid=cluster_uuid,
                                             secure=secure,print_f=print_f)
    return cluster_uuid, cluster


def prism_get_cluster_utilization_average(api_server,username,secret,average_period_days=30,secure=False):
    """Returns from Prism Element the average resource utilization over the given time period (30 days by default).
    This function retrieves CPU, Memory and Storage utilization metrics for the specified period and 
    computes the average for each metric.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        average_period_days: Number of days over which to calculate the average resource utilization.
                             Defaults to 30 days.
        
    Returns:
        The following integers:
            - For CPU utilization: cpu_utilization_average based on the metric hypervisor_cpu_usage_ppm
            - For Memory utilization: memory_utilization_average based on the metric hypervisor_memory_usage_ppm
            - For Storage utilization: storage_utilization_average based on the metric controller_num_iops
    """
    start_time_in_usecs = int(((datetime.now() + timedelta(days = -average_period_days)) - datetime(1970, 1, 1)).total_seconds() *1000000)
    end_time_in_usecs = int(((datetime.now() + timedelta(days = -1)) - datetime(1970, 1, 1)).total_seconds() *1000000)
    interval_in_secs = 60

    params = {
        "metrics" : "hypervisor_cpu_usage_ppm,hypervisor_memory_usage_ppm,controller_num_iops",
        "start_time_in_usecs" : start_time_in_usecs,
        "end_time_in_usecs" : end_time_in_usecs,
        "interval_in_secs" : interval_in_secs
    }
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = "9440"
    api_server_endpoint = "/PrismGateway/services/rest/v2.0/cluster/stats/"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    print("Making a {} API call to {}".format(method, url))
    resp = process_request(url,method,username,secret,headers,params=params,secure=secure)
    if resp.ok:
        cluster_metrics_values = json.loads(resp.content)
        cpu_metrics = [stat['values'] for stat in cluster_metrics_values['stats_specific_responses'] if stat['metric'] == "hypervisor_cpu_usage_ppm"]
        memory_metrics = [stat['values'] for stat in cluster_metrics_values['stats_specific_responses'] if stat['metric'] == "hypervisor_memory_usage_ppm"]
        storage_metrics = [stat['values'] for stat in cluster_metrics_values['stats_specific_responses'] if stat['metric'] == "controller_num_iops"]
        cpu_utilization_average = sum(cpu_metrics[0]) / len(cpu_metrics[0]) /10000
        memory_utilization_average = sum(memory_metrics[0]) / len(memory_metrics[0]) /10000
        storage_utilization_average = int(sum(storage_metrics[0]) / len(storage_metrics[0]))
        print("CPU Utilization Average for the last {} days is: {} %".format(average_period_days,round(cpu_utilization_average,2)))
        print("Memory Utilization Average for the last {} days is: {} %".format(average_period_days,round(memory_utilization_average,2)))
        print("Storage Utilization Average for the last {} days is: {} iops".format(average_period_days,storage_utilization_average))
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

    return cpu_utilization_average, memory_utilization_average, storage_utilization_average

