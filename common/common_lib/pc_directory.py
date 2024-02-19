################################################
############ pc_directory.py        ############
################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py
############################################################################################

def pc_get_directory_service_uuid(api_server,username,secret,directory_service_name,secure=False):
    """
        Retrieves directory service uuid on Prism Central

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        directory_service_name: Name of the directory service to retrieve
        
    Returns:
        Uuid of the directory service (string).
    """
    directory_service_uuid, directory = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="directory_service",entity_api_root="directory_services",entity_name=directory_service_name,secure=secure)
    return directory_service_uuid
