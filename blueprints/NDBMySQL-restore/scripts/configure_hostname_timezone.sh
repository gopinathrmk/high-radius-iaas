vm_name='@@{calm_application_name}@@'
domain_name='@@{domain_name}@@'
fqdn=${vm_name}.${domain_name}

tz='@@{DB_VM_TZ}@@'
ip='@@{NDB_Service.DB_SERVER_IP}@@'

sudo hostnamectl set-hostname $fqdn
sudo timedatectl set-timezone $tz

sudo sed -i "s/^@@{NDB_Service.DB_SERVER_IP}@@.*/& $fqdn/" /etc/hosts

echo "Hostname and TimeZone Changed"
echo "Rebooting the VM."
sudo shutdown -r 