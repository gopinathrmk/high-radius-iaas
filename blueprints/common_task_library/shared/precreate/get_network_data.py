import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#TODO - variable for lin vs win dns domain name.
#TODO - Create DNS python to determine DNS servers.

CALM_PROJECT = '@@{PROJECT_NAME}@@'
CALM_ENV = '@@{calm_environment_name}@@'

######## SECTION TO FETCH CREDS FROM CYBERARK ########
# @@{FETCH_CRED_PY}@@
# PC_CREDS = fetch_cred("prism")
# SELF_SERVICE_USERNAME = PC_CREDS.username
# SELF_SERVICE_SECRET = PC_CREDS.secret
# IB_CREDS = fetch_cred("ipam")
# INFOBLOX_USERNAME = IB_CREDS.username
# INFOBLOX_SECRET = IB_CREDS.secret

SELF_SERVICE_ADDRESS = '@@{SELF_SERVICE_ADDRESS}@@'
SELF_SERVICE_USERNAME = '@@{SELF_SERVICE_USERNAME}@@'
SELF_SERVICE_SECRET = '@@{SELF_SERVICE_SECRET}@@'
SELF_SERVICE_SECURE = False

PC_PROVIDER_ADDRESS = '@@{PC_PROVIDER_ADDRESS}@@'
PC_PROVIDER_USERNAME = '@@{PC_PROVIDER_USERNAME}@@'
PC_PROVIDER_SECRET = '@@{PC_PROVIDER_SECRET}@@'
PC_PROVIDER_SECURE = False

CALM_PROJECT_NAME = '@@{PROJECT_NAME}@@'

INFOBLOX_ADDRESS = '@@{INFOBLOX_ADDRESS}@@'
INFOBLOX_USERNAME = '@@{INFOBLOX_USERNAME}@@'
INFOBLOX_SECRET = '@@{INFOBLOX_SECRET}@@'
INFOBLOX_SECURE = @@{INFOBLOX_SECURE}@@

SELF_SERVICE_USERNAME = '@@{PC_PROVIDER_USERNAME}@@'
SELF_SERVICE_SECRET = '@@{PC_PROVIDER_SECRET}@@'
NUTANIX_AUTH = HTTPBasicAuth(SELF_SERVICE_USERNAME, SELF_SERVICE_SECRET)
CALM_URL = 'https://{}:9440/api/nutanix/v3'.format('127.0.0.1')
CALM_HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

INFOBLOX_AUTH = HTTPBasicAuth(INFOBLOX_USERNAME, INFOBLOX_SECRET)
INFOBLOX_HEADERS = {'Content-Type': 'application/json'}

def get_environment_uuid_type(url, env_name):
    body = {"filter": "name=={0}".format(env_name)}
    response = requests.post(url + '/environments/list', json=body,  headers=CALM_HEADERS, auth=NUTANIX_AUTH, verify=False)
    print('Calm project is {}'.format(CALM_PROJECT))
    print('Calm environment is {}'.format(CALM_ENV))
    if response.ok:
        data = response.json()
        if data['metadata']['total_matches'] > 0:
            for env in data['entities']:
                if env['metadata']['project_reference']['name'] == CALM_PROJECT:
                    env_type = env['status']['resources']['infra_inclusion_list'][0]['type']
                    env_uuid = env['status']['uuid']
                    return env_uuid, env_type
    else:
        print('Error {} fetching the environment uuid - {}'.format(response.status_code, response.content))
        exit(1)

def get_ahv_environment_netuuids(url, env_name):
    body = {"filter": "name=={0}".format(env_name)}
    response = requests.post(url + '/environments/list', json=body,  headers=CALM_HEADERS, auth=NUTANIX_AUTH, verify=False)
    env_networks = []
    if response.ok:
        data = response.json()
        if data['metadata']['total_matches'] > 0:
            for env in data['entities']:
                env_type = env['status']['resources']['infra_inclusion_list'][0]['type']
                if env['metadata']['project_reference']['name'] == CALM_PROJECT and env_type == 'nutanix_pc':
                    for subnet in env['status']['resources']['infra_inclusion_list'][0]['subnet_references']:
                        env_networks.append(subnet['uuid'])
                    return env_networks
    else:
        print('Error {} fetching the environment subnets - {}'.format(response.status_code, response.content))
        exit(1)

def get_ahv_sub_ref_ls(url, prj):
    body = {"filter": "name=={0}".format(prj)}
    response = requests.post(url + "/projects/list", json=body, headers=CALM_HEADERS, auth=NUTANIX_AUTH, verify=False)
    if response.ok:
        data = response.json()
        netdata={}
        if len(data['entities']) > 0:
            for n in data['entities']:
                if len(n['spec']['resources']['external_network_list']) > 0:
                    nets=n['spec']['resources']['external_network_list']
                for n in nets:
                    net_uuid = n["uuid"]
                    netdata[net_uuid] = n["name"]
            return netdata

def get_act_id_server(url, prj):
    body = {"filter": "name=={0}".format(prj)}
    response = requests.post(url + "/projects/list", json=body, headers=CALM_HEADERS, auth=NUTANIX_AUTH, verify=False)
    if response.ok:
        data = response.json()
        if data['metadata']['total_matches'] > 0:
            for act in data['entities'][0]['spec']['resources']['account_reference_list']:
                act_uid = act['uuid']
                acct_server = get_act_server(url, act_uid)
                #if chk_act:
                return act_uid, acct_server

def get_act_server(url, act_uid):
    response = requests.get(url + "/accounts/{}".format(act_uid), headers=CALM_HEADERS, auth=NUTANIX_AUTH, verify=False)
    if response.ok:
        data = response.json()
        #chk_act=False
        #if data['spec']['resources']['type'] == 'vmware' and data['metadata']['name'] in SITE_CLUSTER_MATCH:
        #if data['spec']['resources']['type'] == 'vmware':
            #chk_act=True
        act_server = data['spec']['resources']['data']['server']
        return act_server

def get_network_list_sending_to_infoblox(networks):
    ib_networks = []
    for net in networks:
        print(net)
        net_split = net['name'].split('_')[2]
        # net_full = (net_split[2] + '.' + net_split[3] + '.' + net_split[4] + '.'+net_split[5])
        # print(net_full)
        x = {'name': net['name'], 'uuid': net['uuid'], 'ibnetwork': net_split}
        ib_networks.append(x)
    return ib_networks

def get_ip_from_infoblox(network_data):
    url = "https://{}/wapi/v2.12.3/request".format(INFOBLOX_ADDRESS)
    #url = "https://{}/wapi/v2.12.3/fixedaddress?_return_fields%2B=ipv4addr&_return_as_object=1".format(INFOBLOX_ADDRESS)
    net = network_data['ibnetwork']
    # data = {
    #     "ipv4addr": "func:nextavailableip:{}".format(net),
    #     "name": "@@{hostname}@@.@@{domain}@@",
    #     "match_client": "RESERVED",
    #     "comment": "Created by Nutanix CALM for Deployment: @@{hostname}@@"
    # }
    data = {
        "method":"POST",
        "object":"fixedaddress",
        "data": {
            "name": "@@{hostname}@@.@@{domain}@@",
            "comment": "Created by Nutanix CALM for Deployment: gtest",
            "match_client": "RESERVED",
            "ipv4addr": {
            "_object_function": "next_available_ip",
            "_object": "network",
            "_object_parameters": {"network": "{}".format(net)},
            "_result_field": "ips",
            "_parameters": {"exclude": ["{}".format(exclusion)]}
            }
            },
        "args": {"_return_fields": "name,ipv4addr"}
    }
    net_list = net.split('/')[0].split('.')[:-1]+['1']
    exclusion = ".".join(net_list)
    print('exclusion is {}'.format(exclusion))
    response = requests.post(url, headers=INFOBLOX_HEADERS, json=data, auth=INFOBLOX_AUTH, verify=False)
    if response.ok:
        data = response.json()
        ipreference = data["_ref"]
        ipaddress = data["ipv4addr"]
        return ipreference, ipaddress

def get_dns_gateway_cidr_mask_from_infoblox(network_data):
    network = network_data['ibnetwork']
    url = "https://{}/wapi/v2.12.3/network?network={}&_return_fields=options".format(INFOBLOX_ADDRESS, network)
    response = requests.get(url, headers=INFOBLOX_HEADERS, auth=INFOBLOX_AUTH, verify=False)
    if response.ok:
        data = response.json()
        for option in data[0]['options']:
            if option['name'] == 'domain-name-servers':
                dns_server = option['value']
            if option['name'] == 'routers':
                default_gateway = option['value']
        network_cidr = network.split('/')[1]
        subnet_mask = get_subnet_mask(network_cidr)
        #return dns_server, default_gateway, network_cidr, subnet_mask
        return default_gateway, network_cidr, subnet_mask
    else:
        print('Error {} fetching the dns servers and network gateway from infoblox - {}'.format(response.status_code, response.content))
        exit(1)

def get_subnet_mask(cidr):
    mask = '1'*int(cidr) + '0'*(32-int(cidr))
    subnet_mask = "{}.{}.{}.{}".format(int(mask[0:8],2), int(mask[8:16],2), int(mask[16:24],2), int(mask[24:32],2))
    print("Converted CIDR {} to subnet mask {}".format(cidr, subnet_mask))
    return subnet_mask

def check_dns_infoblox(network):
    url = "https://{}/wapi/v2.12.3/network?network={}&_return_fields=options".format(INFOBLOX_ADDRESS, network)
    print(url)
    response = requests.get(url, headers=INFOBLOX_HEADERS, auth=INFOBLOX_AUTH, verify=False)
    if response.ok:
        data = response.json()
        print(data)
        if len(data) != 0:
            check_dns_gateway = False
            for option in data[0]['options']:
                print(option)
                if option['name'] == 'domain-name-servers':
                    check_dns_gateway = True
            return check_dns_gateway

def get_least_used_network_from_infoblox(networks):
    """Retrieves the InfoBlox network with the most available IP address available from a json list of dictionaries"""
    # Initiating an empty dictionary to append subnet and it's available IPs as a key-value pair
    networks_available_ips = {}
    # Looping through each network and retrieving count of available IPs
    for network in networks:
        network = network['ibnetwork']
        chk_dns_gate = check_dns_infoblox(network)
        print('Domain Name Server check was good')
        url = "https://{}/wapi/v2.12.3/ipv4address?network={}&status=UNUSED&_max_results=1021".format (INFOBLOX_ADDRESS, network)
        response = requests.get(url, headers=INFOBLOX_HEADERS, auth=INFOBLOX_AUTH, verify=False)
        if response.ok:
            try:
                # Count the number of objects returned for available IPs
                measure = response.json()
            except:
                print("Error {} - InfoBlox API Request failed - {}".format(response.status_code, response.content))
                exit(1)
            # Appending the network and the count to the dictionary
            networks_available_ips.update({network: len(measure)})
    print('\n InfoBlox subnets and Available IPs: ', networks_available_ips)
    # Sorting the subnets based on the count
    #sorted_subnets = sorted(networks_available_ips.items(), key=operator.itemgetter(1), reverse=True)
    sorted_subnets = sorted(networks_available_ips.items(), key=lambda x : x[1], reverse=True)
    print('\n InfoBlox subnets sorted with most available IPs first:', sorted_subnets)
    # Selecting the first subnet from the sorted
    selected_subnet = sorted_subnets[0][0]
    print('\n InfoBlox selected subnet:', selected_subnet)
    for network in networks:
        if selected_subnet in network['ibnetwork']:
            network_dict = network
            return network_dict

def create_dns_record_in_infoblox(ip):
    url = "https://{}/wapi/v2.12.3/record:host".format(INFOBLOX_ADDRESS)
    data = {
    "ipv4addrs": [{"ipv4addr": ip}],
    "name": "@@{hostname}@@.@@{domain}@@",
    "comment": "Created by Nutanix CALM for Deployment: @@{hostname}@@"
    }
    response = requests.post(url, headers=INFOBLOX_HEADERS, json=data, auth=INFOBLOX_AUTH, verify=False)
    if response.ok and response.status_code == 201:
        data = response.json()
        a_record_reference = data
    else:
        print('Error {} creating the DNS record in InfoBlox - {}'.format(response.status_code, response.content))
        exit(1)
    return a_record_reference

calm_env_uuid, calm_env_type = get_environment_uuid_type(CALM_URL, CALM_ENV)

if calm_env_type == 'nutanix_pc':
    account_uid, account_server=get_act_id_server(CALM_URL, CALM_PROJECT)
    print('Calm Account UUID is {}'.format(account_uid))
    print('Calm Account Server is {}'.format(account_server))
    provider_account_name="Prism Central Console - {}".format(CALM_PROJECT)
    provider_account_url="https://" + account_server + ":9440/console"
    netdata_temp = get_ahv_sub_ref_ls(CALM_URL, CALM_PROJECT)
    print('\n Calm project networks are {}'.format(netdata_temp))
    calm_env_netuuids = get_ahv_environment_netuuids(CALM_URL, CALM_ENV)
    print('\n Calm environment networks are {}'.format(calm_env_netuuids))

    substrate_network_data = []
    if len(calm_env_netuuids) > 0:
        for key, value in netdata_temp.items():
            if key in calm_env_netuuids:
                x = {"name": value, "uuid": key}
                substrate_network_data.append(x)
    print('\n Calm project networks matching those from the Calm environment network list are {}'.format(substrate_network_data))

    infoblox_networks = get_network_list_sending_to_infoblox(substrate_network_data)
    print('\n Network list from target list above sending to InfoBlox are {}'.format(infoblox_networks))

    ib_target_network_dict = get_least_used_network_from_infoblox(infoblox_networks)
    print('InfoBlox selected network dictionary is {}'.format(ib_target_network_dict))
    dynamic_network = {'name': ib_target_network_dict['name'], 'uuid': ib_target_network_dict['uuid']}
    dynamic_network = json.dumps(dynamic_network)
    ipref, staticip = get_ip_from_infoblox(ib_target_network_dict)
    print('\n ipref is {} and staticip is {}'.format(ipref, staticip))
    #dns, gateway, cidr, netmask = get_dns_gateway_cidr_mask_from_infoblox(ib_target_network_dict)
    gateway, cidr, netmask = get_dns_gateway_cidr_mask_from_infoblox(ib_target_network_dict)
    print(dynamic_network, ipref, staticip, gateway, cidr)
    a_ref = create_dns_record_in_infoblox(staticip)
    print(a_ref)
    # dns_split = dns.split(',')
    # if len(dns_split) == 1:
    #     dns1 = dns_split[0]
    #     dns2 = ''
    # elif len(dns_split) > 1:
    #     dns1 = dns_split[0]
    #     dns2 = dns_split[1]

print("account_server={}".format(account_server))
print("provider_account_url={}".format(provider_account_url))
print("provider_account_name={}".format(provider_account_name))
print("dynamic_network={}".format(dynamic_network))
print("ip_ref={}".format(ipref))
print("staticip={}".format(staticip))
# print("dns1={}".format(dns1))
# print("dns2={}".format(dns2))
print("gateway={}".format(gateway))
print("cidr={}".format(cidr))
print("netmask={}".format(netmask))
print("a_ref={}".format(a_ref))