# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    RemoveGitHubRunner
# description:  given a github repository token, unregister that runner from the repo it is currently registered to.               
# output vars:  none
# dependencies: github_repo_token
# endregion

cd ~/actions-runner
./config.sh remove --token @@{github_repo_token}@@