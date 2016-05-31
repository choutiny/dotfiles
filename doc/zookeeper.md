Zookeeper
=========
zookeeper是一个注册中心

###流程
----------------
```
1.服务提供者启动时向/dubbo/com.foo.BarService/providers目录下写入URL
2.服务消费者启动时订阅/dubbo/com.foo.BarService/providers目录下的URL向/dubbo/com.foo.BarService/consumers目录下写入自己的URL
3.监控中心启动时订阅/dubbo/com.foo.BarService目录下的所有提供者和消费者URL

支持以下功能:
1.当提供者出现断电等异常停机时,注册中心能自动删除提供者信息.
2.当注册中心重启时,能自动恢复注册数据,以及订阅请求.
3.当会话过期时,能自动恢复注册数据,以及订阅请求.
4.当设置<dubbo:registry check="false" />时,记录失败注册和订阅请求,后台定时重试.
5.可通过<dubbo:registry username="admin" password="1234" />设置zookeeper登录信息.
6.可通过<dubbo:registry group="dubbo" />设置zookeeper的根节点,不设置将使用无根树.
7.支持*号通配符<dubbo:reference group="*" version="*" />,可订阅服务的所有分组和所有版本的提供者.
```

###command
----------------
```
ps aux | grep zookeeper-server
netstat -tpnl | grep 2181
端口应该都是一个有互相通信的

测试
zookeeper-client -server host1:2181
zookeeper-client -server host:port cmd args


hortonworks:
rest_url=http://cnode1.domain,org:9998,http://cnode2.domain,org:9998,http://cnode3.domain,org:9998


ZooKeeper 四字命令

conf 输出相关服务配置的详细信息.
cons 列出所有连接到服务器的客户端的完全的连接 / 会话的详细信息.包括"接受 / 发送"的包数量,会话 id ,操作延迟,最后的操作执行等等信息.
dump 列出未经处理的会话和临时节点.
envi 输出关于服务环境的详细信息(区别于 conf 命令).
reqs 列出未经处理的请求
ruok 测试服务是否处于正确状态.如果确实如此,那么服务返回" imok ",否则不做任何相应.
stat 输出关于性能和连接的客户端的列表.
wchs 列出服务器 watch 的详细信息.
wchc 通过 session 列出服务器 watch 的详细信息,它的输出是一个与 watch 相关的会话的列表.
wchp 通过路径列出服务器 watch 的详细信息.它输出一个与 session 相关的路径.

shell:echo rouk | nc 192.168.85.333 2181

zk command:

ls: 命令来查看当前 ZooKeeper 中所包含的内容:
create: 创建一个新的 znode ,使用 create /zk myData .这个命令创建了一个新的 znode 节点" zk "以及与它关联的字符串:
get:    命令来确认第二步中所创建的 znode 是否包含我们所创建的字符串
set:    命令来对 zk 所关联的字符串进行设置
delete: delete /zk删除zk节点

ZooKeeper API 

功能        描述

create 在本地目录树中创建一个节点
delete 删除一个节点
exists 测试本地是否存在目标节点
get/set data 从目标节点上读取 / 写数据
get/set ACL 获取 / 设置目标节点访问控制列表信息
get children 检索一个子节点上的列表
sync 等待要被传送的数据
```

###Hbase in Zookeeper
----------------
```
hbaseid:集群id, 包含了集群ID, 跟存储在HDFS上的 hbase.id 文件中的一致
master:存储hmaster节点(Master启动后,注册在该节点中),包含了服务器名称
replication: 包含了replication的细节信息
root-region-server: 包含了持有 -ROOT- regions 的region server的服务器名称. 在region查找过程中会用到它ROOT表所在的regionserver(HMaster查找root表并分配给一个NodeServer上后,注册在zookeeper上)
rs: 作为所有region servers的根节点,会记录它们是何时启动.用来追踪服务器的失败.每个内部的znode节点是临时性的,以它所代表的region server的服务器名称为名子节点表示在线的region server(regionserver上线后,注册在rs下面)
draining:(HDFS currently has a way to exclude certain datanodes and prevent them from getting new blocks. HDFS goes one step further and even drains these nodes for you. This enhancement is a step in that direction.
The idea is that we mark nodes in zookeeper as draining nodes. This means that they don't get any more new regions. These draining nodes look exactly the same as the corresponding nodes in /rs, except they live under /draining.)
backup-masters:存储backup master节点(Backup master注册在该节点下)
shutdown:关闭的regionserver(关闭的失效的regionserver)
unassigned:子节点表示未分配的region(HMaster启动后,扫描HDFS中ROOT,META表,把所有的region放在这个节点下,待分配)
table:当一个表被禁用时,它会被添加到该节点下. 表名就是新创建的znode的名称,内容就是"DISABLED", 子节点表示表名称,内容表示表的状态,缓存表状态(如果无该表节点,表示未enabled的状态)
splitlog:(分布式split log,子节点是所有的需要split的WAL日志文件,在region server中有woker线程领取任务<锁住>,对该文件进行拆分,按照region分组,拆分到HDFS中的regioninfo下)

```


