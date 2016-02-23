Kerberos
===========

###Terminology(术语)
------------------------
```
| Term                                 |  Description                     |
| ------------------------------------ |:--------------------------------:|
| Key Distribution Center, or KDC      | 一个可信的启用了Kerberos认证的源 |
| Kerberos KDC Server                  | 密钥分发中心的机器或者服务器     |
| Kerberos Client                      | KDC集群中的任何一台被授权的机器  |
| Principal                            | 该认证对KDC用户或者服务的唯一名称|
| Keytab                               | 包含一个或者多个主体和密钥的文件 |
| Realm                                | Kerberos网络,包含KDC和客户端     |
| KDC Admin Account                    | 通过Ambari管理员创建并产生keytabs|

Server: kdctommy.example.org
Client：kdcc.example.org
```

###Install
------------------------
```
RHEL/CentOS/Oracle Linux
yum install krb5-server krb5-libs krb5-workstation

Ubuntu/Debian
apt-get install krb5-kdc krb5-admin-server
```

###Configuration
------------------------
```
vim /etc/krb5.conf


libdefault:     包含Kerberos V5库的默认值
appdefaults:    包含Kerberos V5应用程序使用的默认值
Realm:          包含Kerberos领域名称键入小节. 每个小节描述域特定的信息, 包括在哪里可以找到该realm中的Kerberos的服务器. 
domain_realm:   包含关系, 这种关系映射域名和子域到Kerberos领域的名称. 这是由程序用来确定主机应该是什么样的境界中, 赋予其完全合格的域名. 
logging:        包含了确定Kerberos的程序如何进行日志记录的关系. 
capaths:        包含直接（不分等级）跨领域(cross-realm)验证使用的验证路径. 在本节中的条目由客户端使用, 以确定哪些可以跨领域验证中使用的中间领域. 检查转换字段信任中间领域时, 也使用终端服务. 
KDC:            密钥分发中心,含有kdc.conf文件的位置. 
Principal:      primary/instance@REALM  
                    primary在一个用户的时候,是用户名, 在一个服务的时候是服务名;
                    instance是给有资格的主要信息. 实例可以为null. 在一个用户的情况下, 该实例被经常用于描述的目的用途相应的凭据. 在一台主机的情况下, 实例是完全合格的主机名 
                    REALM由单个Kerberos数据库以及一组密钥分发中心的服务的逻辑网络. 按照惯例, realm名称一般都是全部大写, 以区别于互联网领域的境界

```

```
rm -rf /var/Kerberos/krb5kdc/principal*
kdb5_util create -s -r EXAMPLE.ORG 
    -s表示通过 kadmin 登录本机不需要密码
    Loading random data 的时间会有点长, 之后会让设置一个密码

登录 KDC, 添加管理员和一般用户的 principal. 
首先创建一个有管理权限的 principal：
# kadmin.local
Authenticating as principal root/admin@EXAMPLE.ORG with password.

kadmin.local:  addprinc root/admin
Authenticating as principal root/admin@EXAMPLE.ORG with password.
WARNING: no policy specified for root/admin@EXAMPLE.ORG; defaulting to no policy
Enter password for principal "root/admin@EXAMPLE.ORG": root
Re-enter password for principal "root/admin@EXAMPLE.ORG": root
Principal "root/admin@EXAMPLE.ORG" created.
创建一个普通的 principal：

kadmin.local:  addprinc tommy
Enter password for principal "tommy@EXAMPLE.ORG": yourpassword
Re-enter password for principal "tommy@EXAMPLE.ORG": yourpassword
Principal "tommy@EXAMPLE.ORG" created.

kadmin 和 kadmin.local 都是 KDC 的管理接口, 区别在于 kadmin.local 只能在 Server 上使用,无需密码; kadmin 在 Server 和 Client 上都能使用, 需要密码——当然, 需要在 Server 上启动 Kadmin 服务.

将 KDC 的域名加入到 Kerberos 的数据库
kadmin.local:  addprinc -randkey host/kdctommy.example.org
Authenticating as principal root/admin@EXAMPLE.ORG with password.
WARNING: no policy specified for host/kdctommy.example.org@EXAMPLE.ORG; defaulting to no policy
Principal "host/kdctommy.example.org@EXAMPLE.ORG" created.

导出 kadmin 服务的 keytab 文件：
kadmin.local:  ktadd host/kdctommy.example.org
Entry for principal host/kdctommy.example.org with kvno 2, encryption type aes256-cts-hmac-sha1-96
added to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy.example.org with kvno 2, encryption type aes128-cts-hmac-sha1-96
added to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy.example.org with kvno 2, encryption type des3-cbc-sha1 added to
keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy.example.org with kvno 2, encryption type arcfour-hmac added to
keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy.example.org with kvno 2, encryption type camellia256-cts-cmac added
to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy.example.org with kvno 2, encryption type camellia128-cts-cmac added
to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy.example.org with kvno 2, encryption type des-hmac-sha1 added to
keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy.example.org with kvno 2, encryption type des-cbc-md5 added to
keytab FILE:/etc/krb5.keytab.
kadmin.local:  quit
[root@kdctommy krb5kdc/<Right># klist -k
Keytab name: FILE:/etc/krb5.keytab
KVNO Principal
---- --------------------------------------------------------------------------
   2 host/kdctommy.example.org@EXAMPLE.ORG
   2 host/kdctommy.example.org@EXAMPLE.ORG
   2 host/kdctommy.example.org@EXAMPLE.ORG
   2 host/kdctommy.example.org@EXAMPLE.ORG
   2 host/kdctommy.example.org@EXAMPLE.ORG
   2 host/kdctommy.example.org@EXAMPLE.ORG
   2 host/kdctommy.example.org@EXAMPLE.ORG
   2 host/kdctommy.example.org@EXAMPLE.ORG
[root@kdctommy krb5kdc#]]
```
