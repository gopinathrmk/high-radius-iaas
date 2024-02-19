# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    RestartGitHubRunner
# description:  Restarts a GitHub runner daemon.               
# output vars:  none
# dependencies: task: CreateGitHubRunner
# endregion

cd ~/actions-runner
sudo ./svc.sh stop
sudo ./svc.sh start