from datetime import datetime

############# Calm imports #################################################################
# CALM_USES http_requests.py
############################################################################################

def fetch_cred(user_label):

    def get_ccp_creds(ccp_endpoint, ccp_endpoint_service, ccp_app_id, ccp_safe, ccp_virtuser):
        # Return tuple (fq_userid, password)
        method = "GET"
        url = "https://{}/{}/api/Accounts?AppId={}&Query=Safe={};VirtualUserName={}".format(ccp_endpoint, ccp_endpoint_service, ccp_app_id, ccp_safe, ccp_virtuser)
        response = process_request(url,method=method, verify=False)
        if response.ok:
            data = response.json()
            return (data['UserName']+'@'+data['Address'], data['Content'])
        print("get_ccp_creds: Received {} response: {}".format(response.status_code, response.content))
        return (None, None)

    fq_userid = password = None
    cred_config = json.loads(r'@@{CRED_CONFIG}@@')

    virtuser = cred_config['virtual_users'][user_label]['vuser']
    ccp_safe = cred_config['virtual_users'][user_label].get('safe', cred_config['ccp_default_safe'])
    ccp_endpoint = cred_config['ccp_endpoint']
    ccp_endpoint_service = cred_config['ccp_endpoint_service']
    ccp_app_id = cred_config['ccp_app_id']

    print("{} Retrieving credentials for {} from CyberArk...".format(datetime.now(), virtuser))
    fq_userid, password = get_ccp_creds(ccp_endpoint, ccp_endpoint_service, ccp_app_id, ccp_safe, virtuser)

    print('{} Returning credentials to caller'.format(datetime.now()))
    return type('credential',(object,), {'username': fq_userid, 'secret': password})