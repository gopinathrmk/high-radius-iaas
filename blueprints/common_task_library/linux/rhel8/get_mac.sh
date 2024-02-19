# region headers
# * author:     haikel.zein@nutanix.com
# task_name:    GetMACRHEL
# description:  Retrieve MAC address from RHEL 8                
# output vars:  none
# dependencies: none
# endregion


MACVM=$(sudo cat /sys/class/net/ens192/address)

echo "mac=$MACVM