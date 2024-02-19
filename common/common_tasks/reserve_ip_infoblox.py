############# Calm imports #################################################################
# CALM_USES infoblox_subnets.py, infoblox_ips.py, ip_utilities.py
############################################################################################

INFOBLOX_ADDRESS = '@@{INFOBLOX_ADDRESS}@@'
INFOBLOX_USERNAME = '@@{INFOBLOX_USERNAME}@@'
INFOBLOX_SECRET = '@@{INFOBLOX_SECRET}@@'
INFOBLOX_SECURE = @@{INFOBLOX_SECURE}@@
INFOBLOX_TENANT_EXT_ATTR_NAME = '@@{INFOBLOX_TENANT_EXT_ATTR_NAME}@@'
PROJECT_NAME = "@@{PROJECT_NAME}@@"

PRODIP = "@@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@@"
ADMINIP = "@@{platform.status.resources.nic_list[1].ip_endpoint_list[0].ip}@@"

IP_LIST = [PRODIP, ADMINIP]

ip_ref_list = []
for ip in IP_LIST:
    print("\n\n\n######## Checking to see if the VM IP address {} already exist in Infoblox ##################".format(ip))
    ip_reservation, ip_reservtion_status = infoblox_check_fixed_address_reservation(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                        ip_address=ip,extattrs={INFOBLOX_TENANT_EXT_ATTR_NAME: {"value": PROJECT_NAME}},secure=INFOBLOX_SECURE)
    if ip_reservtion_status == 'UNUSED':
        print("\n\n\n######## Reserving VM IP address {} in Infoblox since its status is UNUSED ##################".format(ip))
        resp = infoblox_add_fixed_address_reservation(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                        ip_address=ip,hostname='@@{hostname}@@',extattrs={INFOBLOX_TENANT_EXT_ATTR_NAME: {"value": PROJECT_NAME}},secure=INFOBLOX_SECURE)
        print('response is {}'.format(resp))
    elif ip_reservtion_status == 'USED':
        print("\n\n\n######## Releasing VM IP address {} in Infoblox since its status is USED and AHV is the source of truth for IPAM ##################".format(ip))
        resp = infoblox_release_fixed_address_reservation(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                        ip_address=ip,extattrs={INFOBLOX_TENANT_EXT_ATTR_NAME: {"value": PROJECT_NAME}},secure=INFOBLOX_SECURE)
        print("\n\n\n######## Reserving VM IP address {} in Infoblox since its status is now UNUSED ##################".format(ip))
        resp = infoblox_add_fixed_address_reservation(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                        ip_address=ip,hostname='@@{hostname}@@',extattrs={INFOBLOX_TENANT_EXT_ATTR_NAME: {"value": PROJECT_NAME}},secure=INFOBLOX_SECURE)
    else:
        print('The IP address supplied does not exist in Infoblox')