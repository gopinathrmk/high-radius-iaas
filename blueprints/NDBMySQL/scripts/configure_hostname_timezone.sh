fqdn='@@{DB_VM_FQDN}@@'
tz='@@{DB_VM_TZ}@@'
ip='@@{NDB_Service.DB_SERVER_IP}@@'

sudo hostnamectl set-hostname $fqdn
sudo timedatectl set-timezone $tz

sudo sed -i 's/^@@{NDB_Service.DB_SERVER_IP}@@.*/& @@{DB_VM_FQDN}@@/' /etc/hosts

echo "Hostname and TimeZone Changed"
echo "Rebooting the VM."
sudo shutdown -r 