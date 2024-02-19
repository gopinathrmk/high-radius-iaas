#!/bin/bash

#configuring variables
USERNAME="@@{CVM_USERNAME}@@"
PASSWORD="@@{CVM_SECRET}@@"
CVM="@@{cluster_ip}@@"
VM="@@{name}@@"
VM_GROUP_NAME="@@{calm_application_name}@@"
SLEEP_TIME=$((@@{calm_array_index}@@ * 2 + 1))
action = "@@{action}@@"
sleep $SLEEP_TIME

#configuring the vm anti-affinity group
if [ $action = "Update" ] ; then
    GROUP_EXISTS=$(sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${CVM} "/usr/local/nutanix/bin/acli vm_group.list" | grep ${VM_GROUP_NAME})
    if [ -n "$GROUP_EXISTS" ]; then
        echo "Skipping VM group creation as it already exists."
    else
        echo "Adding VM group ${VM_GROUP_NAME}"
        sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${CVM} "/usr/local/nutanix/bin/acli vm_group.create ${VM_GROUP_NAME}"
        echo "Configuring anti-affinity on group ${VM_GROUP_NAME}..."
        sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${CVM} "/usr/local/nutanix/bin/acli vm_group.antiaffinity_set ${VM_GROUP_NAME}"
    fi

    sleep $SLEEP_TIME
    echo "Adding VM ${VM} to group ${VM_GROUP_NAME}..."
    sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${CVM} "/usr/local/nutanix/bin/acli vm_group.add_vms ${VM_GROUP_NAME} vm_list=${VM}"

elif [ $action = "Delete" ]; then
    GROUP_EXISTS=$(sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${CVM} "/usr/local/nutanix/bin/acli vm_group.list" | grep ${VM_GROUP_NAME})
    if [ "$GROUP_EXISTS" ]; then
        echo "Skipping VM group Deletion as it does not exists."
    else
        echo "Removing VM-VM Anti-Affinity Policy ${VM_GROUP_NAME}"
        sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${CVM} "/usr/local/nutanix/bin/acli vm_group.antiaffinity_unset ${VM_GROUP_NAME}"
        sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${CVM} "/usr/local/nutanix/bin/acli vm_group.delete ${VM_GROUP_NAME}"
    fi
fi