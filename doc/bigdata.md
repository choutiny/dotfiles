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

###
