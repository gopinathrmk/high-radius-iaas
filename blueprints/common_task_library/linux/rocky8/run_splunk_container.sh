# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20220708
# task_name:    RunSplunkContainer
# description:  installs and configures docker.               
# output vars:  none
# dependencies: Rockey8InstallDocker.sh
# endregion

#pull image from dockerhub
sudo docker pull splunk/splunk:latest

#start container, setting the admin user password
sudo docker run -d -p 8000:8000 -p 9997:9997 -e SPLUNK_START_ARGS='--accept-license' -e SPLUNK_PASSWORD='@@{splunk.secret}@@' --name splunk splunk/splunk:latest
#open firewall port
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
sudo firewall-cmd --zone=public --add-port=9997/tcp --permanent
sudo firewall-cmd --reload