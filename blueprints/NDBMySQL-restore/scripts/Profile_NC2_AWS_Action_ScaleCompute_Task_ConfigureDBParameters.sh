echo 'Configuring my.conf'

sudo sed -i 's/innodb_buffer_pool_size=[0-9]\+/innodb_buffer_pool_size=@@{NDB_Service.INNODB_POOL_SIZE}@@/' /etc/my.cnf
sudo sed -i 's/innodb_buffer_pool_size=[0-9]\+/innodb_buffer_pool_size=@@{NDB_Service.INNODB_POOL_SIZE}@@/' '@@{NDB_Service.DB_SOFT_DIR}@@/my.cnf'

sudo systemctl stop era_mysql
sudo systemctl start era_mysql

