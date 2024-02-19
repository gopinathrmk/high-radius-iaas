calm_bp_profile = "AHV_Default"
calm_bp_service = "VM_Provision"

variable_list = [
    { "value": { "value": "1" }, "context": calm_bp_profile, "name": "number_of_vms"},
    { "value": { "value": "RHEL7_CALM - https://artifactory.emeagso.lab:8082/calm_rhel7.qcow2 - 1.0.1" }, "context": calm_bp_profile, "name": "IMAGE_INFO"},
    { "value": { "value": "https://artifactory.emeagso.lab:8082/calm_rhel7.qcow2" }, "context": calm_bp_service, "name": "image_source"},
    { "value": { "value": "RHEL7_CALM" }, "context": calm_bp_service, "name": "image_name"},
    { "value": { "value": "1.0.1" }, "context": calm_bp_service, "name": "image_version"},
]