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
