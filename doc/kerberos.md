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
yum install -y krb5-libs krb5-server krb5-workstation pam_krb5

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


ealm: 认证管理域。一个realm对应着KDC的一个database，一个Client在未提前配置的情况下只能访问跟其在一个realm的服务。
principal:KDC database中每一条记录就是一个principal。一个用户或者一个服务，只要其在KDC进行了注册，在database中就会有一条相应的记录，这条记录就是其对应的principal
    格式：Name[/Instance]@REALM
    对于用户来说，以zj为例，其对应principal可以是zj/nodeA@US，也可以是zj@US，US为realm名，一般大写。对于服务来说，以ES为例，其对应principal可以为email/nodeB@US，一般不省略nodeB，因为一个服务可能分布在多个节点上，以hostname作为Instance可作区分。 
.keytab文件: 一个用户，作为人，可以记住自己的密码，在认证时输入即可；但是一个服务是无法做这种交互的，那么就提供一个.keytab文件，记录服务principal的信息（包括加密的密码），在登录KDC时就提供该文件。
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

修改/etc/ssh/ssh_config
GSSAPIAuthentication yes
GSSAPIDelegateCredentials yes
GSSAPITrustDNS yes
重启 sshd
systemctl reload sshd
配置 PAM
authconfig-tui
选择 [*] Use Kerberos 并选择 Next, 确定 Realm、KDC 和 Admin Server 是否正确, 并选择 [*] Use DNS to resolve hosts to realms、[*] Use DNS to locate KDCs for realms, 选择 OK 保存.
authconfig --enablekrb5 --update


配置 firewall（如果开启了的话）
创建 /etc/firewalld/services/kerberos.xml 文件并写入:
<?xml version="1.0" encoding="utf-8"?>
<service>
  <short>Kerberos</short>
  <description>Kerberos network authentication protocol server</description>
  <port protocol="tcp" port="88"/>
  <port protocol="udp" port="88"/>
  <port protocol="tcp" port="749"/>
</service>
向 firewall 中添加 service
firewall-cmd --permanent --add-service=kerberos
重新加载 firewall 配置
firewall-cmd --reload

向 /root/.k5login 添加 principal
tommyx@EXAMPLE.ORG

配置 Kerberos Client
安装相关模块
yum install -y krb5-libs krb5-workstation pam_krb5
配置文件
将 Server 上的 /etc/krb5.conf 直接 copy 过来即可
向 Kerberos 数据库中添加 Client 的域名

kdestroy
kadmin
Authenticating as principal root/admin@EXAMPLE.ORG with password.
Password for root/admin@EXAMPLE.ORG: 
kadmin:  addp
addpol    addprinc  
kadmin:  addp
addpol    addprinc  
kadmin:  addp
addpol    addprinc  
kadmin:  addprinc -randkey host/kdctommy2.example.org
WARNING: no policy specified for host/kdctommy2.example.org@EXAMPLE.ORG; defaulting to no policy
Principal "host/kdctommy2.example.org@EXAMPLE.ORG" created.
kadmin:  ktadd host/kdctommy2.example.org
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type aes256-cts-hmac-sha1-96
added to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type aes128-cts-hmac-sha1-96
added to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type des3-cbc-sha1 added to
keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type arcfour-hmac added to
keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type camellia256-cts-cmac
added to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type camellia128-cts-cmac
added to keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type des-hmac-sha1 added to
keytab FILE:/etc/krb5.keytab.
Entry for principal host/kdctommy2.example.org with kvno 2, encryption type des-cbc-md5 added to
keytab FILE:/etc/krb5.keytab.
kadmin:  
""

Test
klist -k
kinit tommyx
Password for tommyx@DOMAIN.ORG
klist
Ticket cache: FILE:/tmp/krb5cc_0
Default Principal: tommyx@DOMAIN.ORG
ssh kdctommy@DOMAIN.ORG
```



