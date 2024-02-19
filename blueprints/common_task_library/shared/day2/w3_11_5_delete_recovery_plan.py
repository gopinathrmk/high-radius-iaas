################## Calm Imports ####################
# CALM_USES pc_entities.py
# CALM_USES pc_tasks.py
################################################

PC_PROVIDER_ADDRESS = '@@{PC_PROVIDER_ADDRESS}@@'
PC_PROVIDER_USERNAME = "@@{PC_PROVIDER_USERNAME}@@"
PC_PROVIDER_SECRET = "@@{PC_PROVIDER_SECRET}@@"
PC_PROVIDER_SECURE = False

rp_name = '@@{rp_name}@@'

if ("@@{calm_array_index}@@" != "0" ):
    print("Exiting for @@{calm_array_index}@@ index")
    exit(0)

#Delete Recovery Plan on Primary Site 
task_uuid = prism_delete_entity(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,
                                 entity_type="recovery_plan",entity_api_root="recovery_plans", entity_name=rp_name)

prism_monitor_task_apiv3(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,task_uuid=task_uuid)

