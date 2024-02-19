####################################################
############ pc_ssp_environments.py     ############
####################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py
############################################################################################

def prism_ssp_get_accounts_list(api_server,username,secret,secure=False,print_f=True,filter=None):

    """Retrieve the list of Accounts from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of Accounts (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="account",entity_api_root="accounts",secure=secure,print_f=print_f,filter=filter)


def prism_ssp_get_account(api_server,username,secret,account_name=None,account_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given account name.
       If an account_uuid is specified, it will skip retrieving all accounts (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        account_name: Name of the account (optional).
        account_uuid: Uuid of the account (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the account (account_uuid) and the json content
        of the account details (account)
    """

    account_uuid, account = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="account",entity_api_root="accounts",entity_name=account_name,entity_uuid=account_uuid,
                              secure=secure,print_f=print_f)
    return account_uuid, account