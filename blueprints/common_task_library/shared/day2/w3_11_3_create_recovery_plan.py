
############# Calm imports #################################################################
# CALM_USES pc_recovery_plan.py
# CALM_USES pc_tasks.py
# CALM_USES pc_projects.py
# CALM_USES pc_clusters.py
############################################################################################

PC_PROVIDER_ADDRESS = '@@{PC_PROVIDER_ADDRESS}@@'
PC_PROVIDER_USERNAME = "@@{PC_PROVIDER_USERNAME}@@"
PC_PROVIDER_SECRET = "@@{PC_PROVIDER_SECRET}@@"
PC_PROVIDER_SECURE = False

calm_app_name = '@@{calm_application_name}@@'

#Category 
vm_category = {"CalmApplication" : calm_app_name} 
rp_name = "RP_" + calm_app_name + "@@{calm_now}@@".split()[0]
if ("@@{calm_array_index}@@" != "0" ):
    print("Exiting for @@{calm_array_index}@@ index")
    exit(0)

az_list = pc_get_az_urls(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE)
print("az_list : \n {}".format(az_list))

local_az_url = " "
#recovery_az_url = ""
for az in az_list:
    #Assume only one PC for both primary and remote site 
    if az['type'] == "kLocal":
        local_az_url = az['url']
#    if az['type'] == 'kPC':
#        recovery_az_url = az['url']

#recovery_az_url = primary_az_url #since there is single PC 
SELF_SERVICE_ADDRESS  = "@@{SELF_SERVICE_ADDRESS}@@"
SELF_SERVICE_USERNAME = "@@{SELF_SERVICE_USERNAME}@@"
SELF_SERVICE_SECRET   = "@@{SELF_SERVICE_SECRET}@@"
CALM_PROJECT_NAME     = "@@{calm_project_name}@@"
SELF_SERVICE_SECURE   =  @@{SELF_SERVICE_SECURE}@@

project_uuid, project = prism_get_project(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,secure=SELF_SERVICE_SECURE,project_name=CALM_PROJECT_NAME)
primary_cluster_uuid = "@@{platform.status.cluster_reference.uuid}@@"
recovery_cluster_uuid = [ x['uuid'] for x in project['spec']['resources']['cluster_reference_list'] if x['uuid'] != primary_cluster_uuid ][0]
tenant_vpc_uuid = project['spec']['resources']['vpc_reference_list'][0]['uuid']
subnet_nic1 = project['spec']['resources']['external_network_list'][0]['name']
subnet_nic2 = project['spec']['resources']['external_network_list'][1]['name']
print(recovery_cluster_uuid,tenant_vpc_uuid,subnet_nic1,subnet_nic2)

#Create Recovery Plan 
json_resp = pc_create_recovery_plan(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,
                               rp_name=rp_name,local_az_url=local_az_url,primary_cluster_uuid=primary_cluster_uuid,recovery_cluster_uuid=recovery_cluster_uuid,
                               tenant_vpc_uuid=tenant_vpc_uuid,subnet_nic1=subnet_nic1,subnet_nic2=subnet_nic2,vm_category=vm_category,)

task_uuid = json_resp['status']['execution_context']['task_uuid']
rp_uuid = json_resp['metadata']['uuid']
prism_monitor_task_apiv3(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,task_uuid=task_uuid)


print("rp_name={}".format(rp_name))
print("local_az_url={}".format(local_az_url))
print("primary_cluster_uuid={}".format(primary_cluster_uuid))
print("recovery_cluster_uuid={}".format(recovery_cluster_uuid))

#print("recovery_az_url={}".format(recovery_az_url))
