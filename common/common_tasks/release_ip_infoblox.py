############# Calm imports #################################################################
# CALM_USES infoblox_subnets.py, infoblox_ips.py, ip_utilities.py
############################################################################################

INFOBLOX_ADDRESS = '@@{INFOBLOX_ADDRESS}@@'
INFOBLOX_USERNAME = '@@{INFOBLOX_USERNAME}@@'
INFOBLOX_SECRET = '@@{INFOBLOX_SECRET}@@'
INFOBLOX_SECURE = @@{INFOBLOX_SECURE}@@
INFOBLOX_TENANT_EXT_ATTR_NAME = '@@{INFOBLOX_TENANT_EXT_ATTR_NAME}@@'
PROJECT_NAME = '@@{PROJECT_NAME}@@'

PRODIP = "@@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@@"
ADMINIP = "@@{platform.status.resources.nic_list[1].ip_endpoint_list[0].ip}@@"

IP_LIST = [PRODIP, ADMINIP]

print("\n\n\n######## Releasing VM IP addresses in Infoblox ##################")
IP_LIST = [PRODIP, ADMINIP]
for ip in IP_LIST:
    resp = infoblox_release_fixed_address_reservation(infoblox_api_endpoint=INFOBLOX_ADDRESS,username=INFOBLOX_USERNAME,secret=INFOBLOX_SECRET,
                                        ip_address=ip,extattrs={INFOBLOX_TENANT_EXT_ATTR_NAME: {"value": PROJECT_NAME}},secure=INFOBLOX_SECURE)
    print('response is {}'.format(resp))