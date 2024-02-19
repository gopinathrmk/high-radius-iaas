# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    DownloadGitHubRunner
# description:  downloads and extracts binaries for GitHub runner.               
# output vars:  none
# dependencies: none
# endregion

# Create a folder
mkdir ~/actions-runner && cd ~/actions-runner
# Download the latest runner package
curl -O -L https://github.com/actions/runner/releases/download/v2.277.1/actions-runner-linux-x64-2.277.1.tar.gz
# Extract the installer
tar xzf ./actions-runner-linux-x64-2.277.1.tar.gz