# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    ConfigureGitHubRunner
# description:  given a Github repository and token, register this runner in that repo.             
# output vars:  none
# dependencies: task: DownloadGitHubRunner, macros: github_repo, github_repo_token, github_label
# endregion

# Create the runner and start the configuration experience
cd ~/actions-runner
sudo ./bin/installdependencies.sh
./config.sh --url @@{github_repo}@@ --token @@{github_repo_token}@@ --unattended --labels @@{github_label}@@