#!/bin/bash
# region headers
# * author:     haikel.zein@nutanix.com
# task_name:    RegisterSatellite
# description:  RegisterSatellite for RHEL 8   
# output vars:  none
# dependencies: none
# endregion

# Register System with vendor expects a YES variable for @@{SatelliteRegister}@@
#
echo "Satellite Registration"
REG="@@{SatelliteRegister}@@"
PATH=$PATH:/bin:/usr/bin
MYDIR=`dirname ${0}`

if [ $REG == "YES" ]
then
  echo "beginning vendor registration"
  sudo subscription-manager register --username @@{SatelliteReg.username}@@ --password @@{SatelliteReg.secret}@@ --auto-attach --force
  # subscription-manager register --username <username> --password <password> --auto-attach
else
  echo "vendor registration not requested"
fi