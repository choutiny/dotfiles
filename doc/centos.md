Centos Config
===========

#CentOS 7

###Ulimit -n
----------
cat /proc/sys/fs/file-max  will affect the limits
vim /etc/security/limits.conf, for centos7
add the below content at the end of file then restart server
```
* soft nofile 102400
* hard nofile 102400
```

###Network initial start when reboot
----------
cat /etc/sysconfig/network-scripts/ifcfg-enp2s0
```
ONBOOT="yes"
```

###Close selinux
----------
```
setenforce 0
vim /etc/selinux/config
```

###Close iptables
----------
```
systemctl disable firewalld
service firewalld stop
```

###Createrepo
----------
```
ssh into centos7 server which has fast network speed
yum install yum-utils createrepo yum-plugin-priorities
cd /etc/yum.repos.d/
wget repo_file
    wget http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.2.1.0/ambari.repo
        http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.2.1.0/ambari-2.2.1.0-centos7.tar.gz
    wget http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.4.0.0/hdp.repo
        http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.4.0.0/HDP-2.4.0.0-centos7-rpm.tar.gz
        http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.20/repos/centos7/HDP-UTILS-1.1.0.20-centos7.tar.gz
cd /tmp
mkdir ambari
mkdir hdp
reposync -r repo_soft_name
    reposync -r Updates-ambari-2.2.1.0
    reposync -r HDP-2.4.0.0
    reposync -r HDP-UTILS-1.1.0.20
sync the packages to local repository path
install apache or others web services
    Repository              Base URL 
    Ambari Base URL         http://<web.server>/ambari/<OS>/Updates-ambari-2.2.1.0
    HDP Base URL            http://<web.server>/hdp/<OS>/HDP-<latest.version>
    HDP-UTILS Base URL      http://<web.server>/hdp/<OS>/HDP-UTILS-<version>

createrepo filepath
    createrepo Updates-ambari-2.2.1.0
    createrepo HDP-2.4.0.0
    createrepo HDP-UTILS-1.1.0.20

vim /etc/yum.repos.d/repo.file 
    
    #VERSION_NUMBER=2.2.1.00

    [Updates-ambari-2.2.1.0]
    name=ambari-2.2.1.0 - Updates
    baseurl=http://halo-cnode1.domain.org/ambari_repo_rpms/centos7/Updates-ambari-2.2.1.0
    gpgcheck=0
    gpgkey=http://public-repo-1.hortonworks.com/ambari/centos7/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins
    enabled=1
    priority=1
    make gpgcheck=0


    [HDP-2.4]
    name=HDP-2.4
    baseurl=http://halo-cnode1.domain.org/hdp_repo_rpms/centos7/HDP-2.4.0.0/

    path=/
    enabled=1
    gpgcheck=0


    [HDP-UTILS-1.1.0.20]
    name=HDP-UTILS-1.1.0.20
    baseurl=http://halo-cnode1.domain.org/hdp_repo_rpms/centos7/HDP-UTILS-1.1.0.20/
    #baseurl=http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.20/repos/centos7/

    path=/
    enabled=1
    gpgcheck=0

```
