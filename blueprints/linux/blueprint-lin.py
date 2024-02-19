"""
Linux Server on AHV Multi-VM Blueprint
"""

import json
import os
import sys
from ruamel import yaml

from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import (
    Deployment,
    Profile,
    Blueprint,
)
from calm.dsl.builtins import *
from calm.dsl.builtins import action, parallel, ref, basic_cred, CalmVariable, CalmTask
from calm.dsl.builtins import vm_disk_package, read_file, read_local_file, file_exists
from calm.dsl.builtins import AppEdit, PatchField, AhvUpdateConfigAttrs
from calm.dsl.builtins import vm_disk_package, AhvVm, AhvVmDisk, AhvVmNic
from calm.dsl.builtins import AhvVmGC, AhvVmResources, ahv_vm, read_ahv_spec, read_spec, readiness_probe
from calm.dsl.runbooks import CalmEndpoint as Endpoint
from calm.dsl.store import *

PROJECT_ROOT = os.environ['PROJECT_ROOT']
SELF_SERVICE_ADDRESS = os.environ['CALM_IP_ADDRESS']
SELF_SERVICE_USERNAME = os.environ['CALM_USER']
SELF_SERVICE_SECRET = os.environ['CALM_PASS']
CALM_PROJECT = os.environ['CALM_PROJECT']

######################################################### ENV management ##########################################################################
# Add this section in your bps/rbs to bring the environment parameters and scripts
#
# All common references start with common config file, which path is located in the make variable COMMON_CONFIG_FILE.
#
# All bp/rb specific references start with the bp/rb config file, which path is located in the make variable USECASE_CONFIG_FILE.
#
# COMMON_CONFIG_FILE contains paths of parameters files (JSONs) and folders containing scripts used by all bps/rbs.
#
# USECASE_CONFIG_FILE contains paths of parameters files (JSONs) and folders containing scripts used specifically by the use case.
# todo: config files should be templetised for customization by the calling context (makefile or pielines) --> in the future templates should
#         be committed to the source code repo
# todo: how to manage secrets from the calling context
#                     (configs created on the fly from template then deleted ?, directly passed to sys env variables instead of files?)
# The DSL_HELPERS_FOLDER (first reference in the COMMON_CONFIG_FILE json) gets variables and scripts within the repo folder structure to be used
#    in the bp/rb Python file during runtime (inside the locals() dict) as Python variables.
###################################################################################################################################################

# CALM_ENVIRONMENT is exported via Makefile, otherwise, set environment variable on local machine
CALM_ENVIRONMENT = os.environ['CALM_ENVIRONMENT'].lower()
CALM_ENV_CONFIG_PATH = os.path.join("../../.local",CALM_ENVIRONMENT,(CALM_ENVIRONMENT + "-config.json"))
#CALM_ENV_CONFIG = json.loads(read_file(CALM_ENV_CONFIG_PATH))
#region get the common config
COMMON_CONFIG_FILE = os.environ["COMMON_CONFIG_FILE"]
COMMON_CONFIG = json.load(open(COMMON_CONFIG_FILE))
COMMON_CONFIG = {k: v.replace(".", PROJECT_ROOT, 1) for k,v in COMMON_CONFIG.items()}

#endregion

#region get the use case config
USECASE_CONFIG_FILE = os.environ["USECASE_CONFIG_FILE"]
USECASE_CONFIG = json.load(open(USECASE_CONFIG_FILE))
#endregion

#region helper functions
DSL_HELPERS_FOLDER = COMMON_CONFIG["DSL_HELPERS_FOLDER"]
sys.path.insert(0, DSL_HELPERS_FOLDER)
from dsl_helpers import *
del(locals()["DSL_HELPERS_FOLDER"]) #delete the variable because it will be loaded again by the helper function which is now available
#endregion

#region Bring the environment
failexec = False
# Load the parameters from the use case config file
failexec = loadEnvVarsFromFile(path=USECASE_CONFIG_FILE, dict=locals()) or failexec
# Load the common environment parameters
failexec = loadEnvVarsFromFile(path=CALM_ENV_CONFIG_PATH, dict=locals()) or failexec
# Load the common lib scripts
failexec = loadScriptsFromFolder(path=COMMON_CONFIG["COMMON_LIB_FOLDER"], dict=locals()) or failexec
# Load the common tasks scripts
failexec = loadScriptsFromFolder(path=COMMON_CONFIG["COMMON_TASKS_FOLDER"], dict=locals()) or failexec
# Load the Day2 tasks scripts
failexec = loadScriptsFromFolder(path=COMMON_CONFIG["DAY2_TASKS_FOLDER"], dict=locals()) or failexec
# Load the use case specific environment parameters
# Load the use case specific environment parameters
failexec = loadEnvVarsFromFile(path=USECASE_CONFIG["USECASE_ENV_FILE"], dict=locals()) or failexec
# Load the use case specific lib scripts
#failexec = loadScriptsFromFolder(path=USECASE_CONFIG["USECASE_LIB_FOLDER"], dict=locals()) or failexec
# Load the use case tasks scripts
#failexec = loadScriptsFromFolder(path=USECASE_CONFIG["USECASE_TASKS_FOLDER"], dict=locals()) or failexec
if failexec:
    exit(1)
#endregion
####################################################################################################################################################
######################################################### ENV management END #######################################################################
####################################################################################################################################################
######################################################################

COMMON_TASK_LIBRARY = "../common_task_library/"
#CALM_LINUX_ENDPOINT = ['BLUEPRINT_ENDPOINTS']['LINUX_ENDPOINT_NAME']
#CALM_WINDOWS_ENDPOINT = CALM_ENV_CONFIG['endpoints']['windows_endpoint_name']

ENV_AHV_NAME = "default"

### END VARIABLES
######################################################################

### DEFINE SECRET VARIABLES
######################################################################
if file_exists(f"{blueprint_variables['linux_os_cred_private_key_path']}"):
    ssh_private_key = read_local_file(f"{blueprint_variables['linux_os_cred_private_key_path']}")
else:
    print('The ssh private key does not exist in the path specified.')
### END SECRET VARIABLES
#####################################################################

### DEFINE CREDENTIALS
BP_CRED_linux = basic_cred(blueprint_variables["linux_default_creds_username"], password=ssh_private_key, name="cred_linux", type='KEY',default=True)

### END CREDENTIALS
#####################################################################

#####################################################################
### DEFINE DOWNLOADABLE IMAGE
disk_package = vm_disk_package(
    name="disk_package",
    description="",
    config={
        "name": "disk_package",
        "image": {
            "name": "@@{VM_Provision.image_name}@@",
            "type": "DISK_IMAGE",
            "source": "@@{VM_Provision.image_source}@@",
            "architecture": "X86_64",
        },
        "product": {"name": "win", "version": "@@{VM_Provision.image_version}@@"},
        "checksum": {},
    },
)
### END DOWNLOADABLE IMAGE
####################################################################

####################################################################
# DEFINE SERVICE
class VM_Provision(Service):
    image_source = CalmVariable.WithOptions.FromTask(CalmTask.Exec.escript(script="print('@@{IMAGE_INFO}@@'.split(' - ')[1])"),label="OS Image Source", is_hidden=False, is_mandatory=True)
    image_name = CalmVariable.WithOptions.FromTask(CalmTask.Exec.escript(script="print('@@{IMAGE_INFO}@@'.split(' - ')[0])"),label="OS Image Name", is_hidden=False, is_mandatory=True)
    image_version = CalmVariable.WithOptions.FromTask(CalmTask.Exec.escript(script="print('@@{IMAGE_INFO}@@'.split(' - ')[2])"),label="OS Image Version", is_hidden=False, is_mandatory=True)
    rp_name = CalmVariable.Simple("",is_mandatory=False,runtime=False,is_hidden=True,)
    local_az_url = CalmVariable.Simple("",is_mandatory=False,runtime=False,is_hidden=True,)
    primary_cluster_uuid = CalmVariable.Simple("",is_mandatory=False,runtime=False,is_hidden=True,)
    recovery_cluster_uuid = CalmVariable.Simple("",is_mandatory=False,runtime=False,is_hidden=True,)

    @action
    def Reserve_IP_Infoblox():
        CalmTask.Exec.escript(name="Reserve IP Addresses with Infoblox",script=build_task_script(script_file_name="reserve_ip_infoblox.py", dict=locals()),)

### END SERVICE
#####################################################################

#####################################################################
### DEFINE PACKAGE
# DEFINE AHV PACKAGE FOR INHERITANCE
class AHVPackage_Default(Package):
    services = [ref(VM_Provision)]

    @action
    def __install__():
        VM_Provision.Reserve_IP_Infoblox(name="Reserve IP Addresses with Infoblox")

### END PACKAGE
##############################################################

#############################################################
### DEFINE AHV RESOURCES
class AhvVmResources_Default(AhvVmResources):

    memory = 8
    vCPUs = 1
    cores_per_vCPU = 2
    disks = [AhvVmDisk.Disk.Scsi.cloneFromVMDiskPackage(disk_package, bootable=True),
             AhvVmDisk.Disk.Scsi.allocateOnStorageContainer(20),]
    nics = [AhvVmNic.NormalNic.ingress("@@{subnet_prod.uuid}@@", vpc="@@{tenant_vpc_uuid}@@"),
            AhvVmNic.NormalNic.ingress("@@{subnet_admin.uuid}@@", vpc="@@{tenant_vpc_uuid}@@")]

    guest_customization = AhvVmGC.CloudInit(
        filename=os.path.join("specs", "cloud_init.yaml")
    )

### END AHV RESOURCES
##############################################################

#############################################################
### DEFINE SUBSTRATE
class AHVSubstrate_Default(Substrate):
    """AHV VM Default Substrate"""

    os_type = "Linux"
    provider_type = "AHV_VM"
    provider_spec = ahv_vm(
        name="@@{hostname}@@",
        resources = AhvVmResources_Default,
        cluster = Ref.Cluster(name="@@{target_cluster.uuid}@@"),
        categories = {"AppFamily": "Demo", "AppType": "Default", "BackupECHO_IAAS": "Standard"}
    )
    provider_spec_editables = read_spec(os.path.join("specs", "ahv_create_spec_editables.yaml"))
    readiness_probe = readiness_probe(connection_type="SSH",disabled=False,retries="5",connection_port=22,address="@@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@@",delay_secs="30",credential=ref(BP_CRED_linux),)

    @action
    def __pre_create__():
        CalmTask.SetVariable.escript(name="Get Remote PC Address",script=build_task_script(script_file_name="get_remote_pc_address.py", dict=locals()),variables=["PC_PROVIDER_ADDRESS"],)
        CalmTask.SetVariable.escript(name="Set Hostname",script=build_task_script(script_file_name="set_vm_name.py", dict=locals()),variables=["hostname"],)
        CalmTask.SetVariable.escript(name="Create Security Zone Subnet if needed",script=build_task_script(script_file_name="pc_flow_vpc_add_externally_routable_ips_overlay_subnet.py", dict=locals()),variables=["default_subnet_ip", "default_subnet_mask","default_subnet_cidr","default_subnet_len"],)
        CalmTask.SetVariable.escript(name="Get Overlay Subnets from Project",script=build_task_script(script_file_name="get_project_subnets.py", dict=locals()),variables=["tenant_vpc_uuid","subnet_prod","subnet_admin"],)
        CalmTask.SetVariable.escript(name="Get Target Cluster",script=build_task_script(script_file_name="determine_cluster.py", dict=locals()),variables=["target_cluster"],)

    @action
    def __post_delete__():
        #CalmTask.Exec.powershell(name="UnJoin_Domain",filename=COMMON_TASK_LIBRARY +  "windows/postdelete/domain_unjoin/ad-domain-unjoin.ps1",target_endpoint=Endpoint.use_existing(CALM_ENDPOINT),)
        CalmTask.Exec.escript(name="Release InfoBlox IP",script=build_task_script(script_file_name="release_ip_infoblox.py", dict=locals()),)
        CalmTask.Exec.escript(name="Delete Security Policy",script=build_task_script(script_file_name="delete_security_policy.py", dict=locals()),)

### END SUBSTRATE
#############################################################

#############################################################
### DEFINE DEPLOYMENT
# DEFINE AHV DEPLOYMENT FOR INHERITANCE

class AHVDeployment_Default(Deployment):
    packages = [ref(AHVPackage_Default)]
    substrate = ref(AHVSubstrate_Default)
    min_replicas = "1"
    max_replicas = "10"
    default_replicas = "@@{number_of_vms}@@"

### END DEPLOYMENT
###############################################################

### BEGIN AHV CONFIG
###############################################################
class AhvUpdateAttrsModifyCompute(AhvUpdateConfigAttrs):
    """AHV VM update Compute attrs"""

    memory = PatchField.Ahv.vcpu(value="2", operation="increase", min_val=0, max_val=16384, editable=True)
    vcpu = PatchField.Ahv.vcpu(value="2", operation="increase", min_val=0, max_val=4, editable=True)
    numsocket = PatchField.Ahv.vcpu(value="2", operation="increase", min_val=0, max_val=4, editable=True)

### END AHV CONFIG
###############################################################

###############################################################
### BEGIN PROFILES
# DEFINE THE COMMON PROFILE FOR INHERITANCE (HIDDEN IN GUI)
class Common(Profile):

    PROJECT_NAME = CalmVariable.WithOptions.FromTask(
        #"""Need for Scale-Out/In as they do not expand the Calm macro calm_project_name - JIRA is CALM-26334"""
        #"""Downstream tasks will need to use this macro to get the Calm Project Name when Scale-Out/In is utilized"""
        CalmTask.Exec.escript(name="Get Project Name",script="print('@@{calm_project_name}@@')"))
    SELF_SERVICE_ADDRESS = CalmVariable.Simple(SELF_SERVICE_ADDRESS, label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    SELF_SERVICE_USERNAME = CalmVariable.Simple(SELF_SERVICE_USERNAME, label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    SELF_SERVICE_SECRET = CalmVariable.Simple.Secret(SELF_SERVICE_SECRET,label="",is_mandatory=False,is_hidden=True,runtime=False,description="",)
    SELF_SERVICE_SECURE = CalmVariable.Simple("False", label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    PC_PROVIDER_ADDRESS = CalmVariable.Simple(prism_central_config["PC_PROVIDER_ADDRESS"], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    PC_PROVIDER_USERNAME = CalmVariable.Simple(prism_central_config["PC_PROVIDER_USERNAME"], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    PC_PROVIDER_SECRET = CalmVariable.Simple.Secret(prism_central_config["PC_PROVIDER_SECRET"],label="",is_mandatory=False,is_hidden=True,runtime=False,description="",)
    PC_PROVIDER_SECURE = CalmVariable.Simple("False", label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    HYCU_ADDRESS = CalmVariable.Simple(hycu_config["HYCU_ADDRESS"], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    HYCU_USERNAME = CalmVariable.Simple(hycu_config["HYCU_USERNAME"], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    HYCU_SECRET = CalmVariable.Simple.Secret(hycu_config["HYCU_SECRET"],label="",is_mandatory=False,is_hidden=True,runtime=False,description="",)
    HYCU_SECURE = CalmVariable.Simple("False", label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    INFOBLOX_ADDRESS = CalmVariable.Simple(infoblox_config["INFOBLOX_ADDRESS"], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    INFOBLOX_USERNAME = CalmVariable.Simple(infoblox_config["INFOBLOX_USERNAME"], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    INFOBLOX_SECRET = CalmVariable.Simple.Secret(infoblox_config["INFOBLOX_SECRET"],label="",is_mandatory=False,is_hidden=True,runtime=False,description="",)
    INFOBLOX_SECURE = CalmVariable.Simple("False", label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    INFOBLOX_NETWORKS_SPECS = CalmVariable.Simple.multiline(json.dumps(infoblox_config["INFOBLOX_NETWORKS_SPECS"]),label="CIDR size of the tenant network",is_mandatory=False,is_hidden=True,runtime=(False if infoblox_config["INFOBLOX_NETWORKS_SPECS"] else True),description="CIDR size of the tenant network")
    INFOBLOX_TENANT_EXT_ATTR_NAME = CalmVariable.Simple(infoblox_config["INFOBLOX_TENANT_EXT_ATTR_NAME"],label="Infoblox extensible attribute name for tenant",is_mandatory=False,is_hidden=True,runtime=True,description="Infoblox extensible attribute name for tenant")
    CVM_USERNAME = CalmVariable.Simple(blueprint_variables["cvm_creds_username"], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    CVM_SECRET = CalmVariable.Simple.Secret(blueprint_variables["cvm_creds_secret"],label="",is_mandatory=False,is_hidden=True,runtime=False,description="",)
    WIN2022_IMAGE_LOCATION = CalmVariable.Simple(blueprint_variables['windows_2022_image_location'], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    WIN2019_IMAGE_LOCATION = CalmVariable.Simple(blueprint_variables['windows_2019_image_location'], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    RHEL8_IMAGE_LOCATION = CalmVariable.Simple(blueprint_variables['rhel_8_image_location'], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    RHEL9_IMAGE_LOCATION = CalmVariable.Simple(blueprint_variables['rhel_9_image_location'], label="", is_mandatory=False, is_hidden=True, runtime=False, description="")
    timezone = CalmVariable.Simple(blueprint_variables["timezone"],label="VM Timezone",is_mandatory=False,runtime=False,is_hidden=False,)
    os_cred_public_key = CalmVariable.Simple(blueprint_variables["linux_os_cred_public_key"],label="OS Cred Public Key",is_hidden=False,description="SSH public key for OS CRED user.")
    timezone = CalmVariable.Simple(blueprint_variables["timezone"],label="VM Timezone",is_mandatory=False,runtime=False,is_hidden=True,)
    company_name = CalmVariable.Simple(blueprint_variables["organization"],label="Company Name",is_mandatory=False,runtime=False,is_hidden=True,)
    IMAGE_INFO = CalmVariable.WithOptions.FromTask(CalmTask.Exec.escript(script=GET_IMAGE_INFO),label="Image information",is_mandatory=True,is_hidden=False,description="",)
    number_of_vms = CalmVariable.WithOptions(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],label="The number of VMs to build",default="1",is_mandatory=True,is_hidden=False,runtime=True,description="",)
    domain = CalmVariable.WithOptions(["sddc.vwgroup.com"],label="Active Directory Domain Name",default="sddc.vwgroup.com",is_mandatory=True,is_hidden=True,runtime=True,description="AD Domain",)
    OS = CalmVariable.WithOptions(["RHEL8", "RHEL9"],label="Please select the OS version for the VM",default="RHEL8",is_mandatory=True,is_hidden=False,runtime=True,description="",)
    SECURITY_ZONE = CalmVariable.WithOptions(["APPZONE1", "APPZONE2", "APPZONE3"],label="Please select the network security zone for the VM",default="APPZONE1",is_mandatory=True,is_hidden=False,runtime=True,description="",)
    CLUSTER_SELECTION = CalmVariable.WithOptions.FromTask(CalmTask.Exec.escript(script="{}".format(GET_CLUSTER_SELECTION)),label="Select the Cluster",is_mandatory=True,is_hidden=False,description="")
    CRED_CONFIG = CalmVariable.Simple.multiline(
        #"""In-task credential provider config"""
        value=json.dumps(cyberark_config),label="Used for credential provider macros",is_mandatory=True,runtime=False,is_hidden=True,)
    FETCH_CRED_PY = CalmVariable.Simple.multiline(
        #""" E-Script to fetch credential (used as macro) """
        value=json.dumps(FETCH_CRED_PYTHON),is_mandatory=True,runtime=False,is_hidden=True)
    FETCH_CRED_PS = CalmVariable.Simple.multiline(
        #""" Powershell Script to fetch credential (used as macro) """
        value=json.dumps(FETCH_CRED_POWERSHELL),is_mandatory=True,runtime=False,is_hidden=True)
    #az1_pc_ip = CalmVariable.Simple(blueprint_variables["az1_pc_ip"],label="AZ1_PC_IP",is_mandatory=False,runtime=False,is_hidden=True,)
    #az2_pc_ip = CalmVariable.Simple(blueprint_variables["az2_pc_ip"],label="AZ2_PC_IP",is_mandatory=False,runtime=False,is_hidden=True,)
    cluster_ip = CalmVariable.Simple(blueprint_variables["cluster_ip"],label="Cluster IP",is_mandatory=False,runtime=False,is_hidden=True,)
    linux_ethernet_type = CalmVariable.Simple("eth0",label="VM Timezone",is_mandatory=False,runtime=False,is_hidden=True,)

    patch_list = [
        AppEdit.UpdateConfig(
            "Compute_Config", target=ref(AHVDeployment_Default), patch_attrs=AhvUpdateAttrsModifyCompute
        )
    ]

# DEFINE THE AHV COMMON PROFILE FOR INHERITANCE (HIDDEN IN GUI)
class AHVCOMMON(Profile):
    environments = [Ref.Environment(name=ENV_AHV_NAME)]

    PLATFORM_TYPE = CalmVariable.Simple("nutanix_pc",label="Blueprint Platform Type",is_mandatory=True,runtime=False,is_hidden=True,)

# DEFINE AHV PROFILES

class AHV_Default(Common, AHVCOMMON):
    deployments = [AHVDeployment_Default]

    @action
    def Backup_VMs(name="Backup Application VMs"):
        CalmTask.Exec.escript(name="Backup Application VMs",script=build_task_script(script_file_name="hycu_backup_vm.py", dict=locals()),target=ref(VM_Provision),)

    @action
    def ScaleOut(name="Scale Out"):
        increase_count = CalmVariable.Simple("1",label="",is_mandatory=False,is_hidden=False,runtime=True,description="",)
        CalmTask.Scaling.scale_out("@@{increase_count}@@",name="ScaleOut",target=ref(AHVDeployment_Default),)

    @action
    def ScaleIn(name="Scale In"):
        decrease_count = CalmVariable.Simple("1",label="",is_mandatory=False,is_hidden=False,runtime=True,description="",)
        CalmTask.Scaling.scale_in("@@{decrease_count}@@",name="ScaleIn",target=ref(AHVDeployment_Default),)

    @action
    def planned_failover(name="Failover"):
        CalmTask.SetVariable.escript(
            name="Create Recovery Plan",
            script=build_task_script(script_file_name="w3_11_3_create_recovery_plan.py", dict=locals()),
            variables=["rp_name","local_az_url","primary_cluster_uuid","recovery_cluster_uuid"],
            target=ref(VM_Provision),
        )
        CalmTask.Exec.escript(
            name="Start Failover",
            script=build_task_script(script_file_name="w3_11_4_start_failover.py", dict=locals()),
            target=ref(VM_Provision),
        )
        CalmTask.Exec.escript(
            name="Delete Recovery Plan",
            script=build_task_script(script_file_name="w3_11_5_delete_recovery_plan.py", dict=locals()),
            target=ref(VM_Provision),
        )

    @action
    def update_antiaffinity(name="Update Anti Affinity Rules"):

        action = CalmVariable.WithOptions(
            ["Update", "Delete"],
            label="",
            default="Update",
            is_mandatory=True,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.Exec.ssh(
            name="Update Anti Affinity Rules",
            filename=COMMON_TASK_LIBRARY +  "shared/day2/anti_affinity.sh",
            target_endpoint=Endpoint.use_existing(blueprint_endpoints['linux_endpoint_name']),
            target=ref(VM_Provision),
        )

    @action
    def clone_vm(name="Clone VM"):

        VM_NAME = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="Get Application VM list",
                filename=COMMON_TASK_LIBRARY +  "shared/day2/w3_12_get_app_vms.py"
            ),
            label="Select VM",
            regex="^.*$",
            validate_regex=False,
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        CalmTask.Exec.escript(
            name="Clone VM",
            filename=COMMON_TASK_LIBRARY +  "shared/day2/w3_12_clone_vm.py",
            target=ref(VM_Provision),
        )

# END AHV PROFILES
### END PROFILES
##############################################################

##############################################################
### DEFINE BLUEPRINT

class Linux_BP(Blueprint):
    services = [VM_Provision]
    packages = [AHVPackage_Default, disk_package]
    substrates = [AHVSubstrate_Default]
    profiles = [AHV_Default]
    credentials = [BP_CRED_linux]

### END BLUEPRINT
############################################################

# Setting the Docstring for blueprint to description file contents.
# This file is used for both blueprint and marketplace descriptions.
Linux_BP.__doc__ = read_file('mp_meta/bp-description.md')

def main():
    print(Linux_BP.json_dumps(pprint=True))

if __name__ == "__main__":
    main()