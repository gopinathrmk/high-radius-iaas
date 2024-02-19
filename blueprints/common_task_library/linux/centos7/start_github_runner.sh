# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    StartGitHubRunner
# description:  Starts a GitHub runner daemon.               
# output vars:  none
# dependencies: task: CreateGitHubRunner
# endregion

cd ~/actions-runner
sudo ./svc.sh start