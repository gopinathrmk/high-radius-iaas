# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    InstallCalmDSL
# description:  installs and configured Nutanix Calm DSL.               
# output vars:  none
# dependencies: none
# endregion

#install pre-reqs
sudo yum groupinstall 'development tools' -y
sudo yum install python3 python3-devel python3-wheel python3-pip make gcc openssl-devel -y
sudo pip3 install virtualenv

cd $home
git clone https://github.com/nutanix/calm-dsl.git
cd calm-dsl
make dev