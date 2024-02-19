# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20220906
# task_name:    InstallDocker
# description:  installs and configured docker.               
# output vars:  none
# dependencies: Centos7InitializeDataDisk.sh (to create /data mount point)
# endregion

#* adding the repo we need
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

#* installing docker binaries with containerd engine
sudo yum install -y docker-ce docker-ce-cli containerd.io

#* installing iptables firewall
sudo dnf install -y iptables
sudo systemctl enable docker
sudo systemctl start docker

#* making sure permissions are correct for the current user
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock

#* replacing default path for docker volumes (pointing to /data instead) and restarting the docker service to apply that change
sudo sed 's#ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock#ExecStart=/usr/bin/dockerd --data-root /data -H fd:// --containerd=/run/containerd/containerd.sock#' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl restart docker