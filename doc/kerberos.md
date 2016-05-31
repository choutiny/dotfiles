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
Client:kdcc.example.org
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
capaths:        包含直接(不分等级)跨领域(cross-realm)验证使用的验证路径. 在本节中的条目由客户端使用, 以确定哪些可以跨领域验证中使用的中间领域. 检查转换字段信任中间领域时, 也使用终端服务. 
KDC:            密钥分发中心,含有kdc.conf文件的位置. 
Principal:      primary/instance@REALM  
                    primary在一个用户的时候,是用户名, 在一个服务的时候是服务名;
                    instance是给有资格的主要信息. 实例可以为null. 在一个用户的情况下, 该实例被经常用于描述的目的用途相应的凭据. 在一台主机的情况下, 实例是完全合格的主机名 
                    REALM由单个Kerberos数据库以及一组密钥分发中心的服务的逻辑网络. 按照惯例, realm名称一般都是全部大写, 以区别于互联网领域的境界


ealm: 认证管理域.一个realm对应着KDC的一个database,一个Client在未提前配置的情况下只能访问跟其在一个realm的服务.
principal:KDC database中每一条记录就是一个principal.一个用户或者一个服务,只要其在KDC进行了注册,在database中就会有一条相应的记录,这条记录就是其对应的principal
    格式:Name[/Instance]@REALM
    对于用户来说,以zj为例,其对应principal可以是zj/nodeA@US,也可以是zj@US,US为realm名,一般大写.对于服务来说,以ES为例,其对应principal可以为email/nodeB@US,一般不省略nodeB,因为一个服务可能分布在多个节点上,以hostname作为Instance可作区分. 
.keytab文件: 一个用户,作为人,可以记住自己的密码,在认证时输入即可;但是一个服务是无法做这种交互的,那么就提供一个.keytab文件,记录服务principal的信息(包括加密的密码),在登录KDC时就提供该文件.
```

```
rm -rf /var/Kerberos/krb5kdc/principal*
kdb5_util create -s -r EXAMPLE.ORG 
    -s表示通过 kadmin 登录本机不需要密码
    Loading random data 的时间会有点长, 之后会让设置一个密码

登录 KDC, 添加管理员和一般用户的 principal. 
首先创建一个有管理权限的 principal:
# kadmin.local
Authenticating as principal root/admin@EXAMPLE.ORG with password.

kadmin.local:  addprinc root/admin
Authenticating as principal root/admin@EXAMPLE.ORG with password.
WARNING: no policy specified for root/admin@EXAMPLE.ORG; defaulting to no policy
Enter password for principal "root/admin@EXAMPLE.ORG": root
Re-enter password for principal "root/admin@EXAMPLE.ORG": root
Principal "root/admin@EXAMPLE.ORG" created.
创建一个普通的 principal:

kadmin.local:  addprinc tommy
Enter password for principal "tommy@EXAMPLE.ORG": yourpassword
Re-enter password for principal "tommy@EXAMPLE.ORG": yourpassword
Principal "tommy@EXAMPLE.ORG" created.

kadmin.local:  addprinc -randkey host/cdkdc.domain.org                                                                │~                                                                                                                     
WARNING: no policy specified for host/cdkdc.domain.org@DOMAIN.ORG; defaulting to no policy                            │~                                                                                                                     
add_principal: Principal or policy already exists while creating "host/cdkdc.domain.org@DOMAIN.ORG".                  │~                                                                                                                     
kadmin.local:  ktadd host/cdkdc.domain.org     


kadmin 和 kadmin.local 都是 KDC 的管理接口, 区别在于 kadmin.local 只能在 Server 上使用,无需密码; kadmin 在 Server 和 Client 上都能使用, 需要密码——当然, 需要在 Server 上启动 Kadmin 服务.

将 KDC 的域名加入到 Kerberos 的数据库
kadmin.local:  addprinc -randkey host/kdctommy.example.org
Authenticating as principal root/admin@EXAMPLE.ORG with password.
WARNING: no policy specified for host/kdctommy.example.org@EXAMPLE.ORG; defaulting to no policy
Principal "host/kdctommy.example.org@EXAMPLE.ORG" created.

导出 kadmin 服务的 keytab 文件:
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
选择 [*] Use Kerberos 并选择 Next, 确定 Realm,KDC 和 Admin Server 是否正确, 并选择 [*] Use DNS to resolve hosts to realms,[*] Use DNS to locate KDCs for realms, 选择 OK 保存.
authconfig --enablekrb5 --update


配置 firewall(如果开启了的话)
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
apt-get install krb5-user libpam-krb5
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


Client
kinit root/admin
kadmin -q "addprinc flume/halo-cnode3.domain.org@SYNNEX.ORG"

创建keytab文件
keytab 是包含 principals 和加密 principal key 的文件.
keytab 文件对于每个 host 是唯一的,因为 key 中包含 hostname.keytab 文件用于不需要人工交互和保存纯文本密码,实现到 kerberos 上验证一个主机上的 principal.
因为服务器上可以访问 keytab 文件即可以以 principal 的身份通过 kerberos 的认证,所以,keytab 文件应该被妥善保存,应该只有少数的用户可以访问

创建包含 hdfs principal 和 host principal 的 hdfs keytab:
xst -norandkey -k hdfs.keytab hdfs/fully.qualified.domain.name host/fully.qualified.domain.name

创建包含 mapred principal 和 host principal 的 mapred keytab:
xst -norandkey -k mapred.keytab mapred/fully.qualified.domain.name host/fully.qualified.domain.name
```

###Ambari-server
------------------------
refer to ambari.md

###Kerberos command
------------------------
kadmin: ?
```
Available kadmin requests:

add_principal, addprinc, ank
                         Add principal
delete_principal, delprinc
                         Delete principal
modify_principal, modprinc
                         Modify principal
rename_principal, renprinc
                         Rename principal
change_password, cpw     Change password
get_principal, getprinc  Get principal
list_principals, listprincs, get_principals, getprincs
                         List principals
add_policy, addpol       Add policy
modify_policy, modpol    Modify policy
delete_policy, delpol    Delete policy
get_policy, getpol       Get policy
list_policies, listpols, get_policies, getpols
                         List policies
get_privs, getprivs      Get privileges
ktadd, xst               Add entry(s) to a keytab
ktremove, ktrem          Remove entry(s) from a keytab
lock                     Lock database exclusively (use with extreme caution!)
unlock                   Release exclusive database lock
purgekeys                Purge previously retained old keys from a principal
get_strings, getstrs     Show string attributes on a principal
set_string, setstr       Set a string attribute on a principal
del_string, delstr       Delete a string attribute on a principal
list_requests, lr, ?     List available requests.
quit, exit, q            Exit program.
```

###Kerberos configuration
------------------------
server 
1. /var/kerberos/krb5kdc/kadm5.acl
```
*/admin@DOMAIN.ORG    *
```

2. /var/Kerberos/krb5kdc/kdc.conf
```
[kdcdefaults]
 kdc_ports = 88
 kdc_tcp_ports = 88

[realms]
 DOMAIN.ORG  = {
  #master_key_type = aes256-cts
  acl_file = /var/kerberos/krb5kdc/kadm5.acl
  dict_file = /usr/share/dict/words
  admin_keytab = /var/kerberos/krb5kdc/kadm5.keytab
  supported_enctypes = aes256-cts:normal aes128-cts:normal des3-hmac-sha1:normal arcfour-hmac:normal camellia256-cts:normal camellia128-cts:normal des-hmac-sha1:normal des-cbc-md5:normal des-cbc-crc:normal
 }
```

3. restart krb5kdc, kadmin
```
systemctl restart krb5kdc
systemctl restart kadmin
```

client
```
yum install -y pam_krb5
systemctl restart krb5kdc
systemctl restart kadmin

```

###QA
------------------------
```
kadmin:  addprinc -randkey host/cdkdc.domain.org
WARNING: no policy specified for host/cdkdc.domain.org@DOMAIN.ORG; defaulting to no policy
add_principal: Operation requires ``add'' privilege while creating "host/cdkdc.domain.org@DOMAIN.ORG".

make sure kdc.conf exists in /var/kerberos/krb5kdc

```

###Command
------------------------
kinit 用户名 获得或更新 Kerberos 票据授权票据.
klist 显示 Kerberos 凭证高速缓存或密钥表的内容.
kdestroy 破坏 Kerberos 凭证高速缓存.
help kerberos

另外kinit获取的ticket是有时间限制的.在我们的KDC配置中是10小时.快要过期之前可以kinit -R刷新下,就会又有10小时的有效期.最长可以延长到7天.
但超过7天,或者快到10小时没能及时kinit -R,ticket会过期,就必须要重新获取了.
kinit -R是否有效似乎取决于服务端的配置,有些ticket是不能renew的,我不是很熟.
可以用klist命令查看当前ticket的剩余时间,renew的期限.


这里指的只是客户端.比如我们在提交job时,如何通过kerberos认证?

两种方式:

在命令行中用kinit命令.比如kinit -kt xxx.keytab yyy/zzz.kinit成功后,就可以像平常一样用hadoop jar提交job了.job的代码不用做任何改变.原理:kinit获取ticket后会缓存在一个临时文件中.java可以读取这个文件并获取kerberos认证相关信息.前提是替换过JCE相关jar.
用java代码获取ticket.hadoop提供了一个类UserGroupInformation,可以用以下代码获取ticket:

// 如果core-site.xml在classpath里,会自动加载,就不用手动设置属性了
Configuration conf = new Configuration();
// 只是举个例子,kerberos认证的时候只有下面两个属性是必须的
conf.setBoolean("hadoop.security.authorization", true);
conf.set("hadoop.security.authentication", "kerberos");
UserGroupInformation.setConfiguration(conf);
// 如果认证成功会有日志输出
UserGroupInformation.loginUserFromKeytab("yyy/zzz","E:/Documents/TEMP/xxx.keytab");
// 接下来就可以做其他操作了,比如操作FileSystem,提交job等
方法1不用改代码,但是如果一个linux用户要用不同的keytab进行认证,会互相冲突.原因在于默认情况下,对同一个linux用户而言,ticket文件的缓存和kerberos的配置文件都只能有一个.可以通过一些环境变量来设置.
方法2要改些代码,但比较灵活.loginUserFromKeytab一次之后,同一个JVM内所有线程都可以用.不同JVM之间不会互相影响.而且UserGroupInformation提供了其他一些方便的方法,比如ticket快要过期时自动更新,代理执行等等.具体去看javadoc吧.

我现在更喜欢用方法2.

方法2要注意代码执行的顺序.loginUserFromKeytab方法必须在其他代码(访问hdfs,提交job之类)之前执行.


###Kerberos Keytab
------------------------
```
创建keytab文件
keytab 是包含 principals 和加密 principal key 的文件.
keytab 文件对于每个 host 是唯一的,因为 key 中包含 hostname.keytab 文件用于不需要人工交互和保存纯文本密码,实现到 kerberos 上验证一个主机上的 principal.
因为服务器上可以访问 keytab 文件即可以以 principal 的身份通过 kerberos 的认证,所以,keytab 文件应该被妥善保存,应该只有少数的用户可以访问

创建包含 hdfs principal 和 host principal 的 hdfs keytab:
xst -norandkey -k hdfs.keytab hdfs/fully.qualified.domain.name host/fully.qualified.domain.name

创建包含 mapred principal 和 host principal 的 mapred keytab:
xst -norandkey -k mapred.keytab mapred/fully.qualified.domain.name host/fully.qualified.domain.name

注意:
上面的方法使用了xst的norandkey参数,有些kerberos不支持该参数.
当不支持该参数时有这样的提示:Principal -norandkey does not exist.,需要使用下面的方法来生成keytab文件.
在 KDC server 节点上执行下面命令(cdkdc.domain.org):

$ cd /var/kerberos/krb5kdc/

$ kadmin.local -q "xst  -k hdfs-unmerged.keytab  hdfs/cdh1@DOMAIN.ORG"
$ kadmin.local -q "xst  -k hdfs-unmerged.keytab  hdfs/cdh2@DOMAIN.ORG"
$ kadmin.local -q "xst  -k hdfs-unmerged.keytab  hdfs/cdh3@DOMAIN.ORG"

$ kadmin.local -q "xst  -k HTTP.keytab  HTTP/cdh1@DOMAIN.ORG"
$ kadmin.local -q "xst  -k HTTP.keytab  HTTP/cdh2@DOMAIN.ORG"
$ kadmin.local -q "xst  -k HTTP.keytab  HTTP/cdh3@DOMAIN.ORG"
这样,就会在 /var/kerberos/krb5kdc/ 目录下生成 hdfs-unmerged.keytab 和 HTTP.keytab 两个文件,接下来使用 ktutil 合并者两个文件为 hdfs.keytab.

$ cd /var/kerberos/krb5kdc/

$ ktutil
ktutil: rkt hdfs-unmerged.keytab
ktutil: rkt HTTP.keytab
ktutil: wkt hdfs.keytab
使用 klist 显示 hdfs.keytab 文件列表, (合并的作用是让多个keytab存在一个keytab文件中)

$ klist -ket  hdfs.keytab
Keytab name: FILE:hdfs.keytab
KVNO Timestamp         Principal
---- ----------------- --------------------------------------------------------
   2 11/13/14 10:40:18 hdfs/cdh1@DOMAIN.ORG (des3-cbc-sha1)
   2 11/13/14 10:40:18 hdfs/cdh1@DOMAIN.ORG (arcfour-hmac)
   2 11/13/14 10:40:18 hdfs/cdh1@DOMAIN.ORG (des-hmac-sha1)
   2 11/13/14 10:40:18 hdfs/cdh1@DOMAIN.ORG (des-cbc-md5)
   4 11/13/14 10:40:18 hdfs/cdh2@DOMAIN.ORG (des3-cbc-sha1)
   4 11/13/14 10:40:18 hdfs/cdh2@DOMAIN.ORG (arcfour-hmac)
   4 11/13/14 10:40:18 hdfs/cdh2@DOMAIN.ORG (des-hmac-sha1)
   4 11/13/14 10:40:18 hdfs/cdh2@DOMAIN.ORG (des-cbc-md5)
   4 11/13/14 10:40:18 hdfs/cdh3@DOMAIN.ORG (des3-cbc-sha1)
   4 11/13/14 10:40:18 hdfs/cdh3@DOMAIN.ORG (arcfour-hmac)
   4 11/13/14 10:40:18 hdfs/cdh3@DOMAIN.ORG (des-hmac-sha1)
   4 11/13/14 10:40:18 hdfs/cdh3@DOMAIN.ORG (des-cbc-md5)
   3 11/13/14 10:40:18 HTTP/cdh1@DOMAIN.ORG (des3-cbc-sha1)
   3 11/13/14 10:40:18 HTTP/cdh1@DOMAIN.ORG (arcfour-hmac)
   3 11/13/14 10:40:18 HTTP/cdh1@DOMAIN.ORG (des-hmac-sha1)
   3 11/13/14 10:40:18 HTTP/cdh1@DOMAIN.ORG (des-cbc-md5)
   3 11/13/14 10:40:18 HTTP/cdh2@DOMAIN.ORG (des3-cbc-sha1)
   3 11/13/14 10:40:18 HTTP/cdh2@DOMAIN.ORG (arcfour-hmac)
   3 11/13/14 10:40:18 HTTP/cdh2@DOMAIN.ORG (des-hmac-sha1)
   3 11/13/14 10:40:18 HTTP/cdh2@DOMAIN.ORG (des-cbc-md5)
   3 11/13/14 10:40:18 HTTP/cdh3@DOMAIN.ORG (des3-cbc-sha1)
   3 11/13/14 10:40:18 HTTP/cdh3@DOMAIN.ORG (arcfour-hmac)
   3 11/13/14 10:40:18 HTTP/cdh3@DOMAIN.ORG (des-hmac-sha1)
   3 11/13/14 10:40:18 HTTP/cdh3@DOMAIN.ORG (des-cbc-md5)
验证是否正确合并了key,使用合并后的keytab,分别使用hdfs和host principals来获取证书.

$ kinit -k -t hdfs.keytab hdfs/cdh1@DOMAIN.ORG
$ kinit -k -t hdfs.keytab HTTP/cdh1@DOMAIN.ORG
如果出现错误:kinit: Key table entry not found while getting initial credentials,
则上面的合并有问题,重新执行前面的操作.

4.3 部署kerberos keytab文件
拷贝 hdfs.keytab 文件到其他节点的 /etc/hadoop/conf 目录

$ cd /var/kerberos/krb5kdc/

$ scp hdfs.keytab cdh1:/etc/hadoop/conf
$ scp hdfs.keytab cdh2:/etc/hadoop/conf
$ scp hdfs.keytab cdh3:/etc/hadoop/conf
并设置权限,分别在 cdh1,cdh2,cdh3 上执行:

$ ssh cdh1 "chown hdfs:hadoop /etc/hadoop/conf/hdfs.keytab ;chmod 400 /etc/hadoop/conf/hdfs.keytab"
$ ssh cdh2 "chown hdfs:hadoop /etc/hadoop/conf/hdfs.keytab ;chmod 400 /etc/hadoop/conf/hdfs.keytab"
$ ssh cdh3 "chown hdfs:hadoop /etc/hadoop/conf/hdfs.keytab ;chmod 400 /etc/hadoop/conf/hdfs.keytab"
由于 keytab 相当于有了永久凭证,不需要提供密码(如果修改kdc中的principal的密码,则该keytab就会失效),所以其他用户如果对该文件有读权限,就可以冒充 keytab 中指定的用户身份访问 hadoop,所以 keytab 文件需要确保只对 owner 有读权限(0400)
```
