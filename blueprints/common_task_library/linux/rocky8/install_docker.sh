# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20220708
# task_name:    InstallDocker
# description:  installs and configures docker.               
# output vars:  none
# dependencies: none
# endregion

#updates the server (optional)
sudo dnf update -y

#add the official Docker repository
sudo dnf install -y dnf-utils
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#update the system repos
sudo dnf update -y

#install Docker CE
sudo dnf install -y docker-ce

#verify the version of Docker
sudo docker --version

#start the docker service
sudo systemctl start docker
#enable the docker service at boot
sudo systemctl enable docker
#! the command below requires user for some reason
#sudo systemctl status docker

#adds a user to the docker group
sudo usermod -aG docker @@{linux.username}@@

#tests installation by running a simple container
sudo docker container run hello-world