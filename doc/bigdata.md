Concept for hadoop
==================

###Zookeeper
---------------
ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，是Google的Chubby一个开源的实现，是Hadoop和Hbase的重要组件。它是一个为分布式应用提供一致性服务的软件，提供的功能包括：配置维护、域名服务、分布式同步、组服务等。
ZooKeeper的目标就是封装好复杂易出错的关键服务，将简单易用的接口和性能高效、功能稳定的系统提供给用户。
ZooKeeper包含一个简单的原语集，[1]  提供Java和C的接口。
ZooKeeper代码版本中，提供了分布式独享锁、选举、队列的接口，代码在zookeeper-3.4.3\src\recipes。其中分布锁和队列有Java和C两个版本，选举只有Java版本

ZooKeeper是以Fast Paxos算法为基础的，Paxos 算法存在活锁的问题，即当有多个proposer交错提交时，有可能互相排斥导致没有一个proposer能提交成功，而Fast Paxos作了一些优化，通过选举产生一个leader，只有leader才能提交proposer，具体算法可见Fast Paxos。因此，要想弄懂ZooKeeper首先得对Fast Paxos有所了解。[3] 
ZooKeeper的基本运转流程：
1、选举Leader。
2、同步数据。
3、选举Leader过程中算法有很多，但要达到的选举标准是一致的。
4、Leader要具有最高的zxid。
5、集群中大多数的机器得到响应并follow选出的Leader。[3] 

HBase和ZooKeeper
HBase内置有ZooKeeper，也可以使用外部ZooKeeper。
让HBase使用一个已有的不被HBase托管的Zookeep集群，需要设置 conf/hbase env sh文件中的HBASE_MANAGES_ZK 属性为 false
接下来，指明Zookeeper的host和端口。可以在 hbase-site.xml中设置, 也可以在HBase的CLASSPATH下面加一个zoo.cfg配置文件。 HBase 会优先加载 zoo.cfg 里面的配置，把hbase-site.xml里面的覆盖掉.
当HBase托管ZooKeeper的时候，Zookeeper集群的启动是HBase启动脚本的一部分。但你需要自己去运行。你可以这样做
${HBASE_HOME}/bin/hbase-daemons sh {start,stop} zookeeper
你可以用这条命令启动ZooKeeper而不启动HBase. HBASE_MANAGES_ZK 的值是 false， 如果你想在HBase重启的时候不重启ZooKeeper,你可以这样做


###Hbase
---------------
HBase是一个分布式的、面向列的开源数据库,源于google的一篇论文《bigtable：一个结构化数据的分布式存储系统》。HBase是Google Bigtable的开源实现，它利用Hadoop HDFS作为其文件存储系统，利用Hadoop MapReduce来处理HBase中的海量数据，利用Zookeeper作为协同服务。
HBase以表的形式存储数据。表有行和列组成。列划分为若干个列族/列簇(column family)。

Master选举：HBase基于Master-Slave模式架构，可以有多个HMaster，使用ZooKeeper实现了SPOF下Master的选举
租约管理：客户端与RegionServer交互时，会生成租约，该租约对象具有有效期
表元数据管理：HBase中包括用户表及其两个特殊的表：-ROOT-表和.META.表（例如，管理-ROOT-表中location信息，一个-ROOT-表只有一个Region，它保存了RegionServer的地址信息。）
协调RegionServer节点：数据变更会通过ZooKeeper同步复制到其他节点

Row Key	column-family1	column-family2	column-family3
column1	column2	column1	column2	column3	column1
key1						
key2						
key3						
如上图所示，key1,key2,key3是三条记录的唯一的row key值，column-family1,column-family2,column-family3是三个列族，每个列族下又包括几列。比如column-family1这个列族下包括两列，名字是column1和column2，t1:abc,t2:gdxdf是由row key1和column-family1-column1唯一确定的一个单元cell。这个cell中有两个数据，abc和gdxdf。两个值的时间戳不一样，分别是t1,t2, hbase会返回最新时间的值给请求者。

(1) Row Key

与nosql数据库们一样,row key是用来检索记录的主键。访问hbase table中的行，只有三种方式：
(1.1) 通过单个row key访问
(1.2) 通过row key的range
(1.3) 全表扫描

Row key行键 (Row key)可以是任意字符串(最大长度是 64KB，实际应用中长度一般为 10-100bytes)，在hbase内部，row key保存为字节数组。
存储时，数据按照Row key的字典序(byte order)排序存储。设计key时，要充分排序存储这个特性，将经常一起读取的行存储放到一起。(位置相关性)
注意：  字典序对int排序的结果是1,10,100,11,12,13,14,15,16,17,18,19,2,20,21,…,9,91,92,93,94,95,96,97,98,99。要保持整形的自然序，行键必须用0作左填充。

行的一次读写是原子操作 (不论一次读写多少列)。这个设计决策能够使用户很容易的理解程序在对同一个行进行并发更新操作时的行为。

(2) 列族 column family
hbase表中的每个列，都归属与某个列族。列族是表的chema的一部分(而列不是)，必须在使用表之前定义。列名都以列族作为前缀。例如courses:history ， courses:math 都属于 courses 这个列族。
访问控制、磁盘和内存的使用统计都是在列族层面进行的。实际应用中，列族上的控制权限能帮助我们管理不同类型的应用：我们允许一些应用可以添加新的基本数据、一些应用可以读取基本数据并创建继承的列族、一些应用则只允许浏览数据（甚至可能因为隐私的原因不能浏览所有数据）。

(3) 单元 Cell
HBase中通过row和columns确定的为一个存贮单元称为cell。由{row key, column( =<family> + <label>), version} 唯一确定的单元。cell中的数据是没有类型的，全部是字节码形式存贮。

(4) 时间戳 timestamp
每个cell都保存着同一份数据的多个版本。版本通过时间戳来索引。时间戳的类型是 64位整型。时间戳可以由hbase(在数据写入时自动 )赋值，此时时间戳是精确到毫秒的当前系统时间。时间戳也可以由客户显式赋值。如果应用程序要避免数据版本冲突，就必须自己生成具有唯一性的时间戳。每个cell中，不同版本的数据按照时间倒序排序，即最新的数据排在最前面。

为了避免数据存在过多版本造成的的管理 (包括存贮和索引)负担，hbase提供了两种数据版本回收方式。一是保存数据的最后n个版本，二是保存最近一段时间内的版本（比如最近七天）。用户可以针对每个列族进行设置。


###HIVE
---------------

###Solr
---------------
Solr是一个开源的分布式搜索引擎，支持索引的分片和复制，可以根据需要来线性增加节点，扩展集群。Solr使用ZooKeeper主要实现如下功能：

配置文件的管理：每个Collection都有对应的配置文件，多个分片共享配置文件（schema.xml、solrconfig.xml）
Collection管理：一个Solr集群可以有多个逻辑上独立的Collection，每个Collection又包括多个分片和副本
集群节点管理：Solr集群中有哪些活跃的节点可以使用，每个节点上都有Collection的分片（Shard）
Leader分片选举：一个Collection的多个分片可以设置冗余的副本，一个分片的多个副本中只有一个Leader可以进提供服务，如果某个存储Leader分片的节点宕机，Solr基于ZooKeeper来重新选出一个Leader分片，持续提供服务

###Lily
---------------
Lily是一个分布式数据管理平台，它基于Hadoop、HBase、Solr、ZooKeeper实现。使用ZooKeeper来注册Lily Node，从而管理集群节点的状态信息。

###Storm
---------------
Storm流式计算框架使用ZooKeeper来协调整个计算集群，Storm计算集群存在Nimbus和Supervisor两类节点。Nimbus负责分配任务（Topology），将任务信息写入ZooKeeper存储，然后Supervisor从ZooKeeper中读取任务信息。另外，Nimbus也监控集群中的计算任务节点，Supervisor也会发送心跳信息（包括状态信息）到ZooKeeper中，使得Nimbus可以实现状态的监控，任何计算节点出现故障，只要重新启动之后，继续从ZooKeeper中获取数据即可继续执行计算任务。

###Consul
---------------
Consul是HashiCorp公司推出的开源工具，用于实现分布式系统的服务发现与配置。与其他分布式服务注册与发现的方案，比如 Airbnb的SmartStack等相比，Consul的方案更“一站式”，内置了服务注册与发现框 架、分布一致性协议实现、健康检查、Key/Value存储、多数据中心方案，不再需要依赖其他工具（比如ZooKeeper等）。使用起来也较 为简单。Consul用Golang实现，因此具有天然可移植性(支持Linux、windows和Mac OS X)；安装包仅包含一个可执行文件，方便部署，与Docker等轻量级容器可无缝配合。

###YARN
---------------
为了能够对集群中的资源进行统一管理和调度，Hadoop 2.0引入了数据操作系统YARN。YARN的引入，大大提高了集群的资源利用率，并降低了集群管理成本。首先，YARN允许多个应用程序运行在一个集群中，并将资源按需分配给它们，这大大提高了资源利用率，其次，YARN允许各类短作业和长服务混合部署在一个集群中，并提供了容错、资源隔离及负载均衡等方面的支持，这大大简化了作业和服务的部署和管理成本。
YARN总体上采用master/slave架构，如图1所示，其中，master被称为ResourceManager，slave被称为NodeManager，ResourceManager负责对各个NodeManager上的资源进行统一管理和调度。当用户提交一个应用程序时，需要提供一个用以跟踪和管理这个程序的ApplicationMaster，它负责向ResourceManager申请资源，并要求NodeManger启动可以占用一定资源的Container。由于不同的ApplicationMaster被分布到不同的节点上，并通过一定的隔离机制进行了资源隔离，因此它们之间不会相互影响。
YARN中的资源管理和调度功能由资源调度器负责，它是Hadoop YARN中最核心的组件之一，是ResourceManager中的一个插拔式服务组件 。YARN通过层级化队列的方式组织和划分资源，并提供了多种多租户资源调度器，这种调度器允许管理员按照应用需求对用户或者应用程序分组，并为不同的分组分配不同的资源量，同时通过添加各种约束防止单个用户或者应用程序独占资源，进而能够满足各种QoS需求，典型代表是Yahoo！的Capacity Scheduler和Facebook的Fair Scheduler。
YARN作为一个通用数据操作系统，既可以运行像MapReduce、Spark这样的短作业，也可以部署像Web Server、MySQL Server这种长服务，真正实现一个集群多用途，这样的集群，我们通常称为轻量级弹性计算平台，说它轻量级，是因为YARN采用了cgroups轻量级隔离方案，说它弹性，是因为YARN能根据各种计算框架或者应用的负载或者需求调整它们各自占用的资源，实现集群资源共享，资源弹性收缩。

###Mesos
---------------
Mesos是一个开源的资源管理系统，可以对集群中的资源做弹性管理，目前twitter, apple等公司在大量使用mesos管理集群资源，大家记得apple的siri吗，它的后端便是采用的mesos进行资源管理（自行在网上查找文章：“新一代Siri后端将采用开放源代码平台Mesos”）。国内也有零零散散的公司在使用mesos，比如豆瓣。 Mesos是高仿google内部的资源管理系统borg（论文已经发表）实现的，随着近期它对docker容器支持的越来越好，将备受关注。（注：Mesosphere，一家试图围绕 Apache Mesos 项目开展商业活动的公司，不久前从 Andreessen Horowitz 那里获得了 1000 万美元投资。他做的事情就是用开源方案实现一个borg，选用的技术栈是：mesos+docker）。

Hadoop YARN要比Mesos更主流，前景更广阔。YARN在实现资源管理的系统前提下，能够跟hadoop生态系统完美结合，在YARN的东家hortonworks看来，YARN定位为大数据中的数据操作系统，能够更好地为上层各类应用程序（MapReduce/Spark）提供资源管理和调度功能。另外，非常重要的一点，YARN的社区力量要比Mesos强大的多，它的参与人员众多，周边系统的建设非常完善（包括最新诞生的apache二级项目Twill，Apache Twill ，cloudera的Kitten，均是方便大家使用YARN而诞生的项目）。
YARN是从MapReduce中演化而来的，因而在大数据处理中扮演重要角色，但这也使得它受限：它现在还不能看做是一个通用的资源管理系统，太多的内部实现过于狭隘，比如资源申请和分配模型，对长服务的支持等。不过，YARN自己仍把它定位在通用资源管理系统上，因而在不断改进，比如最近的版本中，增加了对长服务和docker的支持。


###Kafka
---------------
kafka作为时下最流行的开源消息系统，被广泛地应用在数据缓冲、异步通信、汇集日志、系统解耦等方面。相比较于RocketMQ等其他常见消息系统，Kafka在保障了大部分功能特性的同时，还提供了超一流的读写性能。
Kafka是Linkedin于2010年12月份开源的消息系统，它主要用于处理活跃的流式数据。活跃的流式数据在web网站应用中非常常见，这些数据包括网站的pv、用户访问了什么内容，搜索了什么内容等。 这些数据通常以日志的形式记录下来，然后每隔一段时间进行一次统计处理。
传统的日志分析系统提供了一种离线处理日志信息的可扩展方案，但若要进行实时处理，通常会有较大延迟。而现有的消（队列）系统能够很好的处理实时或者近似实时的应用，但未处理的数据通常不会写到磁盘上，这对于Hadoop之类（一小时或者一天只处理一部分数据）的离线应用而言，可能存在问题。Kafka正是为了解决以上问题而设计的，它能够很好地离线和在线应用。
2、  设计目标
（1）数据在磁盘上存取代价为O(1)。一般数据在磁盘上是使用BTree存储的，存取代价为O（lgn）。
（2）高吞吐率。即使在普通的节点上每秒钟也能处理成百上千的message。
（3）显式分布式，即所有的producer、broker和consumer都会有多个，均为分布式的。
（4）支持数据并行加载到Hadoop中。

###thrift
---------------
Thrift是一个跨语言的服务部署框架，最初由Facebook于2007年开发，2008年进入Apache开源项目。Thrift通过一个中间语言(IDL, 接口定义语言)来定义RPC的接口和数据类型，然后通过一个编译器生成不同语言的代码（目前支持C++,Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa, Smalltalk和OCaml）,并由生成的代码负责RPC协议层和传输层的实现。
