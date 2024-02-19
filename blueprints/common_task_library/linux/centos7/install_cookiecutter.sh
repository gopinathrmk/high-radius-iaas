# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20210630
# task_name:    InstallCookiecutter
# description:  Installs Cookiecutter python module.               
# output vars:  none
# dependencies: none
# endregion

sudo python3 -m pip install --upgrade pip setuptools wheel
pip install --user cookiecutter
export PATH=~/.local/bin:$PATH
cookiecutter --version