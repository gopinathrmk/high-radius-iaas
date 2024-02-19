# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20220811
# task_name:    RunPrometheusContainer
# description:  starts prometheus container.               
# output vars:  none
# dependencies: Centos7InstallDocker.sh
# endregion

#* create the necessary storage volume
sudo docker volume create prometheus_data

#* pull the docker image
sudo docker pull prom/prometheus

#* start the container
sudo docker run -d -p 9090:9090 --name=prometheus -v prometheus_data:/etc/prometheus --restart=always prom/prometheus