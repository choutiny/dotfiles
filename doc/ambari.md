ambari
========

###Command
----------------------
```
ambari-server reset
ambari-server start
ambari-server stop
```

###Remove
----------------------
```
yum remove -y hadoop_* zookeeper* ranger* hbase_* ranger* hbase_* ambari-* hadoop_* zookeeper_* hbase* range* pig*  hive* tez* mysql-* bigtop-*  tuned-* ambari-* apache-maven*
postgresql*
```

###Reinstall Path
----------------------
```
cd /usr/lib/ 
rm -rf hadoop hbase zookeeper hcatalog hive ambari-* storm ams-hbase flume hadoop-*

cd /var/lib/
rm -rf ambari-* hadoop-* pgsql

cd /var/log/ 
rm -rf hadoop hbase spark tuned ambari-* zookeeper hadoop-* hive*

cd /etc/ 
rm -rf hadoop hbase hive* ambari-* spark tez tuned zookeeper maven

rm -rf /hadoop/hdfs

cd /usr/share
rm -rf apache-maven

rm /usr/hdp

cd /usr/bin
rm -rf mvnyjp
ls -la | grep hdp | awk '{ print $9 }' | xargs rm

cd /home

vim /etc/passwd
vim /etc/group

ln -s /home/hdfs/data /hadoop/hdfs/data
ln -s /home/hdfs/namenode /hadoop/hdfs/namenode
chown hdfs:hadoop data -R
chown hdfs:hadoop namenode -R

yum clean metadata
yum repolist
yum -y intall ambari-server

ambari-server setup
ambari-server start
```

###Security
----------------------
```
Install JCE
http://www.oracle.com/technetwork/cn/java/javase/downloads/jce-7-download-432124.html
ps aux | grep java
find java path
cd java_path/jre/lib

kerberos

ambari client:
yum install -y krb5-libs krb5-workstation pam_krb5

KDC:
    KDC host:kdctommy.domain.org
    Realm name: DOMAIN.ORG
    Domains: .DOMAIN.org,DOMAIN.org
Kadmin:
    Kadmin host:kdctommy.domain.org
    Admin principal:root/admin
    Admin password:domain
```

###Failed
----------------------
```
for storm,hive
mkdir -p /usr/hdp/2.4.0.0-169/storm/extlib-daemon
```

###Install
----------------------
```
Install Options:
halo-cnode1
halo-cnode2
halo-cnode3

systemctl enable ntpd
systemctl start ntpd
```

###Install from docker
----------------------
```
git clone https://github.com/sequenceiq/docker-ambari.git
switch to root
source ambari-function
amb-start-cluster 4
amb-settings
docker run -d --privileged --name amb2 -h amb2.service.consul hortonworks/ambari-agent:latest systemd.setenv=NAMESERVER_ADDR=172.17.0.2

1. run consul docker
run ambari-server docker
run ambari-agent docker


2. use consul to register external IP and domain
docker inspect consul_container_id # get consul ip
Consul
curl -X PUT -d '{"Datacenter": "dc1", "Node": "halo-cnode1", "Address": "192.168.85.109", "Service": {"Service": "halo-cnode1"}}' http://172.17.0.2:8500/v1/catalog/register
curl -X PUT -d '{"Datacenter": "dc1", "Node": "kdctommy", "Address": "192.168.85.83", "Service": {"Service": "kdctommy"}}' http://172.17.0.2:8500/v1/catalog/register
curl -X PUT -d '{"Datacenter": "dc1", "Node": "halo-cnode1.synnex.org", "Address": "192.168.85.109", "Service": {"Service": "halo-cnode1.synnex.org"}}' http://172.17.0.2:8500/v1/catalog/register
curl -X PUT -d '{"Datacenter": "dc1", "Node": "kdctommy.synnex.org", "Address": "192.168.85.83", "Service": {"Service": "kdctommy.synnex.org"}}' http://172.17.0.2:8500/v1/catalog/register

3. http://172.17.0.3:8080
 
4. change the repository to internal centos7 repository
http://halo-cnode1.synnex.org/hdp_repo_rpms/centos7/HDP-UTILS-1.1.0.20/
http://halo-cnode1.synnex.org/hdp_repo_rpms/centos7/HDP-2.4.0.0/

5. docker ps   #get all current online ambari container
NAMES: amb2   amb1  amb3 amb-server amb-consul

6. input 
amb1.service.consul
amb2.service.consul
amb3.service.consul

7. Perform manual registration on hosts and do not use SSH

```


