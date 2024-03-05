action='@@{NDB_Service.resource_service}@@'
#echo $action #todo torem
if [[ ${action} == 'CPU' ]]
then
    echo "No change in RAM. Hence no change in innodb_buffer_pool_size"
    exit 0
fi

echo 'Configuring my.conf'

sudo sed -i 's/innodb_buffer_pool_size=[0-9]\+/innodb_buffer_pool_size=@@{NDB_Service.INNODB_POOL_SIZE}@@/' /etc/my.cnf
sudo sed -i 's/innodb_buffer_pool_size=[0-9]\+/innodb_buffer_pool_size=@@{NDB_Service.INNODB_POOL_SIZE}@@/' '@@{NDB_Service.DB_SOFT_DIR}@@/my.cnf'

sudo systemctl stop era_mysql
sudo systemctl start era_mysql

