#!/bin/bash

echo 'Expand Data And Log Disks'

# Function to recursively expand PVs
expand_pvs() {
    local pv
    
    for pv in $(sudo pvdisplay --noheading -C -o pv_name --separator=' '); do
        # Check if the PV belongs to the VG_MYSQL volume group
        if sudo pvs --noheadings -o vg_name "${pv}" | grep -q "VG_MYSQL"; then
            # resize
            sudo pvresize "${pv}"
        fi
    done
}

# Function to recursively expand LVs
expand_lvs() {
    local lv

    for lv in $(sudo lvdisplay --noheading -C -o lv_name,vg_name --separator=':'); do
        local lv_name=$(echo "$lv" | awk -F: '{print $1}')
        local vg_name=$(echo "$lv" | awk -F: '{print $2}')        
        
        if [[ "$lv_name" == *VG_MYSQL* ]]; then
            sudo lvresize -l +100%FREE "/dev/${vg_name}/${lv_name}" 
            sudo resize2fs "/dev/${vg_name}/${lv_name}"    
        fi               
    done

}


echo 'Expand PVs'
expand_pvs

echo 'Expand LVs And Resize File System'
expand_lvs
