# region headers
# * author:     haikel.zein@nutanix.com
# task_name:    GetMAC
# description:  Retrieve MAC address from Windows                
# output vars:  vm_mac
# dependencies: none
# endregion


$nic = Get-NetAdapter
$vm_mac = $nic.MacAddress
Write-Output "vm_mac=$vm_mac"