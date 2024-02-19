################################################
############ pc_images.py         ############
################################################

############# Calm imports #################################################################
# CALM_USES pc_entities.py
############################################################################################

def prism_get_disk_images(api_server,username,secret,secure=False,print_f=True,filter=None):

    """Retrieve the list of images from Prism Central.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        filter: filter to be applied to the search
        
    Returns:
        A list of Images (entities part of the json response).
    """

    return prism_get_entities(api_server=api_server,username=username,secret=secret,
                              entity_type="image",entity_api_root="images",
                              secure=secure,print_f=print_f,filter=filter)


def prism_get_disk_image(api_server,username,secret,image_name=None,image_uuid=None,secure=False,print_f=True):

    """Returns from Prism Central the uuid and details of a given image name.
       If a image_uuid is specified, it will skip retrieving all images (faster).

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        image_name: Name of the image (optional).
        image_uuid: Uuid of the image (optional).
        secure: boolean to verify or not the api server's certificate (True/False) 
        print_f: True/False. if False the function does not print traces to the stdout, as long as there are no errors
        
    Returns:
        A string containing the UUID of the image (image_uuid) and the json content
        of the image details (image)
    """

    image_uuid, image = prism_get_entity(api_server=api_server,username=username,secret=secret,
                              entity_type="image",entity_api_root="images",entity_name=image_name,entity_uuid=image_uuid,
                              secure=secure,print_f=print_f)
    return image_uuid, image