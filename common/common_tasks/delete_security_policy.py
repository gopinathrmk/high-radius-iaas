############# Calm imports #################################################################
# CALM_USES pc_security_policy_v4.py
# CALM_USES pc_tasks_v4.py
############################################################################################

if ("@@{calm_array_index}@@" != "0" ):
    print("Exiting for @@{calm_array_index}@@ index")
    exit(0)

PC_PROVIDER_ADDRESS = '@@{PC_PROVIDER_ADDRESS}@@'
PC_PROVIDER_USERNAME = '@@{PC_PROVIDER_USERNAME}@@'
PC_PROVIDER_SECRET = '@@{PC_PROVIDER_SECRET}@@'
PC_PROVIDER_SECURE =  @@{PC_PROVIDER_SECURE}@@
calm_application_name = '@@{calm_application_name}@@'
zone_name = ["admin","prod"]
SECURED_GROUP_CATEGORY_NAME1 = "CalmApplication"
SECURED_GROUP_CATEGORY_NAME2 = "Subnet"

secured_group_app = {SECURED_GROUP_CATEGORY_NAME1 :calm_application_name}
secured_group_app_uuid = get_category_uuid_v4(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,
                                            category=secured_group_app)

print("Attempting to delete Security Policy associated with app:'{}'".format(calm_application_name))
for zone in zone_name:
    secured_group_subnet = {SECURED_GROUP_CATEGORY_NAME2 :zone}
    security_group_subnet_uuid = get_category_uuid_v4(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,
                                                category=secured_group_subnet)
    extId = pc_get_security_policy_by_secured_category(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,
                                                    secured_group_uuids=[secured_group_app_uuid,security_group_subnet_uuid])
    
    if extId:
        json_resp = pc_delete_security_policy_v4(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,secure=PC_PROVIDER_SECURE,extId=extId)
        if json_resp:
            task_uuid = json_resp.get("data",{}).get("extId")
            prism_monitor_task_apiv4(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,task_uuid=task_uuid,secure=PC_PROVIDER_SECURE)
            print("Network Security Policy '{}' Deleted Successfully !!!".format(extId))
        else:
            print("Network Security Policy '{}' Couldn't be Deleted !!! ".format(extId))   
#    else:
#        print("No Network Security Policy exists for entity'{} & {}'".format(secured_group_app,secured_group_subnet))

