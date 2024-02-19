from general_utils import validate_ip,validate_subnet

"""
We are using a popular Python library "cerberus" to define the json/ yml schema
https://docs.python-cerberus.org/en/stable/validation-rules.html
"""

GLOBAL_SCHEMA = {}

GLOBAL_SCHEMA['CALM_CONFIG'] = {
    "calm_config": {
        "type": "dict",
        "schema": {
            "calm_ip_address": {
                "meta" : {'description': "Nutanix Self-Service IP Address"},
                "required": True,
                "type": "string",
                "default": "127.0.0.1",
                'validator': validate_ip
                },
            "calm_user": {
                "meta" : {'description': "Nutanix Self-Service Username used for authentication"},
                "required": True,
                "type": "string",
                "default": "user@company.com"
                },
            "calm_password": {
                "meta" : {'description': "Nutanix Self-Service Username Password used for authentication", "secret":True},
                "required": True,
                "type": "string"
                },
            "calm_project_name": {
                "meta" : {'description': "Nutanix Self-Service Pre-Configured Project name"},
                "required": True,
                "type": "string",
                "default": "default"
                },
        }
    }
}

GLOBAL_SCHEMA['PRISM_CENTRAL_CONFIG'] = {
    "prism_central_config": {
        "type": "dict",
        "schema": {
            "PC_PROVIDER_ADDRESS": {
                "meta" : {'description': "Nutanix Remote Prism Central Address"},
                "required": True,
                "type": "string",
                "default": "127.0.0.1"
                },
            "PC_PROVIDER_USERNAME": {
                "meta" : {'description': "Nutanix Prism Central Username used for authentication"},
                "required": True,
                "type": "string",
                "default": "user@company.com"
                },
            "PC_PROVIDER_SECRET": {
                "meta" : {'description': "Nutanix Prism Central Username Password used for authentication", "secret":True},
                "required": True,
                "type": "string"
                },
        }
    }
}

GLOBAL_SCHEMA['HYCU_CONFIG'] = {
    "hycu_config": {
        "type": "dict",
        "schema": {
            "HYCU_ADDRESS": {
                "meta" : {'description': "HYCU Address"},
                "required": True,
                "type": "string",
                "default": "127.0.0.1"
                },
            "HYCU_USERNAME": {
                "meta" : {'description': "HYCU Username used for authentication"},
                "required": True,
                "type": "string",
                "default": "user@company.com"
                },
            "HYCU_SECRET": {
                "meta" : {'description': "HYCU Username Password used for authentication", "secret":True},
                "required": True,
                "type": "string"
                },
        }
    }
}

GLOBAL_SCHEMA['CYBERARK_CONFIG'] = {
    "cyberark_config" :{
        "type": "dict",
        "schema": {
            "cyberark_endpoint_ip": {
                "meta" : {'description': "Cyberark Endpoint IP Address"},
                "required": True,
                "type": "string",
                "default": "127.0.0.1",
                'validator': validate_ip
                },
            "cyberark_endpoint_service": {
                "meta" : {'description': "Cyberark Endpoint Service"},
                "required": True,
                "type": "string",
                "maxlength":6
                },
            "cyberark_app_id": {
                "meta" : {'description': "Cyberark Application ID"},
                "required": True,
                "type": "string"
                },
            "cyberark_default_safe": {
                "meta" : {'description': "Cyberark Default Safe"},
                "required": True,
                "type": "string",
                "maxlength": 6
                },
            "infoblox_user": {
                "meta" : {'description': "Infoblox Service Account Name to be pulled from Cyberark"},
                "required": True,
                "type": "string"
                },
            "prism_central_user": {
                "meta" : {'description': "Prism Central Service Account Name to be pulled from Cyberark"},
                "required": True,
                "type": "string"
                },
            "ansible_user": {
                "meta" : {'description': "Ansible Service Account Name to be pulled from Cyberark"},
                "required": True,
                "type": "string"
                },
            "ad_user": {
                "meta" : {'description': "Active Directory Service Account Name to be pulled from Cyberark"},
                "required": True,
                "type": "string"
                }
        }
    }
}

GLOBAL_SCHEMA['INFOBLOX_CONFIG'] = {
    "infoblox_config": {
        "type": "dict",
        "schema": {
            "INFOBLOX_ADDRESS" : {
                "meta" : {'description': "Infoblox Endpoint IP Address"},
                "required": True,
                "type": "string",
                "default": "https://ipam13.wob.vw.vwg/wapi/v2.10",
                },
            "INFOBLOX_USERNAME" : {
                "meta" : {'description': "Infoblox Service Account Username used for authentication"},
                "required": True,
                "type": "string",
                "meta" : {'description': "Infoblox Username"}
                },
            "INFOBLOX_SECRET" : {
                "meta" : {'description': "Infoblox Service Account Secret used for authentication", "secret":True},
                "required": True,
                "type": "string",
                "meta" : {'description': "Infoblox Secret","secret":True}
                },
            "INFOBLOX_TENANT_EXT_ATTR_NAME" : {
                "required": True,
                "type": "string",
                "default": "Tenant",
                "meta" : {'description': "INFOBLOX_TENANT_EXT_ATTR_NAME"}
                },
            "INFOBLOX_NETWORKS_SPECS" : {
                "type": "dict",
                "required": False,
                "schema": {
                    "infoblox_production_network_specs": {
                        "required": True,
                        "type": "dict",
                        "schema" :{
                            "container_network" :{
                                "type" : "string",
                                "required": True,
                                "validator": validate_subnet
                            },
                            "tenant_app_network_len" :{
                                "type" : "integer",
                                "required": True
                            },
                        }
                    }
                }
            }
        }
    }
}

GLOBAL_SCHEMA['BLUEPRINT_VARIABLES'] = {
    "blueprint_variables" :{
        "type": "dict",
        "schema": {
            "rhel_8_image_location": {
                "meta" : {'description': "Artifactory URL path to the RHEL8 image to be used in the blueprints"},
                "required": True,
                "type": "string",
                "default": "https://artifactory.wob.vw.vwg:8443/artifactory/gitc/bps/images/rhel/8/vw-rhel-8-20231211.qcow2"
                },
            "rhel_9_image_location": {
                "meta" : {'description': "Artifactory URL path to the RHEL9 image to be used in the blueprints"},
                "required": True,
                "type": "string",
                "default": "https://artifactory.wob.vw.vwg:8443/artifactory/gitc/bps/images/rhel/9/vw-rhel-9-20231211.qcow2"
                },
            "windows_2019_image_location": {
                "meta" : {'description': "Artifactory URL path to the Windows 2019 image to be used in the blueprints"},
                "required": True,
                "type": "string",
                "default": "https://artifactory.wob.vw.vwg:8443/artifactory/gitc/bps/images/windows/2019/vw-win2k19-20240125.qcow2"
                },
            "windows_2022_image_location": {
                "meta" : {'description': "Artifactory URL path to the Windows 2022 image to be used in the blueprints"},
                "required": True,
                "type": "string",
                "default": "https://artifactory.wob.vw.vwg:8443/artifactory/gitc/bps/images/windows/2022/vw-win2k22-20240123.qcow2"
                },
            "product_key": {
                "required": True,
                "type": "string",
                "default": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"
                },
            "timezone": {
                "required": True,
                "type": "string",
                "default": "W. Europe Standard Time"
                },
            "windows_default_creds_username": {
                "meta" : {'description': "Default Username used for authentication to the Windows OS"},
                "required": True,
                "type": "string",
                "default": "Administrator"
                },
            "windows_default_creds_secret": {
                "meta" : {'description': "Default Username Password used for authentication to the Windows OS", "secret":True},
                "required": True,
                "type": "string"
                },
            "linux_default_creds_username": {
                "meta" : {'description': "Default Username used for authentication to the Linux OS"},
                "required": True,
                "type": "string",
                "default": "cloud-user"
                },
            "linux_os_cred_private_key_path": {
                "meta" : {'description': "Default Path to the Private SSH Key used for authentication to the Linux OS", "secret":True},
                "required": True,
                "type": "string"
                },
            "linux_os_cred_public_key": {
                "meta" : {'description': "Default Public SSH Key used for authentication to the Linux OS"},
                "required": True,
                "type": "string"
                },
            "cvm_creds_username": {
                "meta" : {'description': "Username used for authentication to the Nutanix CVM during the AntiAffinity Day2 Action"},
                "required": True,
                "type": "string"
                },
            "cvm_creds_secret": {
                "meta" : {'description': "Username Password used for authentication to the Nutanix CVM during the AntiAffinity Day2 Action", "secret":True},
                "required": True,
                "type": "string"
                },
            "organization": {
                "required": True,
                "type": "string",
                "default": "VWGroup"
                },
            "cluster_ip": {
                "required": True,
                "type": "string",
                'validator': validate_ip
                },
            "smtp_server": {
                "required": True,
                "type": "string",
                "default": "smtp.server"
                },
            "requester_email": {
                "required": True,
                "type": "string",
                "default": "user@nutanix.com"
                },
            "vm_requester_name": {
                "required": True,
                "type": "string",
                "default": "Nutanix"
                },
            "email_sender": {
                "required": True,
                "type": "string",
                "default": "user@nutanix.com"
                }
        }
    }
}

GLOBAL_SCHEMA['BLUEPRINT_ENDPOINTS'] = {
    "blueprint_endpoints" :{
        "type": "dict",
        "schema": {
            "windows_endpoint_name": {
                "required": True,
                "type": "string",
                "default": "WIN_ENDPOINT"
                },
            "linux_endpoint_name": {
                "required": True,
                "type": "string",
                "default": "LIN_ENDPOINT"
                }
        }
    }
}