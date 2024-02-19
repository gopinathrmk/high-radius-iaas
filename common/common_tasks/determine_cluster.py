############# Calm imports #################################################################
# CALM_USES http_requests.py, pc_projects.py, pc_entities.py, pc_clusters.py
############################################################################################
from datetime import datetime, timedelta

CLUSTER_SELECTION = '@@{CLUSTER_SELECTION}@@'

SELF_SERVICE_ADDRESS = '@@{SELF_SERVICE_ADDRESS}@@'
SELF_SERVICE_USERNAME = '@@{SELF_SERVICE_USERNAME}@@'
SELF_SERVICE_SECRET = '@@{SELF_SERVICE_SECRET}@@'
SELF_SERVICE_SECURE = False

PC_PROVIDER_ADDRESS = '@@{PC_PROVIDER_ADDRESS}@@'
PC_PROVIDER_USERNAME = '@@{PC_PROVIDER_USERNAME}@@'
PC_PROVIDER_SECRET = '@@{PC_PROVIDER_SECRET}@@'
PC_PROVIDER_SECURE = False

CALM_PROJECT_NAME = '@@{PROJECT_NAME}@@'

if CLUSTER_SELECTION == 'AUTO_SELECT':
    #* retrieve list of projects and locate ours
    #https://{{calm_vm_ip}}:9440/api/nutanix/v3/projects/list
    projects = prism_get_entities(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,entity_type="project",entity_api_root="projects")
    project = [project for project in projects if project['metadata']['name'] == CALM_PROJECT_NAME]
    project_clusters = project[0]['spec']['resources']['cluster_reference_list']
    project_clusters_uuids = [project_uuid['uuid'] for project_uuid in project_clusters]

    #* retrieve list of clusters managed by our Prism Central instance
    #https://{{pc_ip}}:9440/api/nutanix/v3/clusters/list
    pc_clusters = prism_get_entities(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,entity_type="cluster",entity_api_root="clusters")

    #* cross reference both lists to make sure we're only looking at applicable clusters
    relevant_clusters=[]
    for cluster in pc_clusters:
        if cluster['metadata']['uuid'] in project_clusters_uuids:
            relevant_clusters.append({"name":cluster['spec']['name'],"uuid":cluster['metadata']['uuid'],"external_ip":cluster['spec']['resources']['network']['external_ip']})

    #* query PE cluster stats v2 api for each cluster resource
    relevant_clusters_utilization_metrics=[]
    headers = {'Accept': 'application/json','Content-Type': 'application/json; charset=UTF-8'}
    for cluster in relevant_clusters:        
        cpu_utilization_percentage_average,memory_utilization_percentage_average,storage_utilization_iops_average = prism_get_cluster_utilization_average(api_server=cluster['external_ip'],username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,average_period_days=7,secure=PC_PROVIDER_SECURE)
        relevant_clusters_utilization_metrics.append({
            "cluster_name": cluster['name'],
            "cluster_uuid": cluster['uuid'],
            "memory_utilization_percentage_average": memory_utilization_percentage_average,
            "cpu_utilization_percentage_average": cpu_utilization_percentage_average,
            "storage_utilization_iops_average": storage_utilization_iops_average
        })

    #* identify the cluster with most available resources (memory first, then compute, then storage)
    memory_utilization_percentage_average=100
    cpu_utilization_percentage_average=100
    storage_utilization_iops_average=100000000
    cluster_name="none"
    for cluster in relevant_clusters_utilization_metrics:
        if cluster['memory_utilization_percentage_average'] < memory_utilization_percentage_average:
            #print("Cluster {} has more memory available {} than cluster {} which has {}".format(cluster['cluster_name'],cluster['available_logical_storage_bytes'],cluster_name,available_memory_bytes))
            cluster_name = cluster['cluster_name']
            cluster_uuid = cluster['cluster_uuid']
            memory_utilization_percentage_average = cluster['memory_utilization_percentage_average']
        if cluster['memory_utilization_percentage_average'] == memory_utilization_percentage_average:
            if cluster['cpu_utilization_percentage_average'] < cpu_utilization_percentage_average:
                cluster_name = cluster['cluster_name']
                cluster_uuid = cluster['cluster_uuid']
                cpu_utilization_percentage_average = cluster['cpu_utilization_percentage_average']
            if cluster['cpu_utilization_percentage_average'] == cpu_utilization_percentage_average:
                if cluster['storage_utilization_iops_average'] > storage_utilization_iops_average:
                    cluster_name = cluster['cluster_name']
                    cluster_uuid = cluster['cluster_uuid']
                    storage_utilization_iops_average = cluster['storage_utilization_iops_average']
        if cluster_name == "none":
            print("Could not determine target cluster!")
            exit(1)
else:
    cluster_name_selected = CLUSTER_SELECTION
    cluster_uuid, cluster_data = prism_get_cluster(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,cluster_name=cluster_name_selected,cluster_uuid=None,secure=PC_PROVIDER_SECURE)
    cluster_name = cluster_data['spec']['name']

print("######## Setting target_cluster variable ##################")
cluster_name = cluster_name
cluster_uuid = cluster_uuid
cluster={"name":cluster_name,"uuid":cluster_uuid}
print("target_cluster={}".format(json.dumps(cluster)))