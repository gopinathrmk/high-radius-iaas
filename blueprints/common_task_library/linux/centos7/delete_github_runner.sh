# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    DeleteGitHubRunner
# description:  Removes a previously create Github runner daemon.               
# output vars:  none
# dependencies: none
# endregion

cd ~/actions-runner
sudo ./svc.sh uninstall