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
