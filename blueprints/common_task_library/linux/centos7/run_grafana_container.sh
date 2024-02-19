# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20220811
# task_name:    RunGrafanaContainer
# description:  starts grafana container.               
# output vars:  none
# dependencies: Centos7InstallDocker.sh
# endregion

#* create the necessary storage volumes
sudo docker volume create grafana-storage
sudo docker volume create grafana-config
sudo docker volume create grafana-logs

#* pull the docker image
sudo docker pull grafana/grafana-enterprise

#* start the container
sudo docker run -d -p 3000:3000 --name=grafana -v grafana-storage:/var/lib/grafana -v grafana-config:/etc/grafana -v grafana-logs:/var/log/grafana --restart=always grafana/grafana-enterprise