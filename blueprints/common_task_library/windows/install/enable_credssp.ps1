# region headers
# * author:     haikel.zein@nutanix.com
# task_name:    EnableCredSSP
# description:  Enable CRED SSP              
# output vars:  none
# dependencies: none
# endregion


Write-Output "Enabling CredSSP"

#Enable credssp for double-hop issues
Enable-WSManCredSSP -Role Server -Force