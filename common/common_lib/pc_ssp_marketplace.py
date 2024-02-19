####################################################
############ pc_ssp_marketplace.py     ############
####################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py
############################################################################################

def prism_ssp_get_marketplace_items_list(api_server,username,secret,secure=False,print_f=True,filter=None):


    """Retrieve the list of marketplace items  from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of marketplace items (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="marketplace_item",entity_api_root="calm_marketplace_items",secure=secure,print_f=print_f,filter=filter)

def prism_ssp_get_marketplace_item(api_server,username,secret,marketplace_item_name=None,marketplace_item_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given marketplace item name.
       If a marketplace_item_uuid is specified, it will skip retrieving all marketplace items (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        marketplace_item_name: Name of the marketplace item (optional).
        marketplace_item_uuid: Uuid of the marketplace item (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the marketplace item (marketplace_item_uuid) and the json content
        of the marketplace item details (marketplace_item)
    """

    marketplace_item_uuid, marketplace_item = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="marketplace_item",entity_api_root="calm_marketplace_items",entity_name=marketplace_item_name,entity_uuid=marketplace_item_uuid,
                              secure=secure,print_f=print_f)
    return marketplace_item_uuid, marketplace_item