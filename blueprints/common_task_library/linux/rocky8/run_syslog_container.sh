# region headers
# * author:     stephane.bourdeaud@nutanix.com
# * version:    v1.0/20220708
# task_name:    RunSyslogNgContainer
# description:  starts syslog-ng container.               
# output vars:  none
# dependencies: Rockey8InstallDocker.sh
# endregion

sudo firewall-cmd --zone=public --add-port=601/tcp --permanent
sudo firewall-cmd --zone=public --add-port=514/udp --permanent
sudo firewall-cmd --zone=public --add-port=514/tcp --permanent
sudo firewall-cmd --reload

sudo docker run -it \
  -p 514:514/udp \
  -p 601:601 \
  -v /etc/syslog-ng/syslog-ng.conf:/etc/syslog-ng/syslog-ng.conf \
  -v @@{data_volume_mount_point}@@:/var/log \
  --restart unless-stopped \
  --name syslog-ng \
  balabit/syslog-ng:latest


#/etc/syslog-ng/syslog-ng.conf
@version: 3.37
options {
    chain_hostnames(no);
    create_dirs (yes);
    dir_perm(0755);
    dns_cache(yes);
    keep_hostname(yes);
    log_fifo_size(2048);
    log_msg_size(8192);
    perm(0644);
    time_reopen (10);
    use_dns(yes);
    use_fqdn(yes);
};
source s_network {
    network(
      transport(tcp)
      flags(syslog-protocol)
      port(601)
    );
};
destination d_logs {
    file(“/var/log/$HOST/$YEAR-$MONTH-$DAY-$HOST.log” create_dirs(yes));
};
log {
    source(s_network); destination(d_logs);
};


#crontab -e
0 5 * * * /bin/find @@{data_volume_mount_point}@@ -type f -name \*.log -mtime +7 -exec rm {} \;