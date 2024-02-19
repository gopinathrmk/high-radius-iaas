# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    CreateGitHubRunner
# description:  Creates a github runner daemon.               
# output vars:  none
# dependencies: task: ConfigureGitHubRunner
# endregion

cd ~/actions-runner
sudo ./svc.sh install
sudo sed -i 's/ExecStart=/ExecStart=\/bin\/bash /g' /etc/systemd/system/$(cat ~/actions-runner/.service)
sudo systemctl daemon-reload