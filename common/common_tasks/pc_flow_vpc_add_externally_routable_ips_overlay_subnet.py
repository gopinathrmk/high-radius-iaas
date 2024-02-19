#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# pc_flow_vpc_add_externally_routable_ips_overlay_subnet.py                                                     >
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

############# Calm imports #################################################################
# CALM_USES http_requests.py, ip_utilities.py, pc_projects.py, pc_subnets.py, pc_ssp_environments.py, pc_flow_vpc, infoblox_subnets.py, infoblox_ips.py, pc_tasks.py
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

INFOBLOX_ADDRESS = '@@{INFOBLOX_ADDRESS}@@'
INFOBLOX_USERNAME = '@@{INFOBLOX_USERNAME}@@'
INFOBLOX_SECRET = '@@{INFOBLOX_SECRET}@@'
INFOBLOX_SECURE = @@{INFOBLOX_SECURE}@@
INFOBLOX_TENANT_EXT_ATTR_NAME = '@@{INFOBLOX_TENANT_EXT_ATTR_NAME}@@'

INFOBLOX_NETWORKS_SPECS = json.loads('@@{INFOBLOX_NETWORKS_SPECS}@@')

project_uuid, project = prism_get_project(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,project_name=CALM_PROJECT_NAME,project_uuid=None,secure=SELF_SERVICE_SECURE)

def create_overlay_subnet():
    print("######## Reserving Network in Infoblox from Production container {} ##################".format(INFOBLOX_NETWORKS_SPECS["infoblox_production_network_specs"]["container_network"]))
    result = infoblox_reserve_next_subnet(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
        container_network_address=INFOBLOX_NETWORKS_SPECS["infoblox_production_network_specs"]["container_network"],
        requested_subnet_cidr=INFOBLOX_NETWORKS_SPECS["infoblox_production_network_specs"]["tenant_app_network_len"],
        extattrs={INFOBLOX_TENANT_EXT_ATTR_NAME: {"value": CALM_PROJECT_NAME}},
        secure=INFOBLOX_SECURE)
    subnet_cidr = result["network"]

    default_subnet_cidr="{}".format(subnet_cidr)
    default_subnet_ip="{}".format(subnet_cidr.split('/')[0])
    default_subnet_mask="{}".format(ipv4_cidrlen_to_mask(int(subnet_cidr.split('/')[1])))
    default_subnet_len="{}".format(subnet_cidr.split('/')[1])
    print("######## Network Reserved Successfully ##################")
    externally_routable_ip_to_add = result["network"]
    print('externally routable ip to be added is {}'.format(externally_routable_ip_to_add))

    task_uuid = prism_flow_vpc_add_externally_routable_ips(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,
                vpc_uuid=tenant_vpc_uuid,externally_routable_prefix_list=[externally_routable_ip_to_add],
                secure=PC_PROVIDER_SECURE
    )

    print("######## Fetching Gateway address from Infoblox ##################")
    subnet_unused_ips = infoblox_get_subnet_unused_ips(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                                    subnet_address=subnet_cidr,
                                                    secure=INFOBLOX_SECURE)
    default_subnet_gateway=ipv4_min(subnet_unused_ips)
    print("######## Gateway address fetched successfully: {} ##################".format(default_subnet_gateway))

    print("\n\n\n######## Reserving Gateway address from Infoblox ##################")
    infoblox_add_fixed_address_reservation(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                        ip_address=default_subnet_gateway,hostname="gateway",
                                        extattrs={INFOBLOX_TENANT_EXT_ATTR_NAME: {"value": CALM_PROJECT_NAME}},
                                        secure=INFOBLOX_SECURE)
    print("######## Gateway address reserved successfutlly ##################")

    print("\n\n\n######## Fetching remaining free ip pool from Infoblox ##################")
    subnet_unused_ips = infoblox_get_subnet_unused_ips(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                                    subnet_address=subnet_cidr,
                                                    secure=INFOBLOX_SECURE)

    default_subnet_ip_pool_start="{}".format(ipv4_min(subnet_unused_ips))
    default_subnet_ip_pool_end="{}".format(ipv4_max(subnet_unused_ips))
    default_subnet_gateway="{}".format(default_subnet_gateway)
    print("######## IP pool fetched successfully ##################")

    print("######## Fetching DNS ips from Infoblox ##################")
    network = infoblox_get_network(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                    subnet_address="10.4.0.0/16",
                                    object_type=["network", "networkcontainer"],return_fields="options",
                                    secure=INFOBLOX_SECURE)

    dns_options_array = []
    dns_options_array = [
        option["value"] for option in  network["options"] if option["name"] == "domain-name-servers"
    ]
    if dns_options_array == []:
        print("ERROR - unable to get the DNS servers list from Infoblox for network container {}".format("10.4.0.0/16"))
        exit(1)

    dns_list="{}".format(dns_options_array[0])
    print("######## DNS ips fetched successfully ##################")

    subnet_name = '{}_{}_{}/{}'.format(CALM_PROJECT_NAME, SECURITY_ZONE, default_subnet_ip, default_subnet_len)
    print("######## Initiating overlay subnet in Prism Central provider ##################")
    subnet_uuid, task_uuid = prism_create_overlay_subnet_managed(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,subnet_name=subnet_name,subnet_ip=default_subnet_ip,prefix_length=default_subnet_len,default_gateway_ip=default_subnet_gateway,dns_list_csv=dns_list,ip_pool_start=default_subnet_ip_pool_start,ip_pool_end=default_subnet_ip_pool_end,vpc_uuid=tenant_vpc_uuid,secure=PC_PROVIDER_SECURE)
    print("######## Subnet creation initiated ##################")

    print("\n\n\n######## Monitoring progress ##################")
    prism_monitor_task_apiv3(api_server=PC_PROVIDER_ADDRESS,username=PC_PROVIDER_USERNAME,secret=PC_PROVIDER_SECRET,task_uuid=task_uuid,secure=PC_PROVIDER_SECURE)
    print("######## Task finished successfully ##################")

    subnet_uuid="{}".format(subnet_uuid)
    subnet_name="{}".format(subnet_name)

    task_uuid = add_subnet_to_project_infrastructure(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,
                                                        project_uuid=project_uuid,subnet_uuid=subnet_uuid,subnet_name=subnet_name,
                                                        secure=SELF_SERVICE_SECURE)

    # pc_tasks.py
    prism_monitor_task_apiv3(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,
                                task_uuid=task_uuid,
                                secure=SELF_SERVICE_SECURE)

    #project_uuid, project = prism_get_project(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,
    #                                            project_name=None,project_uuid=project_uuid,
    #                                            secure=SELF_SERVICE_SECURE)

    for environment_uuid in [environment["uuid"] for environment in project['spec']['resources']['environment_reference_list']]:
        add_subnet_to_project_environment(api_server=SELF_SERVICE_ADDRESS,username=SELF_SERVICE_USERNAME,secret=SELF_SERVICE_SECRET,environment_uuid=environment_uuid,subnet_uuid=subnet_uuid,secure=SELF_SERVICE_SECURE)

if len(project['spec']['resources']['vpc_reference_list']) > 0:
    tenant_vpc_uuid = project['spec']['resources']['vpc_reference_list'][0]['uuid']
    print('tenant_vpc_uuid is {}'.format(tenant_vpc_uuid))
else:
    print('ERROR - VPC does not exist in the project')
    exit(1)

print(project['spec']['resources']['subnet_reference_list'])
print(project['spec']['resources']['external_network_list'])

if len(project['spec']['resources']['subnet_reference_list']) > 0:
    networks = project['spec']['resources']['subnet_reference_list']
elif len(project['spec']['resources']['external_network_list']) > 0:
    networks = project['spec']['resources']['external_network_list']
else:
    print('ERROR - There are no networks in the subnet_reference_list or external_network_list')
    ## Do we want to create the ADMIN network if not there?
    exit(1)

print('Networks are {}'.format(networks))

if len(networks) >= 1:
    if [appzone for appzone in networks if SECURITY_ZONE in appzone['name']]:
        print('The {} security zone overlay subnet already exists, skipping creation'.format(SECURITY_ZONE))
    else:
        print('Creating the {} security zone overlay subnet'.format(SECURITY_ZONE))
        create_overlay_subnet()
else:
    print('No networks were found for this Tenant')
    exit(1)