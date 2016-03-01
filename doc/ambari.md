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
yum remove -y hadoop_* zookeeper* ranger* hbase_* ranger* hbase_* ambari-* hadoop_* zookeeper_* hbase* range* pig*  hive* tez* mysql-*
```

###Path
----------------------
```
/usr/lib/hadoop
/usr/lib/hbase
/usr/lib/zookeeper
/usr/lib/hcatalog
/usr/lib/hive

/var/log/hadoop
/var/log/hbase

/etc/hadoop
/etc/hbase
/etc/hive

/hadoop/hdfs
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
