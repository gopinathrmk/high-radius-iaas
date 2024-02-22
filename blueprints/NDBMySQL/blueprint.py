# THIS FILE IS AUTOMATICALLY GENERATED.
# Disclaimer: Please test this file before using in production.
"""
Generated blueprint DSL (.py)
"""

import json  # no_qa
import os  # no_qa

from calm.dsl.builtins import *  # no_qa


# Secret Variables

#BP_CRED_DB_SERVER_KEY = read_local_file("BP_CRED_DB_SERVER_KEY")
BP_CRED_DB_SERVER_BASIC_PASSWORD = read_local_file("BP_CRED_DB_SERVER_BASIC_PASSWORD")
BP_CRED_PC_PASSWORD = read_local_file("BP_CRED_PC_PASSWORD")
BP_CRED_NDB_PASSWORD = read_local_file("BP_CRED_NDB_PASSWORD")
Profile_NC2_AWS_Action_Clone_variable_CLONE_ROOT_PASS = read_local_file(
    "Profile_NC2_AWS_Action_Clone_variable_CLONE_ROOT_PASS"
)
Profile_NC2_AWS_Action_Restore_variable_CLONE_ROOT_PASS = read_local_file(
    "Profile_NC2_AWS_Action_Restore_variable_CLONE_ROOT_PASS"
)
Profile_NC2_AWS_variable_DB_PASS = read_local_file("Profile_NC2_AWS_variable_DB_PASS")

# Credentials
#BP_CRED_DB_SERVER = basic_cred(
#    "era",
#    BP_CRED_DB_SERVER_KEY,
#    name="DB_SERVER",
#    type="KEY",
#    default=True,
#    editables={"username": False, "secret": True},
#)
BP_CRED_DB_SERVER_BASIC = basic_cred(
    "era",
    BP_CRED_DB_SERVER_BASIC_PASSWORD,
    name="DB_SERVER_BASIC",
    type="PASSWORD",
    default=True,
    editables={"username": False, "secret": True},
)
BP_CRED_PC = basic_cred(
    "admin",
    BP_CRED_PC_PASSWORD,
    name="PC",
    type="PASSWORD",
)
BP_CRED_NDB = basic_cred(
    "admin",
    BP_CRED_NDB_PASSWORD,
    name="NDB",
    type="PASSWORD",
)


class NDB_Service(Service):

    CLEANUP_OPERATION_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DELETE_DB_OPERATION_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    CLUSTER_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    COMPUTE_PROF_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    CREATE_OPERATION_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    TIME_MACHINE_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DB_ENTITY_NAME = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DB_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DB_PARAM_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    REGISTER_OPERATION_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DEREGISTER_OPERATION_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    NETWORK_PROF_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    SLA_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    SOFTWARE_PROF_VERSION_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    SOFTWARE_PROF_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DB_SERVER_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DB_SERVER_IP = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DB_SNAPSHOT_ID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    PC_VM_UUID = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    INNODB_POOL_SIZE = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )

    DB_SOFT_DIR = CalmVariable.Simple(
        "", label="", is_mandatory=False, is_hidden=False, runtime=False, description=""
    )


class NDB_Provisioning(Substrate):

    os_type = "Linux"
    provider_type = "EXISTING_VM"
    provider_spec = read_provider_spec(
        os.path.join("specs", "NDB_Provisioning_provider_spec.yaml")
    )

    readiness_probe = readiness_probe(
        connection_type="SSH",
        disabled=True,
        retries="5",
        connection_port=22,
        address="ndb.nutanix.local",
        delay_secs="30",
    )


class MySQL_VM(Substrate):

    os_type = "Linux"
    provider_type = "EXISTING_VM"
    provider_spec = read_provider_spec(
        os.path.join("specs", "MySQL_VM_provider_spec.yaml")
    )

    readiness_probe = readiness_probe(
        connection_type="SSH",
        disabled=True,
        retries="5",
        connection_port=22,
        address="@@{ip_address}@@",
        delay_secs="30",
    )


class MySQL(Service):

    dependencies = [ref(NDB_Service)]


class NDB_PKG(Package):

    services = [ref(NDB_Service)]

    @action
    def __install__():

        CalmTask.SetVariable.escript(
            name="GetClusterID",
            filename=os.path.join(
                "scripts", "Package_NDB_PKG_Action___install___Task_GetClusterID.py"
            ),
            target=ref(NDB_Service),
            variables=["CLUSTER_ID"],
        )

        CalmTask.SetVariable.escript(
            name="GetProfileIDs",
            filename=os.path.join(
                "scripts", "Package_NDB_PKG_Action___install___Task_GetProfileIDs.py"
            ),
            target=ref(NDB_Service),
            variables=[
                "SOFTWARE_PROF_ID",
                "SOFTWARE_PROF_VERSION_ID",
                "COMPUTE_PROF_ID",
                "NETWORK_PROF_ID",
                "DB_PARAM_ID",
            ],
        )

        CalmTask.SetVariable.escript(
            name="GetSLAID",
            filename=os.path.join(
                "scripts", "Package_NDB_PKG_Action___install___Task_GetSLAID.py"
            ),
            target=ref(NDB_Service),
            variables=["SLA_ID"],
        )

        CalmTask.SetVariable.escript(
            name="ProvisionDB",
            filename=os.path.join(
                "scripts", "Package_NDB_PKG_Action___install___Task_ProvisionDB.py"
            ),
            target=ref(NDB_Service),
            variables=["CREATE_OPERATION_ID"],
        )

        CalmTask.SetVariable.escript(
            name="MonitorOperation",
            filename=os.path.join(
                "scripts", "Package_NDB_PKG_Action___install___Task_MonitorOperation.py"
            ),
            target=ref(NDB_Service),
            variables=["DB_ENTITY_NAME"],
        )

        CalmTask.SetVariable.escript(
            name="GetDatabaseInfo",
            filename=os.path.join(
                "scripts", "Package_NDB_PKG_Action___install___Task_GetDatabaseInfo.py"
            ),
            target=ref(NDB_Service),
            variables=[
                "DB_ID",
                "TIME_MACHINE_ID",
                "DB_SERVER_ID",
                "DB_SERVER_IP",
                "PC_VM_UUID",
            ],
        )

    @action
    def __uninstall__():

        CalmTask.SetVariable.escript(
            name="CleanupDB",
            filename=os.path.join(
                "scripts", "Package_NDB_PKG_Action___uninstall___Task_CleanupDB.py"
            ),
            target=ref(NDB_Service),
            variables=["CLEANUP_OPERATION_ID"],
        )

        CalmTask.Exec.escript(
            name="MonitorCleanupOp",
            filename=os.path.join(
                "scripts",
                "monitor_cleanup_db.py",
            ),
            target=ref(NDB_Service),
        )

        CalmTask.Exec.escript(
            name="ShutdownDBServer",
            filename=os.path.join(
                "scripts",
                "Package_NDB_PKG_Action___uninstall___Task_ShutdownDBServer.py",
            ),
            target=ref(NDB_Service),
        )

        CalmTask.SetVariable.escript(
            name="Delete DB Server VM",
            filename=os.path.join(
                "scripts", "delete_db_server_vm.py"
            ),
            target=ref(NDB_Service),
            variables=["DELETE_DB_OPERATION_ID"],
        )

        CalmTask.Exec.escript(
            name="Monitor Delete DB Server",
            filename=os.path.join(
                "scripts", "monitor_delete_db_server.py",
            ),
            target=ref(NDB_Service),
        )

        
    #    with parallel() as p2:
    #        with branch(p2):
    #            CalmTask.Exec.escript(
    #                name="SkipDeleteDBServer",
    #                filename=os.path.join(
    #                    "scripts",
    #                    "Package_NDB_PKG_Action___uninstall___Task_SkipDeleteDBServer.py",
    #                ),
    #                target=ref(NDB_Service),
    #            )
    #        with branch(p2):
    #            CalmTask.Exec.escript(
    #                name="ShutdownDBServer",
    #                filename=os.path.join(
    #                    "scripts",
    #                    "Package_NDB_PKG_Action___uninstall___Task_ShutdownDBServer.py",
    #                ),
    #                target=ref(NDB_Service),
    #            )


class MySQL_PKG(Package):

    services = [ref(MySQL)]


class f9a4c530_deployment(Deployment):

    min_replicas = "1"
    max_replicas = "1"
    default_replicas = "1"

    packages = [ref(NDB_PKG)]
    substrate = ref(NDB_Provisioning)


class _66f2fcac_deployment(Deployment):

    name = "66f2fcac_deployment"
    min_replicas = "1"
    max_replicas = "1"
    default_replicas = "1"

    packages = [ref(MySQL_PKG)]
    substrate = ref(MySQL_VM)


class NC2_AWS(Profile):

    deployments = [f9a4c530_deployment, _66f2fcac_deployment]

    DB_SIZE = CalmVariable.Simple(
        "200",
        label="Provide Database Size (GB)",
        regex="^[\d]*$",
        validate_regex = True,
        is_mandatory=True,
        is_hidden=False,
        runtime=True,
        description="",
    )

    DB_PASS = CalmVariable.Simple.Secret(
        Profile_NC2_AWS_variable_DB_PASS,
        label="Provide Root Password",
        #regex="^.*$",
        validate_regex=False,
        is_mandatory=False,
        is_hidden=False,
        runtime=True,
        description="",
    )

    DB_NAME = CalmVariable.Simple(
        "mysqldb",
        label="Provide Name For Initial Database",
        is_mandatory=True,
        is_hidden=False,
        runtime=True,
        description="",
    )

    SLA = CalmVariable.WithOptions.FromTask(
        CalmTask.Exec.escript(
            name="",
            filename=os.path.join(
                "scripts", "list_slas.py"
            ),
        ),
        label="Select SLA For Snapshots/PITR Data Retention",
        is_mandatory=True,
        is_hidden=False,
        description="",
    )

    DB_PARAMETERS = CalmVariable.WithOptions.FromTask(
        CalmTask.Exec.escript(
            name="",
            filename=os.path.join(
                "scripts", "get_db_parameters.py"
            ),
        ),
        label="Select Database Parameter Profile",
        regex=".*[Pp][Oo][Ss][Tt][Gg][Rr][Ee][Ss].*",
        validate_regex=False,
        is_mandatory=True,
        is_hidden=False,
        description="",
    )

    SOFT_PROFILE = CalmVariable.WithOptions.FromTask(
        CalmTask.Exec.escript(
            name="",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_variable_SOFT_PROFILE_Task_SampleTask.py"
            ),
        ),
        label="Select Database Software Profile",
        regex="^.*$",
        validate_regex=False,
        is_mandatory=False,
        is_hidden=False,
        description="",
    )

    NETWORK_PROFILE = CalmVariable.WithOptions.FromTask(
        CalmTask.Exec.escript(
            name="",
            filename=os.path.join(
                "scripts", "get_network_profile.py"
            ),
        ),
        label="Select Database Network Profile",
        regex="[Pp][Oo][Ss][Tt][Gg][Rr][Ee][Ss].*",
        validate_regex=False,
        is_mandatory=True,
        is_hidden=False,
        description="",
    )

    COMPUTE_PROFILE = CalmVariable.WithOptions.FromTask(
        CalmTask.Exec.escript(
            name="",
            filename=os.path.join(
                "scripts", "get_compute_profile.py"
            ),
        ),
        label="Select Database Compute Profile",
        regex="[Dd][Ee][Ff][Aa][Uu][Ll][Tt].*",
        validate_regex=False,
        is_mandatory=True,
        is_hidden=False,
        description="",
    )

    cluster_name = CalmVariable.WithOptions.FromTask(
        CalmTask.Exec.escript(
            name="",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_variable_cluster_name_SampleTask.py"
            ),
        ),
        label="Cluster",
        is_mandatory=True,
        is_hidden=False,
        description="",
    )    

    NDB_public_key = CalmVariable.Simple.Secret(
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4Uh4sTFla3SJTKl9UQn8kShGo8ndvZwvx2nqmU8g1FSE3V5E3umXsHEdU5E/6t2pIHEVZSZDwRbDgC2q5vALpLaz7KtfzgbwBHQtgiVTOht1dZLSSi99iGZyO4lYXF50BXAjEJXsQXzNAMLVNfTNWcQfPAGuPwYVhzVMcQjSxS4jlnG3sHa+cLodAhiE4aaRnB1rdqBgJqgQHCFEU0Fd4EQRQNrT9dyS9Dm3eC03PKBq8nnTy1ldM4IlUzm18LqkgWSUbRJSwcwvvXCjhaaxAnO7ge53qA3w1WYMhLIIJfx0LLIa8Yn2Xzxo1aqkHTtHrpV9k7bSF3AO2RhaWGjbj era@mysqlsource",
        label="",
        is_mandatory=False,
        is_hidden=False,
        runtime=False,
        description="",
    )
    NDB_IP = CalmVariable.Simple(
        "10.136.232.103",
        label="",
        is_mandatory=False,
        is_hidden=True,
        runtime=False,
        description="",
    )

    PC_IP = CalmVariable.Simple(
        "10.136.232.39",
        label="",
        is_mandatory=False,
        is_hidden=True,
        runtime=False,
        description="",
    )    

    @action
    def Snapshot():
        """Create Time Machine Snapshot"""

        DB_SNAPSHOT_NAME = CalmVariable.Simple(
            "",
            label="Snapshot Name",
            is_mandatory=True,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.Exec.escript(
            name="SnapshotDatabase",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Snapshot_Task_SnapshotDatabase.py"
            ),
            target=ref(NDB_Service),
        )

    @action
    def DeleteDatabaseAndRetainTimeMachine(
        name="Delete Database And Retain Time Machine",
    ):
        """This will unregister database from NDB and delete the database on VM. Time Machine (Snapshots/PITR Data) and Database Server will be retained for future cloning or creating a copy."""

        CalmTask.SetVariable.escript(
            name="CleanupDB",
            filename=os.path.join(
                "scripts",
                "Profile_NC2_AWS_Action_DeleteDatabaseAndRetainTimeMachine_Task_CleanupDB.py",
            ),
            target=ref(NDB_Service),
            variables=["CLEANUP_OPERATION_ID"],
        )

        CalmTask.Exec.escript(
            name="MonitorCleanupOp",
            filename=os.path.join(
                "scripts",
                "monitor_cleanup_db.py",
            ),
            target=ref(NDB_Service),
        )

    @action
    def ScaleCompute(name="Scale Compute"):
        """Scale Compute And Configure MySQL innodb_buffer_pool_size in my.cnf"""

        RAM = CalmVariable.Simple.int(
            "0",
            label="RAM To Add (GB)",
            regex="^[\d]*$",
            validate_regex=False,
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CPU = CalmVariable.Simple.int(
            "0",
            label="CPU To Add",
            regex="^[\d]*$",
            validate_regex=False,
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.Exec.escript(
            name="Check",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_ScaleCompute_Task_Check.py"
            ),
            target=ref(NDB_Service),
        )

        CalmTask.SetVariable.escript(
            name="Add Resources",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_ScaleCompute_Task_AddResources.py"
            ),
            target=ref(NDB_Service),
            variables=["DB_SOFT_DIR", "INNODB_POOL_SIZE"],
        )

        CalmTask.Delay(name="Wait", delay_seconds=20, target=ref(NDB_Service))

        CalmTask.Exec.ssh(
            name="Configure DB Parameters",
            filename=os.path.join(
                "scripts",
                "Profile_NC2_AWS_Action_ScaleCompute_Task_ConfigureDBParameters.sh",
            ),
            cred=ref(BP_CRED_DB_SERVER_BASIC),
            target=ref(MySQL),
        )

    @action
    def ScaleDataArea(name="Scale Data Area"):
        """Increase log and data area VGs"""

        DISK = CalmVariable.Simple.int(
            "0",
            label="Disk To Add (GB)",
            regex="^[\d]*$",
            validate_regex=False,
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.Exec.escript(
            name="Check",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_ScaleDataArea_Task_Check.py"
            ),
            target=ref(NDB_Service),
        )

        CalmTask.Exec.escript(
            name="Expand VG Disks",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_ScaleDataArea_Task_ExpandVGDisks.py"
            ),
            target=ref(NDB_Service),
        )

        CalmTask.Delay(name="Wait", delay_seconds=20, target=ref(NDB_Service))

        CalmTask.Exec.ssh(
            name="Expand LV OS",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_ScaleDataArea_Task_ExpandLVOS.sh"
            ),
            cred=ref(BP_CRED_DB_SERVER_BASIC),
            target=ref(MySQL),
        )

    @action
    def DBServerPowerAction(name="DB Server Power Action"):
        """Shutdown, Power on, Reboot DB server"""

        POWER_ACTION = CalmVariable.WithOptions(
            ["Shutdown", "Reboot", "Power On"],
            label="Select Power Action",
            default="Shutdown",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.Exec.escript(
            name="PowerAction",
            filename=os.path.join(
                "scripts",
                "Profile_NC2_AWS_Action_DBServerPowerAction_Task_PowerAction.py",
            ),
            target=ref(NDB_Service),
        )

    @action
    def Clone():
        """Clone database. Time machine will not be created."""

        CLONE_ROOT_PASS = CalmVariable.Simple.Secret(
            Profile_NC2_AWS_Action_Clone_variable_CLONE_ROOT_PASS,
            label="Root Password For Cloned DB",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        DB_PARAMETERS = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts","get_db_parameters.py",
                ),
            ),
            label="Select Database Parameter Profile For Clone",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        NETWORK_PROFILE = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts","get_network_profile.py",
                ),
            ),
            label="Select Network Profile For Clone",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        COMPUTE_PROFILE = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts",
                    "get_compute_profile.py",
                ),
            ),
            label="Select Compute Profile For Clone",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        CLONE_INSTANCE_NAME = CalmVariable.Simple(
            "@@{calm_application_name}@@-clone",
            label="Provide Cloned DB Instance Name",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CLONE_VM_NAME = CalmVariable.Simple(
            "@@{calm_application_name}@@-clone",
            label="Provide Name For Cloned VM",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        RESTORE_DATE_TIME = CalmVariable.Simple.datetime(
            "19/11/2023 - 00:00:00",
            label="Select Date-Time To Clone (If PITR Is Selected Above)",
            regex="^((0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/[12]\d{3})(\s-\s)([0-1]\d|2[0-3]):[0-5]\d(:[0-5]\d)?$",
            validate_regex=False,
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        RESTORE_SNAPSHOT_NAME = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts",
                    "list_snapshots.py",
                ),
            ),
            label="Select Snapshot To Clone",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        RESTORE_TYPE = CalmVariable.WithOptions(
            ["Snapshot", "PITR"],
            label="Choose To Clone From Snapshot Or PITR",
            default="Snapshot",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.SetVariable.escript(
            name="GetSnapshotId",
            filename=os.path.join(
                "scripts", "get_snapshot_id.py"
            ),
            target=ref(NDB_Service),
            variables=["DB_SNAPSHOT_ID"],
        )

        CalmTask.SetVariable.escript(
            name="GetProfileIDs",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Clone_Task_GetProfileIDs.py"
            ),
            target=ref(NDB_Service),
            variables=["COMPUTE_PROF_ID", "NETWORK_PROF_ID", "DB_PARAM_ID"],
        )

        CalmTask.SetVariable.escript(
            name="ProvisionClone",
            filename=os.path.join(
                "scripts", "provision_clone.py"
            ),
            target=ref(NDB_Service),
            variables=["CREATE_OPERATION_ID"],
        )

        CalmTask.Exec.escript(
            name="MonitorClone",
            filename=os.path.join(
                "scripts", "monitor_clone.py"
            ),
            target=ref(NDB_Service),
        )

    @action
    def Restore():
        """Restore database to a new server. New Time machine will be created."""

        CLONE_ROOT_PASS = CalmVariable.Simple.Secret(
            Profile_NC2_AWS_Action_Restore_variable_CLONE_ROOT_PASS,
            label="Root Password For Restored DB",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        SLA = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts",
                    "list_slas.py",
                ),
            ),
            label="Select SLA For Restored DB",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        DB_PARAMETERS = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts","get_db_parameters.py",
                ),
            ),
            label="Select Database Parameter Profile For Restored DB",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        NETWORK_PROFILE = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts","get_network_profile.py",
                ),
            ),
            label="Select Network Profile For Restored DB",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        COMPUTE_PROFILE = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts",
                    "get_compute_profile.py",
                ),
            ),
            label="Select Compute Profile For Restored DB",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        CLONE_INSTANCE_NAME = CalmVariable.Simple(
            "@@{calm_application_name}@@-restored",
            label="Provide Restored DB Instance Name",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CLONE_VM_NAME = CalmVariable.Simple(
            "@@{calm_application_name}@@-restored",
            label="Provide Name For Restored DB VM",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        RESTORE_DATE_TIME = CalmVariable.Simple.datetime(
            "19/11/2023 - 00:00:00",
            label="Select Date-Time To Restore From (If PITR Is Selected Above)",
            regex="^((0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/[12]\d{3})(\s-\s)([0-1]\d|2[0-3]):[0-5]\d(:[0-5]\d)?$",
            validate_regex=False,
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        RESTORE_SNAPSHOT_NAME = CalmVariable.WithOptions.FromTask(
            CalmTask.Exec.escript(
                name="",
                filename=os.path.join(
                    "scripts",
                    "list_snapshots.py",
                ),
            ),
            label="Select Snapshot To Restore From",
            is_mandatory=False,
            is_hidden=False,
            description="",
        )
        RESTORE_TYPE = CalmVariable.WithOptions(
            ["Snapshot", "PITR"],
            label="Choose To Restore From Snapshot Or PITR",
            default="Snapshot",
            is_mandatory=False,
            is_hidden=False,
            runtime=True,
            description="",
        )
        CalmTask.SetVariable.escript(
            name="GetSnapshotId",
            filename=os.path.join(
                "scripts", "get_snapshot_id.py"
            ),
            target=ref(NDB_Service),
            variables=["DB_SNAPSHOT_ID"],
        )

        CalmTask.SetVariable.escript(
            name="GetProfileIDs",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Restore_Task_GetProfileIDs.py"
            ),
            target=ref(NDB_Service),
            variables=["COMPUTE_PROF_ID", "NETWORK_PROF_ID", "DB_PARAM_ID"],
        )

        CalmTask.SetVariable.escript(
            name="ProvisionClone",
            filename=os.path.join(
                "scripts", "provision_clone.py"
            ),
            target=ref(NDB_Service),
            variables=["CREATE_OPERATION_ID"],
        )

        CalmTask.Exec.escript(
            name="MonitorClone",
            filename=os.path.join(
                "scripts", "monitor_clone.py"
            ),
            target=ref(NDB_Service),
        )

        CalmTask.SetVariable.escript(
            name="UnregisterClone",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Restore_Task_UnregisterClone.py"
            ),
            target=ref(NDB_Service),
            variables=["CLEANUP_OPERATION_ID"],
        )

        CalmTask.Exec.escript(
            name="MonitorUnregister",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Restore_Task_MonitorUnregister.py"
            ),
            target=ref(NDB_Service),
        )

        CalmTask.SetVariable.escript(
            name="GetSLAID",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Restore_Task_GetSLAID.py"
            ),
            target=ref(NDB_Service),
            variables=["SLA_ID"],
        )

        CalmTask.SetVariable.escript(
            name="ImportCloneAsNew",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Restore_Task_ImportCloneAsNew.py"
            ),
            target=ref(NDB_Service),
            variables=["REGISTER_OPERATION_ID"],
        )

        CalmTask.Exec.escript(
            name="MonitorImport",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_Restore_Task_MonitorImport.py"
            ),
            target=ref(NDB_Service),
        )

    @action
    def LogCatchUp(name="Log Catch Up"):
        """Perform log catch up operation on DB."""

        CalmTask.Exec.escript(
            name="LogCatchUp",
            filename=os.path.join(
                "scripts", "Profile_NC2_AWS_Action_LogCatchUp_Task_LogCatchUp.py"
            ),
            target=ref(NDB_Service),
        )


class NDBMySQL(Blueprint):
    """MYSQL_SERVER_IP: @@{NDB_Service.DB_SERVER_IP}@@"""

    services = [NDB_Service, MySQL]
    packages = [NDB_PKG, MySQL_PKG]
    substrates = [NDB_Provisioning, MySQL_VM]
    profiles = [NC2_AWS]
    credentials = [BP_CRED_DB_SERVER_BASIC, BP_CRED_PC, BP_CRED_NDB]
