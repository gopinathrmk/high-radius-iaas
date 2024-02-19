############# Calm imports #####################################################################
# CALM_USES pc_ssp_applications.py, hycu_integrations.py
################################################################################################

SELF_SERVICE_ADDRESS = '@@{SELF_SERVICE_ADDRESS}@@'
SELF_SERVICE_USERNAME = '@@{SELF_SERVICE_USERNAME}@@'
SELF_SERVICE_SECRET = '@@{SELF_SERVICE_SECRET}@@'
SELF_SERVICE_SECURE = @@{SELF_SERVICE_SECURE}@@

HYCU_ADDRESS = '@@{HYCU_ADDRESS}@@'
HYCU_USERNAME = '@@{HYCU_USERNAME}@@'
HYCU_SECRET = '@@{HYCU_SECRET}@@'
HYCU_SECURE = @@{HYCU_SECURE}@@

app_uuid = '@@{calm_application_uuid}@@'

print("######## Fetching application VMs ##################")
    
vms_to_backup = prism_ssp_get_vms_in_app(api_server=SELF_SERVICE_ADDRESS, username=SELF_SERVICE_USERNAME, secret=SELF_SERVICE_SECRET,
                        application_name=None, app_uuid=app_uuid, hypervisor_type="AHV_VM",
                        secure=SELF_SERVICE_SECURE, print_f=True, filter=None)
print('vms in list are {}'.format(vms_to_backup)) 
# get all VMs list from HYCU
hycu_vms_list = hycu_get_entities(api_server_endpoint=HYCU_ADDRESS, username=HYCU_USERNAME, secret=HYCU_SECRET,
                                entity_api_root="vms",
                                secure=HYCU_SECURE)

hycu_vms_to_backup = [
    {'uuid': vm['uuid'], 'name': vm['vmName']} for vm in hycu_vms_list if vm['externalId'] in [
                                                                                app_vm['metadata']['uuid'] for app_vm in vms_to_backup
                                                                            ]
]

print("######## Application VMs fetched successfully ##################")


print("######## Initiating backup of application VMs ##################")
jobs_uuid_list = hycu_backup_vms(api_server_endpoint=HYCU_ADDRESS, username=HYCU_USERNAME, secret=HYCU_SECRET,
                                 vms_list=hycu_vms_to_backup,force_full=False,
                                 secure=HYCU_SECURE)
print('Jobs uuid list is {}'.format(jobs_uuid_list))

print("######## backup of application VMs initiated ##################")

print("######## Monitoring backup jobs ##################")
hycu_monitor_multiple_tasks(api_server_endpoint=HYCU_ADDRESS, username=HYCU_USERNAME, secret=HYCU_SECRET,
                            jobs_uuid_list=jobs_uuid_list, nb_retries=360, wait_interval=10, 
                            secure=HYCU_SECURE)
print("######## backup jobs finished successfully ##################")