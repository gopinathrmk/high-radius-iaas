############# Calm imports #################################################################
# CALM_USES http_requests.py, pc_projects.py, pc_subnets.py
############################################################################################

SELF_SERVICE_ADDRESS = '@@{SELF_SERVICE_ADDRESS}@@'
SELF_SERVICE_USERNAME = '@@{SELF_SERVICE_USERNAME}@@'
SELF_SERVICE_SECRET = '@@{SELF_SERVICE_SECRET}@@'
SELF_SERVICE_SECURE = False

PC_PROVIDER_ADDRESS = '@@{PC_PROVIDER_ADDRESS}@@'
PC_PROVIDER_USERNAME = '@@{PC_PROVIDER_USERNAME}@@'
PC_PROVIDER_SECRET = '@@{PC_PROVIDER_SECRET}@@'
PC_PROVIDER_SECURE = False

CALM_PROJECT_NAME = '@@{PROJECT_NAME}@@'
SECURITY_ZONE = '@@{SECURITY_ZONE}@@'

project_uuid, project = prism_get_project(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,project_name=CALM_PROJECT_NAME,project_uuid=None,secure=SELF_SERVICE_SECURE)

if len(project['spec']['resources']['vpc_reference_list']) > 0:
    tenant_vpc_uuid = project['spec']['resources']['vpc_reference_list'][0]['uuid']
    print('tenant_vpc_uuid is {}'.format(tenant_vpc_uuid))
else:
    print('ERROR - VPC does not exist in the project')

print(project['spec']['resources']['subnet_reference_list'])
print(project['spec']['resources']['external_network_list'])

if len(project['spec']['resources']['subnet_reference_list']) > 0:
    networks = project['spec']['resources']['subnet_reference_list']
else:
    if len(project['spec']['resources']['external_network_list']) > 0:
        networks = project['spec']['resources']['external_network_list']

print('Networks are {}'.format(networks))

for subnet in networks:
    if SECURITY_ZONE in subnet['name']:
        print(subnet['name'])
        subnet_uuid = subnet['uuid']
        subnet_uuid, subnet_data = prism_get_subnet(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,subnet_name=None,subnet_uuid=subnet_uuid,secure=PC_PROVIDER_SECURE)
        if 'OVERLAY' in subnet_data['spec']['resources']['subnet_type'] and subnet_data['spec']['resources']['vpc_reference']['uuid'] == tenant_vpc_uuid:
            print('The {} Production Security Zone Overlay Subnet exists in the Calm Project {}'.format(SECURITY_ZONE, CALM_PROJECT_NAME))
            subnet_prod = {'name': subnet['name'], 'uuid': subnet['uuid']}
            subnet_prod = json.dumps(subnet_prod)
    if 'admin'.lower() in subnet['name'].lower():
        print(subnet['name'])
        subnet_uuid = subnet['uuid']
        subnet_uuid, subnet_data = prism_get_subnet(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,subnet_name=None,subnet_uuid=subnet_uuid,secure=PC_PROVIDER_SECURE)
        if 'OVERLAY' in subnet_data['spec']['resources']['subnet_type'] and subnet_data['spec']['resources']['vpc_reference']['uuid'] == tenant_vpc_uuid:
            print('The Admin Security Zone Overlay Subnet exists in the Calm Project {}'.format(CALM_PROJECT_NAME))
            subnet_admin = {'name': subnet['name'], 'uuid': subnet['uuid']}
            subnet_admin = json.dumps(subnet_admin)

print("tenant_vpc_uuid={}".format(tenant_vpc_uuid))
print("subnet_prod={}".format(subnet_prod))
print("subnet_admin={}".format(subnet_admin))