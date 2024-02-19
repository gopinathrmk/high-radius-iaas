############# Calm imports #################################################################
# CALM_USES pc_entities.py
# CALM_USES pc_recovery_plan.py
# CALM_USES pc_tasks.py
############################################################################################

PC_PROVIDER_ADDRESS = '@@{PC_PROVIDER_ADDRESS}@@'
PC_PROVIDER_USERNAME = "@@{PC_PROVIDER_USERNAME}@@"
PC_PROVIDER_SECRET = "@@{PC_PROVIDER_SECRET}@@"
PC_PROVIDER_SECURE = False

rp_name = '@@{rp_name}@@'
local_az_url = '@@{local_az_url}@@'
primary_cluster_uuid = '@@{primary_cluster_uuid}@@'
recovery_cluster_uuid = '@@{recovery_cluster_uuid}@@'

if ("@@{calm_array_index}@@" != "0" ):
    print("Exiting for @@{calm_array_index}@@ index")
    exit(0)
    
#Initiate Failover on Recovery Site 
json_resp = pc_start_failover(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,
                              rp_name=rp_name,local_az_url=local_az_url,primary_cluster_uuid=primary_cluster_uuid,recovery_cluster_uuid=recovery_cluster_uuid,)
task_uuid = json_resp['task_uuid']
prism_monitor_task_apiv3(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,task_uuid=task_uuid)
