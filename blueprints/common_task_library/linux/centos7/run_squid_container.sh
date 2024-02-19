# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20220831- cita-starter version
# task_name:    RunSquidContainer
# description:  installs squid proxy docker container             
# output vars:  none
# dependencies: Centos7InstallDocker.sh
# endregion

#* pull image (using https://hub.docker.com/r/ubuntu/squid)
sudo docker pull ubuntu/squid

#* create docker volumes
sudo docker volume create squid-logs
sudo docker volume create squid-cache
sudo docker volume create squid-config

#* run container
sudo docker run -d --name squid-container -e TZ=UTC -p 3128:3128 -v squid-logs:/var/log/squid -v squid-cache:/var/spool/squid -v squid-config:/etc/squid --restart=always ubuntu/squid:latest

#* display container logs
sudo docker logs squid-container
