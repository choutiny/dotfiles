ambari
========
[hortonworks documents](http://hortonworks.com/downloads/#data-platform)
###Install Flow
----------------------
1. Install centos7 on 3 server or more, centos7 ISO in http://192.168.85.133/, https://www.centos.org/download/
2. Fetch IP address and Hostname. named 'node1, node2, node3' etc.
3. `yum install ntpdate`

   `ntpdate pool.ntp.org` to sync time
4. `ssh-keygen` to generate ssh public key.

   `ssh-copy-id -i ~/.ssh/id_rsa.pub root@node1`,node2,node3 to send the public key to others server
5. Configure centos repository
6. Configure centos `ulimit -n`   # `cat /proc/sys/fs/file-max` , `vi /etc/security/limits.conf`  add the
   below content into the file then restart server
    ```
    * soft nofile 102400
    * hard nofile 102400
    ```
   If server can't restart, check centos network initial start when reboot
    ```
    cat /etc/sysconfig/network-scripts/ifcfg-enp2s0
    ONBOOT="yes"
    ```
   Close selinux and iptables
    ```
    vim /etc/selinux/config
    setenforce 0
    systemctl disable firewalld
    service firewalld stop
    ```
7. Create centos repo, see centos.md 
8. Use local centos repository, copy the below content into /etc/yum.repos.d/

    ```
    #ambari.repo
    ================= start ================
    #VERSION_NUMBER=2.2.1.00

    [Updates-ambari-2.2.1.0]
    name=ambari-2.2.1.0 - Updates
    baseurl=http://halo-cnode1.domain.org/ambari_repo_rpms/centos7/Updates-ambari-2.2.1.0
    gpgcheck=0
    gpgkey=http://public-repo-1.hortonworks.com/ambari/centos7/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins
    enabled=1
    priority=1
    =================  end  ================
    #HDP.repo
    ================= start ================
    [HDP-2.4]
    name=HDP-2.4
    baseurl=http://halo-cnode1.domain.org/hdp_repo_rpms/centos7/HDP-2.4.0.0/

    path=/
    enabled=1
    gpgcheck=0
    =================  end  ================
    #HDP-UTILS.repo
    ================= start ================
    [HDP-UTILS-1.1.0.20]
    name=HDP-UTILS-1.1.0.20
    baseurl=http://halo-cnode1.domain.org/hdp_repo_rpms/centos7/HDP-UTILS-1.1.0.20/

    path=/
    enabled=1
    gpgcheck=0
    =================  end  ================
    ```

9. `yum install ambari-server`

    `ambari-server setup`

    `ambari-server start`

    Go to node1.domain.org:8080 to access ambar-server web-UI, default account/password: ``admin/admin``
    Offical Installation Manual [Installation Documents](http://docs.hortonworks.com/HDPDocuments/Ambari/Ambari-2.2.1.1/index.html)


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
yum remove -y hadoop_* zookeeper* ranger* hbase_* ranger* hbase_* ambari-* hadoop_* zookeeper_* hbase* range* pig*  hive* tez* mysql-* bigtop-*  tuned-* ambari-* apache-maven* postgresql*
```

###Reinstall Path
----------------------
```
cd /usr/lib/ 
rm -rf hadoop hbase zookeeper hcatalog hive ambari-* storm ams-hbase flume hadoop-* falcon* slider* pgsql*
cd /var/lib/
rm -rf ambari-* hadoop-* pgsql oozie* hive*  falcon* slider*
cd /var/log/ 
rm -rf hadoop hbase spark tuned ambari-* zookeeper hadoop-* hive* oozie* storm* kafka*  falcon* slider*
find . -type f -size +10k | grep mesos | xargs rm
centos:find ./ -type f | grep -E "[a-z]+-[0-9]+" | xargs rm
echo '' > messages
echo '' > secure
rm -rf audit/audit.log.*
 
cd /etc/ 
rm -rf hadoop hbase hive* ambari-* spark tez tuned zookeeper maven* oozie* storm* ams-* hadoop-* falcon* slider*
rm -rf /hadoop/*
cd /usr/share
rm -rf apache-maven HDP-oozie maven-* falcon*
rm /usr/hdp
cd /usr/bin
rm -rf mvnyjp
ls -la | grep hdp | awk '{ print $9 }' | xargs rm
cd /home
rm -rf oozie mapred zookeeper storm yarn hive spark tez kafka hcat hdfs hbase ams ambari-* knox
cd /var/spool/mail
rm -rf ambari-* ams hadoop hbase hcat hdfs hive kafka knox mapred oozie  slider spark storm tez yarn zookeeper
cd /
rm -rf kafka-logs hadoop
cd /tmp
rm -rf hadoop* hsperfdata* Jetty* hbase* ambari* jetty* MIME* ehcache* oozie* hive 
 
cd /usr/lib/python2.6/site-packages
rm -rf ambari* resource_*
ps aux | grep ambari | awk '{ print NR=$2 }' | xargs kill -9
 
vim /etc/passwd
vim /etc/group
ln -s /home/hdfs/data /hadoop/hdfs/data
ln -s /home/hdfs/namenode /hadoop/hdfs/namenode
ln -s /home/hdfs/namesecondary /hadoop/hdfs/namesecondary
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

resource_management.core.exceptions.Fail: Execution of 'cp /usr/share/HDP-oozie/ext-2.2.zip /usr/hdp/current/oozie-server/libext' returned 1. cp: cannot stat '/usr/share/HDP-oozie/ext-2.2.zip': No such file or directory

mkdir /usr/share/HDP-oozie
wget http://web_url/ext-2.2.zip -O /usr/share/HDP-oozie/ext-2.2.zip  #6.5MB
chown oozie:hadoop /usr/share/HDP-oozie/ext-2.2.zip
cp /usr/share/HDP-oozie/ext-2.2.zip /usr/hdp/current/oozie-server/libext/

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
curl -X PUT -d '{"Datacenter": "dc1", "Node": "halo-cnode1.domain.org", "Address": "192.168.85.109", "Service": {"Service": "halo-cnode1.domain.org"}}' http://172.17.0.2:8500/v1/catalog/register
curl -X PUT -d '{"Datacenter": "dc1", "Node": "kdctommy.domain.org", "Address": "192.168.85.83", "Service": {"Service": "kdctommy.domain.org"}}' http://172.17.0.2:8500/v1/catalog/register

3. http://172.17.0.3:8080
 
4. change the repository to internal centos7 repository
http://halo-cnode1.domain.org/hdp_repo_rpms/centos7/HDP-UTILS-1.1.0.20/
http://halo-cnode1.domain.org/hdp_repo_rpms/centos7/HDP-2.4.0.0/

5. docker ps   #get all current online ambari container
NAMES: amb2   amb1  amb3 amb-server amb-consul

6. input 
amb1.service.consul
amb2.service.consul
amb3.service.consul

7. Perform manual registration on hosts and do not use SSH

```


