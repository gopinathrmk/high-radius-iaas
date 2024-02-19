############# Calm imports #################################################################
# CALM_USES http_requests.py, pc_projects.py, pc_ssp_environments.py
############################################################################################

SELF_SERVICE_ADDRESS = '@@{SELF_SERVICE_ADDRESS}@@'
SELF_SERVICE_USERNAME = '@@{SELF_SERVICE_USERNAME}@@'
SELF_SERVICE_SECRET = '@@{SELF_SERVICE_SECRET}@@'
SELF_SERVICE_SECURE = @@{SELF_SERVICE_SECURE}@@

CALM_PROJECT_NAME = '@@{PROJECT_NAME}@@'

project_uuid, project = prism_get_project(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,project_name=CALM_PROJECT_NAME,project_uuid=None,secure=SELF_SERVICE_SECURE)

project_account_uuid = project['spec']['resources']['account_reference_list'][0]['uuid']

print("######## Fetching Remote AHV Account Prism Central Address ##################")
account_uuid, account_data = prism_ssp_get_account(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,account_name=None,account_uuid=project_account_uuid,secure=SELF_SERVICE_SECURE)
account_server = account_data['spec']['resources']['data']['server']
account_name = account_data['spec']['name']

print('Calm Account UUID is {}'.format(account_uuid))
print('Calm Account Server is {}'.format(account_server))
print('Calm Account Name is {}'.format(account_name))
PC_PROVIDER_ADDRESS = account_server

print("PC_PROVIDER_ADDRESS={}".format(account_server))
print("######## Remote AHV Account Prism Central Address fetched successfully ##################")