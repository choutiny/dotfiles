Consul
========
```
Consul 是一个支持多数据中心分布式高可用的服务发现和配置共享的服务软件,由 HashiCorp 公司用 Go 语言开发,
基于 Mozilla Public License 2.0 的协议进行开源. Consul 支持健康检查,并允许 HTTP 和 DNS 协议调用 API 存储键值对.
命令行超级好用的虚拟机管理软件 vgrant 也是 HashiCorp 公司开发的产品.
一致性协议采用 Raft 算法,用来保证服务的高可用. 使用 GOSSIP 协议管理成员和广播消息, 并且支持 ACL 访问控制.
```

###使用场景
--------------
1. docker 实例的注册与配置共享
2. coreos 实例的注册与配置共享
3. vitess 集群
4. SaaS 应用的配置共享
5. 与 confd 服务集成，动态生成 nginx 和 haproxy 配置文件

###Concept
--------------
1. ACL 访问控制列表（Access Control List，ACL） 是路由器和交换机接口的指令列表，用来控制端口进出的数据包。ACL适用于所有的被路由协议，如IP、IPX、AppleTalk等。
```
ACL可以限制网络流量、提高网络性能。例如，ACL可以根据数据包的协议，指定数据包的优先级。
ACL提供对通信流量的控制手段。例如，ACL可以限定或简化路由更新信息的长度，从而限制通过路由器某一网段的通信流量。
ACL是提供网络安全访问的基本手段。ACL允许主机A访问人力资源网络，而拒绝主机B访问。
ACL可以在路由器端口处决定哪种类型的通信流量被转发或被阻塞。例如，用户可以允许E-mail通信流量被路由，拒绝所有的Telnet通信流量。
例如：某部门要求只能使用 WWW 这个功能，就可以通过ACL实现； 又例如，为了某部门的保密性，不允许其访问外网，也不允许外网访问它，就可以通过ACL实现。
```


###Running
--------------

consul shell
```
docker exec -t -i 287d1c82ca39 /bin/bash  #287d is consul docker container
```

consul web UI
```
http://172.17.0.2:8500/
```

consul port
```
53/tcp, 53/udp, 8300-8302/tcp, 8400/tcp, 8500/tcp, 8301-8302/udp
```

###Command
--------------
```
consul agent -server -bootstrap-expect 1 -data-dir /tmp/consul -node testServerName -dc domain.org  #启动
consul members  #查看成员
curl 127.0.0.1:8500/v1/catalog/nodes #查看节点
dig @127.0.0.1 -p 8600 testServerName.node.consul #使用DNS协议查看节点信息
```

注册两个 Mysql 服务的实例, 数据中心在 domain.org, 端口都是 3306. 具体为以下命令:
```
curl -X PUT -d '{"Datacenter": "domain.org", "Node": "mysql-1", "Address": \
"mysql-1.node.consul","Service": {"Service": "mysql", "tags": ["master","v1"], \
"Port": 3306}}' http://127.0.0.1:8500/v1/catalog/register

curl -X PUT -d '{"Datacenter": "domain.org", "Node": "mysql-2", "Address": \
"mysql-2.node.consul","Service": {"Service": "mysql", "tags": ["slave","v1"],\
"Port": 3306}}' http://127.0.0.1:8500/v1/catalog/register
```

curl http://127.0.0.1:8500/v1/catalog/service/mysql
```
 [
    {
        "Address": "mysql-1.node.consul",
        "Node": "mysql-1",
        "ServiceID": "mysql",
        "ServiceName": "mysql",
        "ServicePort": 3306,
        "ServiceTags": [
            "master",
            "v1"
        ]
    },
    {
        "Address": "mysql-2.node.consul",
        "Node": "mysql-2",
        "ServiceID": "mysql",
        "ServiceName": "mysql",
        "ServicePort": 3306,
        "ServiceTags": [
            "slave",
            "v1"
        ]
    }
]

dig @127.0.0.1 -p 8600 mysql.service.consul SRV

; <<>> DiG 9.10.0-P2 <<>> @127.0.0.1 -p 8600 mysql.service.consul SRV
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12821
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 2
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;mysql.service.consul.    IN  SRV

;; ANSWER SECTION:
mysql.service.consul. 0 IN  SRV 1 1 3306 mysql-2.node.domain.org.consul.
mysql.service.consul. 0 IN  SRV 1 1 3306 mysql-1.node.domain.org.consul.

;; ADDITIONAL SECTION:
mysql-2.node.domain.org.consul. 0 IN  CNAME mysql-2.node.consul.
mysql-1.node.domain.org.consul. 0 IN  CNAME mysql-1.node.consul.

;; Query time: 0 msec
;; SERVER: 127.0.0.1#8600(127.0.0.1)
;; MSG SIZE  rcvd: 280
```

###Register external domain
--------------
https://www.consul.io/docs/guides/external.html
```
curl -X PUT -d '{"Datacenter": "dc1", "Node": "cnode2", "Address": "192.168.85.115", "Service": {"Service": "cnode2"}}' http://172.17.0.2:8500/v1/catalog/register
```
