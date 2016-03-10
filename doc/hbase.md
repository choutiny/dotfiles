HBase
=========
Hbase Apache Download [Hbase Apache](http://www.apache.org/dyn/closer.cgi/hbase/)
China Hbase Fastest Node [China Hbase Node](http://mirrors.cnnic.cn/apache/hbase)

#Install

###Install JAVA
----------------------
Oracle Java Download [Java 7](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
```
#mkdir /usr/java && cd /usr/java
#tar -zxvf jdk-7u79-linux-x64.tar.gz && mv jdk1.7.0_79 /usr/java/java7
#update-alternatives --install /usr/bin/java java /usr/java/java7/bin/java 1100
#update-alternatives --install /usr/bin/javac javac /usr/java/java7/bin/javac 1100
#update-alternatives --install /usr/bin/jar jar /usr/java/java7/bin/jar 1100
#update-alternatives --config java 
#update-alternatives --config javac
#update-alternatives --config jar

#export JAVA_HOME=/usr/java/java7
#export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar
#export PATH=$PATH:$JAVA_HOME/bin
do it both in user mode
java -version
```

###Install HBase
----------------------
```
#cd /tmp && wget http://mirrors.cnnic.cn/apache/hbase/stable/hbase-1.1.2-bin.tar.gz
#tar -zxvf hbase-0.98.16.1-src.tar.gz -C /usr/
#cd /usr && mv hbase-0.98.16.1 hbase

#export HBASE_HOME=/usr/hbase
#export PATH=$PATH:$HBASE_HOME/bin

gvim /usr/hbase/conf/hbase-env.sh 
uncomment and edit
export JAVA_HOME=/usr/java/java7/
```

###Verify Install
----------------------
```
#hbase version
```

#Usage
----------------------
###start hbase 
```
#$HBASE_HOME/bin/start-hbase.sh
or 
start-hbase.sh
```

###stop hbase
```
stop-hbase.sh
```

###modify default hbase tmp folder
    Edit conf/hbase-site.xml
    add the below content into <configuration>
```
    individual mode
    <property>
        <name>hbase.rootdir</name>
        <value>file:///home/tommy/hbase/</value>
    </property>

    cluster
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://localhost:9000/hbase</value>
    </property>
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
```

###go to hbase shell 
```
#hbase shell 
hbase(main):017:0> status
1 servers, 0 dead, 5.0000 average load
```
###open 60010 hbase web 
    Edit conf/hbase-site.xml
    add the below content into <configuration>
    http://127.0.0.1:60010
```
    <property>
        <name>hbase.master.info.port</name>
        <value>60010</value>
    </property>
```
###Address
```
http://{host}:50070/dfshealth.jsp     HBase build /hbase folder on HDFS for store data
http://{host}:60010/mster-status      HBase master page
http://{host}:60010/zk.jsp            ZooKeeper page
http://{host}:60010/table.jsp?name=wordcount Check wordcount table
http://{host}:60030/rs-status         Region server page
```

###Create Table need assign zookeeper data
    Edit conf/hbase-site.xml
    add the blow content into <configuration>
```
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/home/tommy/hbase/zookeeper</value>
    </property>
```

### Command
1.Create Table 
```
e.g.:create 'table_name','row family'
create 'mytable','row_1'

e.g.:list    #list table
list
TABLE
mytable
t2
2 row(s) in 0.0060 seconds

hbase(main):018:0> list 'user'
TABLE
user
1 row(s) in 0.0060 seconds
=> ["user"]
```

2.Write Data
```
e.g.: put 'table_name','rowkey', 'row family:field_name', 'field_value'
put 'mytable','first','cf:message','hello HBase'
put 'mytable','second','cf:foo', 0x0
put 'mytable','third','cf:bar', 3.14159

e.g.: create 'user','info'
put 'user', 'row_1', 'info:name', 'tommy'
put 'user', 'row_2', 'info:name', 'susan'
put 'user', 'row_2', 'info:email', 'susanl@gmail.com'
```
3.Read Data by get/scan
```
e.g.: get 'table_name', 'rowkey'     #et table_name rowkey data
hbase(main):021:0> get 'mytable', 'first'
COLUMN                                                       CELL
 cf:message                                                  timestamp=1451036405579, value=hello HBase

e.g.: get 'user','row_2','info:email'

e.g.: scan 'table_name'     #get all table_name data
hbase(main):022:0> scan 'mytable'
ROW                                                          COLUMN+CELL
 first                                                       column=cf:message, timestamp=1451036405579, value=hello HBase
 second                                                      column=cf:foo, timestamp=1451036428844, value=0
 third                                                       column=cf:bar, timestamp=1451036464702, value=3.14159
3 row(s) in 0.0210 seconds
```

4 Describe table
```
e.g.: describe 'table_name'
hbase(main):011:0> describe 'user'
Table user is ENABLED
user
COLUMN FAMILIES DESCRIPTION
{NAME => 'info', DATA_BLOCK_ENCODING => 'NONE', BLOOMFILTER => 'ROW', REPLICATION_SCOPE => '0', VERSIONS => '1', COMPRESSION => 'NONE', MIN_VERSIONS => '0', TTL => 'FOREVER', KEEP_DELETED_CELLS => 'FALSE', BLOCKSIZE => '65536', IN_MEMORY
 => 'false', BLOCKCACHE => 'true'}
1 row(s) in 0.0170 seconds
```

5 Disable and Drop table
```
e.g.: disable 'table_name'
e.g.: drop 'table_name'
```

6 Delete one cell
```
e.g.: delete 'table_name', 'rowkey', 'col:qual'
>delete 'testtable','myrow-2','colfam1:q2'
```

7  All command
```
normal command

status
Version

DDL
    alter,create,describe,disable,drop,enable,exists,is_disabled,is_enabled,list

DML
    count,delete,delteall,get,get_counter,incr,put,scan,truncate

Tool
    assign,balance_switch,balancer,compact,Flush,major_compact,Move,split,unassign,zk_dump

Replication
    add_peer,disable_peer,enable_peer,remove_peer,start_replication,stop_replication
```

#Instruction cn
--------------------
```
HBase以表的形式存储数据。表有行和列组成。列划分为若干个列族/列簇(column family)。

Row Key	column-family1	column-family2	column-family3
column1	column2	column1	column2	column3	column1
key1						
key2						
key3						
如上图所示，key1,key2,key3是三条记录的唯一的row key值，column-family1,column-family2,column-family3是三个列族，每个列族下又包括几列。比如column-family1这个列族下包括两列，名字是column1和column2，t1:abc,t2:gdxdf是由row key1和column-family1-column1唯一确定的一个单元cell。这个cell中有两个数据，abc和gdxdf。两个值的时间戳不一样，分别是t1,t2, hbase会返回最新时间的值给请求者。

这些名词的具体含义如下：
```

1 Row Key
```
与nosql数据库们一样,row key是用来检索记录的主键。访问hbase table中的行，只有三种方式：
    (1.1) 通过单个row key访问
    (1.2) 通过row key的range
    (1.3) 全表扫描
Row key行键 (Row key)可以是任意字符串(最大长度是 64KB，实际应用中长度一般为 10-100bytes)，在hbase内部，row key保存为字节数组。
存储时，数据按照Row key的字典序(byte order)排序存储。设计key时，要充分排序存储这个特性，将经常一起读取的行存储放到一起。(位置相关性)
注意： 字典序对int排序的结果是1,10,100,11,12,13,14,15,16,17,18,19,2,20,21,…,9,91,92,93,94,95,96,97,98,99。要保持整形的自然序，行键必须用0作左填充。
行的一次读写是原子操作 (不论一次读写多少列)。这个设计决策能够使用户很容易的理解程序在对同一个行进行并发更新操作时的行为。
```

2 列族 column family
```
hbase表中的每个列，都归属与某个列族。列族是表的chema的一部分(而列不是)，必须在使用表之前定义。列名都以列族作为前缀。例如courses:history ， courses:math 都属于 courses 这个列族。
访问控制、磁盘和内存的使用统计都是在列族层面进行的。实际应用中，列族上的控制权限能帮助我们管理不同类型的应用：我们允许一些应用可以添加新的基本数据、一些应用可以读取基本数据并创建继承的列族、一些应用则只允许浏览数据（甚至可能因为隐私的原因不能浏览所有数据）。
```

3 单元 Cell
```
HBase中通过row和columns确定的为一个存贮单元称为cell。由{row key, column( =<family> + <label>), version} 唯一确定的单元。cell中的数据是没有类型的，全部是字节码形式存贮。
```

4 时间戳 timestamp
```
每个cell都保存着同一份数据的多个版本。版本通过时间戳来索引。时间戳的类型是 64位整型。时间戳可以由hbase(在数据写入时自动 )赋值，此时时间戳是精确到毫秒的当前系统时间。时间戳也可以由客户显式赋值。如果应用程序要避免数据版本冲突，就必须自己生成具有唯一性的时间戳。每个cell中，不同版本的数据按照时间倒序排序，即最新的数据排在最前面。

为了避免数据存在过多版本造成的的管理 (包括存贮和索引)负担，hbase提供了两种数据版本回收方式。一是保存数据的最后n个版本，二是保存最近一段时间内的版本（比如最近七天）。用户可以针对每个列族进行设置。
```

#HBase shell的基本用法
----------------------

hbase提供了一个shell的终端给用户交互。使用命令hbase shell进入命令界面。通过执行 help可以看到命令的帮助信息。
以网上的一个学生成绩表的例子来演示hbase的用法。
```
name	grad	course
math	art
Tom	5	97	87
Jim	4	89	80
```
这里grad对于表来说是一个只有它自己的列族,course对于表来说是一个有两个列的列族,这个列族由两个列组成math和art,当然我们可以根据我们的需要在course中建立更多的列族,如computer,physics等相应的列添加入course列族。

1 建立一个表scores，有两个列族grad和courese
```
hbase(main):001:0> create 'scores','grade', 'course'

可以使用list命令来查看当前HBase里有哪些表。使用describe命令来查看表结构。（记得所有的表明、列名都需要加上引号）
```

2 按设计的表结构插入值：
```
put 'scores','Tom','grade:','5'
put 'scores','Tom','course:math','97'
put 'scores','Tom','course:art','87'
put 'scores','Jim','grade','4'
put 'scores','Jim','course:','89'
put 'scores','Jim','course:','80'

这样表结构就起来了，其实比较自由，列族里边可以自由添加子列很方便。如果列族下没有子列，加不加冒号都是可以的。
put命令比较简单，只有这一种用法：
hbase> put 't1', 'r1', 'c1', 'value', ts1
t1指表名，r1指行键名，c1指列名，value指单元格值。ts1指时间戳，一般都省略掉了。
```

3 根据键值查询数据
```
get 'scores','Jim'
get 'scores','Jim','grade'

可能你就发现规律了，HBase的shell操作，一个大概顺序就是操作关键词后跟表名，行名，列名这样的一个顺序，如果有其他条件再用花括号加上。
get有用法如下：
hbase> get 't1', 'r1'
hbase> get 't1', 'r1', {TIMERANGE => [ts1, ts2]}
hbase> get 't1', 'r1', {COLUMN => 'c1'}
hbase> get 't1', 'r1', {COLUMN => ['c1', 'c2', 'c3']}
hbase> get 't1', 'r1', {COLUMN => 'c1', TIMESTAMP => ts1}
hbase> get 't1', 'r1', {COLUMN => 'c1', TIMERANGE => [ts1, ts2], VERSIONS => 4}
hbase> get 't1', 'r1', {COLUMN => 'c1', TIMESTAMP => ts1, VERSIONS => 4}
hbase> get 't1', 'r1', 'c1'
hbase> get 't1', 'r1', 'c1', 'c2'
hbase> get 't1', 'r1', ['c1', 'c2']
```

4 扫描所有数据
```
scan 'scores'
也可以指定一些修饰词：TIMERANGE, FILTER, LIMIT, STARTROW, STOPROW, TIMESTAMP, MAXLENGTH,or COLUMNS。没任何修饰词，就是上边例句，就会显示所有数据行。

例句如下：
hbase> scan '.META.'
hbase> scan '.META.', {COLUMNS => 'info:regioninfo'}
hbase> scan 't1', {COLUMNS => ['c1', 'c2'], LIMIT => 10, STARTROW => 'xyz'}
hbase> scan 't1', {COLUMNS => 'c1', TIMERANGE => [1303668804, 1303668904]}
hbase> scan 't1', {FILTER => "(PrefixFilter ('row2') AND (QualifierFilter (>=, 'binary:xyz'))) AND (TimestampsFilter ( 123, 456))"}
hbase> scan 't1', {FILTER => org.apache.hadoop.hbase.filter.ColumnPaginationFilter.new(1, 0)}

过滤器filter有两种方法指出：
a. Using a filterString - more information on this is available in the
Filter Language document attached to the HBASE-4176 JIRA
b. Using the entire package name of the filter.

还有一个CACHE_BLOCKS修饰词，开关scan的缓存的，默认是开启的（CACHE_BLOCKS=>true），可以选择关闭（CACHE_BLOCKS=>false）。
```

5 删除指定数据
```
delete 'scores','Jim','grade'
delete 'scores','Jim'

删除数据命令也没太多变化，只有一个：
hbase> delete 't1', 'r1', 'c1', ts1
另外有一个deleteall命令，可以进行整行的范围的删除操作，慎用！
如果需要进行全表删除操作，就使用truncate命令，其实没有直接的全表删除命令，这个命令也是disable，drop，create三个命令组合出来的。
```

6 修改表结构
```
disable 'scores'
alter 'scores',NAME=>'info'
enable 'scores'

alter命令使用如下（如果无法成功的版本，需要先通用表disable）：

a、改变或添加一个列族：
hbase> alter 't1', NAME => 'f1', VERSIONS => 5

b、删除一个列族：
hbase> alter 't1', NAME => 'f1', METHOD => 'delete'
hbase> alter 't1', 'delete' => 'f1'

c、也可以修改表属性如MAX_FILESIZE
MEMSTORE_FLUSHSIZE, READONLY,和 DEFERRED_LOG_FLUSH：
hbase> alter 't1', METHOD => 'table_att', MAX_FILESIZE => '134217728'

d、可以添加一个表协同处理器
hbase> alter 't1', METHOD => 'table_att', 'coprocessor'=> 'hdfs:///foo.jar|com.foo.FooRegionObserver|1001|arg1=1,arg2=2'
一个表上可以配置多个协同处理器，一个序列会自动增长进行标识。加载协同处理器（可以说是过滤程序）需要符合以下规则：
[coprocessor jar file location] | class name | [priority] | [arguments]

e、移除coprocessor如下：
hbase> alter 't1', METHOD => 'table_att_unset', NAME => 'MAX_FILESIZE'
hbase> alter 't1', METHOD => 'table_att_unset', NAME => 'coprocessor$1'

f、可以一次执行多个alter命令：
hbase> alter 't1', {NAME => 'f1'}, {NAME => 'f2', METHOD => 'delete'}
```

7 统计行数：
```
hbase> count 't1'
hbase> count 't1', INTERVAL => 100000
hbase> count 't1', CACHE => 1000
hbase> count 't1', INTERVAL => 10, CACHE => 1000

count一般会比较耗时，使用mapreduce进行统计，统计结果会缓存，默认是10行。统计间隔默认的是1000行（INTERVAL）。
```

8 disable 和 enable 操作
```
很多操作需要先暂停表的可用性，比如上边说的alter操作，删除表也需要这个操作。disable_all和enable_all能够操作更多的表。
```

9 表的删除
```
先停止表的可使用性，然后执行删除命令。

drop 't1'

以上是一些常用命令详解，具体的所有hbase的shell命令如下，分了几个命令群，看英文是可以看出大概用处的，详细的用法使用help "cmd" 进行了解。

COMMAND GROUPS:
  Group name: general
  Commands: status, table_help, version, whoami

  Group name: ddl
  Commands: alter, alter_async, alter_status, create, describe, disable, disable_all, drop, drop_all, enable, enable_all, exists, get_table, is_disabled, is_enabled, list, show_filters

  Group name: namespace
  Commands: alter_namespace, create_namespace, describe_namespace, drop_namespace, list_namespace, list_namespace_tables

  Group name: dml
  Commands: append, count, delete, deleteall, get, get_counter, get_splits, incr, put, scan, truncate, truncate_preserve

  Group name: tools
  Commands: assign, balance_switch, balancer, balancer_enabled, catalogjanitor_enabled, catalogjanitor_run, catalogjanitor_switch, close_region, compact, compact_rs, flush, major_compact, merge_region, move, normalize, normalizer_enabled
, normalizer_switch, split, trace, unassign, wal_roll, zk_dump

  Group name: replication
  Commands: add_peer, append_peer_tableCFs, disable_peer, disable_table_replication, enable_peer, enable_table_replication, list_peers, list_replicated_tables, remove_peer, remove_peer_tableCFs, set_peer_tableCFs, show_peer_tableCFs

  Group name: snapshots
  Commands: clone_snapshot, delete_all_snapshot, delete_snapshot, list_snapshots, restore_snapshot, snapshot, snapshot_all, snapshot_restore

  Group name: configuration
  Commands: update_all_config, update_config

  Group name: quotas
  Commands: list_quotas, set_quota

  Group name: security
  Commands: grant, revoke, user_permission

  Group name: procedures
  Commands: abort_procedure, list_procedures

  Group name: visibility labels
  Commands: add_labels, clear_auths, get_auths, list_labels, set_auths, set_visibility
```

# Instruction
----------------------
1.Hbase 
```
Hbase use coordinate.
[rowkey, column family,column qualifer(qual)]
[TheRealMT, info,       name]

Put p = new Put(Bytes.toBytes("TheRealMT"));
p.add(Bytes.toBytes("info")),
    Bytes.toBytes("name"),
    Bytes.toBytes("Mark Twain");
p.add(Bytes.toBytes("info")),
    Bytes.toBytes("email"),
    Bytes.toBytes("samuel@clemens.org");
p.add(Bytes.toBytes("info")),
    Bytes.toBytes("password"),
    Bytes.toBytes("Langhorne");

hbase(main):019:0> put 'user','TheRealMT','info:name','Chouting'
0 row(s) in 0.0420 seconds
hbase(main):020:0> put 'user','TheRealMT','info:name','Tommy'
0 row(s) in 0.0040 seconds
```

```
进入hbase shell console

$HBASE_HOME/bin/hbase shell
如果有kerberos认证，需要事先使用相应的keytab进行一下认证（使用kinit命令），认证成功之后再使用hbase shell进入可以使用whoami命令可查看当前用户

hbase(main)> whoami
表的管理

1）查看有哪些表

hbase(main)> list
2）创建表

# 语法：create <table>, {NAME => <family>, VERSIONS => <VERSIONS>}
# 例如：创建表t1，有两个family name：f1，f2，且版本数均为2
hbase(main)> create 't1',{NAME => 'f1', VERSIONS => 2},{NAME => 'f2', VERSIONS => 2}
    

3）删除表

分两步：首先disable，然后drop

例如：删除表t1

hbase(main)> disable 't1'
hbase(main)> drop 't1'
4）查看表的结构

# 语法：describe <table>, desc <table>
# 例如：查看表t1的结构
hbase(main)> describe 't1'
5）修改表结构

修改表结构必须先disable

# 语法：alter 't1', {NAME => 'f1'}, {NAME => 'f2', METHOD => 'delete'}
# 例如：修改表test1的cf的TTL为180天
hbase(main)> disable 'test1'
hbase(main)> alter 'test1',{NAME=>'body',TTL=>'15552000'},{NAME=>'meta', TTL=>'15552000'}
hbase(main)> enable 'test1'
权限管理

1）分配权限

# 语法 : grant <user> <permissions> <table> <column family> <column qualifier> 参数后面用逗号分隔
# 权限用五个字母表示： "RWXCA".
# READ('R'), WRITE('W'), EXEC('X'), CREATE('C'), ADMIN('A')
# 例如，给用户‘test'分配对表t1有读写的权限，
hbase(main)> grant 'test','RW','t1'
2）查看权限

# 语法：user_permission <table>
# 例如，查看表t1的权限列表
hbase(main)> user_permission 't1'
3）收回权限

# 与分配权限类似，语法：revoke <user> <table> <column family> <column qualifier>
# 例如，收回test用户在表t1上的权限
hbase(main)> revoke 'test','t1'
表数据的增删改查

1）添加数据

# 语法：put <table>,<rowkey>,<family:column>,<value>,<timestamp>
# 例如：给表t1的添加一行记录：rowkey是rowkey001，family name：f1，column name：col1，value：value01，timestamp：系统默认
hbase(main)> put 't1','rowkey001','f1:col1','value01'
用法比较单一。

2）查询数据

a）查询某行记录

# 语法：get <table>,<rowkey>,[<family:column>,....]
# 例如：查询表t1，rowkey001中的f1下的col1的值
hbase(main)> get 't1','rowkey001', 'f1:col1'
# 或者：
hbase(main)> get 't1','rowkey001', {COLUMN=>'f1:col1'}
# 查询表t1，rowke002中的f1下的所有列值
hbase(main)> get 't1','rowkey001'
b）扫描表

# 语法：scan <table>, {COLUMNS => [ <family:column>,.... ], LIMIT => num}
# 另外，还可以添加STARTROW、TIMERANGE和FITLER等高级功能
# 例如：扫描表t1的前5条数据
hbase(main)> scan 't1',{LIMIT=>5}
c）查询表中的数据行数

# 语法：count <table>, {INTERVAL => intervalNum, CACHE => cacheNum}
# INTERVAL设置多少行显示一次及对应的rowkey，默认1000；CACHE每次去取的缓存区大小，默认是10，调整该参数可提高查询速度
# 例如，查询表t1中的行数，每100条显示一次，缓存区为500
hbase(main)> count 't1', {INTERVAL => 100, CACHE => 500}
3）删除数据

a )删除行中的某个列值

# 语法：delete <table>, <rowkey>,  <family:column> , <timestamp>,必须指定列名
# 例如：删除表t1，rowkey001中的f1:col1的数据
hbase(main)> delete 't1','rowkey001','f1:col1'
注：将删除改行f1:col1列所有版本的数据

b )删除行

# 语法：deleteall <table>, <rowkey>,  <family:column> , <timestamp>，可以不指定列名，删除整行数据
# 例如：删除表t1，rowk001的数据
hbase(main)> deleteall 't1','rowkey001'
c）删除表中的所有数据

# 语法： truncate <table>
# 其具体过程是：disable table -> drop table -> create table
# 例如：删除表t1的所有数据
hbase(main)> truncate 't1'
Region管理

1）移动region

# 语法：move 'encodeRegionName', 'ServerName'
# encodeRegionName指的regioName后面的编码，ServerName指的是master-status的Region Servers列表
# 示例
hbase(main)>move '4343995a58be8e5bbc739af1e91cd72d', 'db-41.xxx.xxx.org,60020,1390274516739'
2）开启/关闭region

# 语法：balance_switch true|false
hbase(main)> balance_switch
3）手动split

# 语法：split 'regionName', 'splitKey'
4）手动触发major compaction

#语法：

#Compact all regions in a table:
#hbase> major_compact 't1'
#Compact an entire region:
#hbase> major_compact 'r1'
#Compact a single column family within a region:
#hbase> major_compact 'r1', 'c1'
#Compact a single column family within a table:
#hbase> major_compact 't1', 'c1'
配置管理及节点重启

1）修改hdfs配置

hdfs配置位置：/etc/hadoop/conf

# 同步hdfs配置
cat /home/hadoop/slaves|xargs -i -t scp /etc/hadoop/conf/hdfs-site.xml hadoop@{}:/etc/hadoop/conf/hdfs-site.xml
#关闭：
cat /home/hadoop/slaves|xargs -i -t ssh hadoop@{} "sudo /home/hadoop/cdh4/hadoop-2.0.0-cdh4.2.1/sbin/hadoop-daemon.sh --config /etc/hadoop/conf stop datanode"
#启动：
cat /home/hadoop/slaves|xargs -i -t ssh hadoop@{} "sudo /home/hadoop/cdh4/hadoop-2.0.0-cdh4.2.1/sbin/hadoop-daemon.sh --config /etc/hadoop/conf start datanode"
2）修改hbase配置

hbase配置位置：

# 同步hbase配置
cat /home/hadoop/hbase/conf/regionservers|xargs -i -t scp /home/hadoop/hbase/conf/hbase-site.xml hadoop@{}:/home/hadoop/hbase/conf/hbase-site.xml
# graceful重启
cd ~/hbase
bin/graceful_stop.sh --restart --reload --debug inspurXXX.xxx.xxx.org
```

# hbase 设置replication复制
----------------------
hbase shell
```
    disable 'table_name'

    alter  'table_name',  { NAME => 'cf1', REPLICATION_SCOPE => 1} #开启table_name的replication, default=0, cf1 = column_family_1
    enable 'table_name'
    flush "table_name" #立即生效

    stop_replication,start_replication
```
test 
http://halo-cnode1.domain.org:16010/

master hbase-site.xml
```
<property>  
    <name>hbase.replication</name>  
    <value>true</value>  
</property>  
<property>
    <name>replication.source.nb.capacity</name>
    <value>25000</value>
    <description>主集群每次向从集群发送的entry最大的个数，默认值25000，可根据集群规模做出适当调整</description>
    <description>The master send maximum entry numbers to cluster, default, 25000,</description>
</property>
<property>
    <name>replication.source.size.capacity</name>
    <value>67108864</value>
    <description> 主集群每次向从集群发送的entry的包的最大值大小，默认为64M,不推荐过大 </description>
    <description> The master send maximun entry package size to cluster, default 64MB</description>
</property>
<property>
    <name>replication.source.ratio</name>
    <value>1</value>
    <description> 主集群使用的从集群的RS的数据百分比，默认为0.1，需调整为1，充分利用从集群的RS,主集群里使用slave服务器的百分比 </description>
    <description> The master use cluster RS ratio, default 0.1=10%, can increase to 100%</description>
</property>
<property>
    <name>replication.sleep.before.failover</name>
    <value>2000</value>
    <description> 主集群在RS(regionserver)宕机多长时间后(毫秒)进行failover，默认为2秒，具体的sleep时间是： sleepBeforeFailover + (long) (new Random().nextFloat() * sleepBeforeFailover) </description>
    <description> The master will failover after RS dump, default 2 seconds, the failover value=sleepBeforeFailover + (long) (new Random().nextFloat() * sleepBeforeFailover) </description>
</property>
<property>
    <name>replication.executor.workers</name>
    <value>1</value>
    <description> 从事replication的线程数，默认为1，如果写入量大，可以适当调大 </description>
    <description> The thread number of replication, default 1, if put is too large can increase the value</description>
</property>
<property>  
    <name>hbase.regionserver.wal.enablecompression</name>  
    <value>false</value> 
    <description> 主集群关闭hlog的压缩</description>  
</property> 

cluster hbase-site.xml
<property>
    <name>hbase.replication</name>
    <value>true</value>
</property>
```

use "verifyrep" to check
```
hbase org.apache.hadoop.hbase.mapreduce.replication.VerifyReplication --starttime=1265875194289 --stoptime=1265878794289 1 TestTable  
```
refer: http://hbase.apache.org/book.html#_cluster_replication


# hbase split table
----------------------
```
Hbase中split是一个很重要的功能，Hbase是通过把数据分配到一定数量的region来达到负载均衡的。一个table会被分配到一个或多个region中，这些region会被分配到一个或者多个regionServer中。在自动split策略中，当一个region达到一定的大小就会自动split成两个region。table在region中是按照row key来排序的，并且一个row key所对应的行只会存储在一个region中，这一点保证了Hbase的强一致性 。
在一个region中有一个或多个stroe，每个stroe对应一个column families(列族)。一个store中包含一个memstore 和 0 或 多个store files。每个column family 是分开存放和分开访问的。
disable 'table_name','cf1', {REGION_REPLICATION => 3}


Client 
    Disable auto flush for client writebuffer, close will contain flush.
RegionServer(RS)
    Split region when create table, design rowkey.
    Query
        Order read, close block cache
        Rand read, open block cache, set hfile.block.cache.size, use boolean filter.
    Compact & split, set  hbase.hregion.majorcompaction=0, set hbase.hregion.max.filesize.  when region hbase exceed this value will split it into RS.
    Memory, hbase.regionserver.global.memstore.upperLimit，hbase.regionserver.global.memstore.lowerLimit，memstore.flush .size
    HFile
        compress, GZIP, LZO, Snappy. (recommend LZO or Snappy)
            Algorithm   % remaining Encoding    Decoding
            GZIP        13.4%       21 MB/s     118 MB/s
            LZO         20.5%       135 MB/s    410 MB/s
            Snappy      22.2%       172 MB/s    409 MB/s
    create 'testtable', { NAME => 'colfam1', COMPRESSION => 'GZ' }
    create 'testtable', { NAME => 'colfam1', COMPRESSION => 'lzo' } 
        # need lzo and native liberary, copy native.jar into hadoop/lib/native and hbase/lib/native
        # core-site.xml
            <property>
                <name>io.compression.codecs</name>
                <value>org.apache.hadoop.io.compress.GzipCodec,org.apache.hadoop.io.compress.DefaultCodec,com.hadoop.compression.lzo.LzoCodec,com.hadoop.compression.lzo.LzopCodec
                </value>
            </property>
            <property>
                <name>io.compression.codec.lzo.class</name>
                <value>com.hadoop.compression.lzo.LzoCodec</value>
            </property>
    create 'testtable', { NAME => 'colfam1', COMPRESSION => 'snappy' } 
        # need snappy liberary, copy snappy-SNAPSHOT.jar into hbase, hadoop/lib 
        # core-site.xml
            <property>
                <name>io.compression.codecs</name>
                <value>org.apache.hadoop.io.compress.SnappyCodec
            </value>
            </property>
```


# Hbase thrift
----------------------
```
在查阅HBase文档（http://hbase.apache.org/book.html#config.files）后发现，负责外部系统与HBase通信的Thrift Server服务具有三个参数用来控制同时启动的线程数量。
这三个参数分别是：
l hbase.thrift.minWorkerThreads
l hbase.thrift.maxWorkerThreads
l hbase.thrift.maxQueuedRequests
 
hbase.thrift.minWorkerThreads是thrift server的最小线程数，默认值为16个。hbase.thrift.maxWorkerThreads是thrift server的最大线程数，默认值为1000个。hbase.thrift.maxQueuedRequests是在队列中等待的链接数量，默认值为1000个。
当程序访问HBase Thrift Server时，每当有一个新的连接就会创建一个新的线程，直到线程数量达到最小线程数。当线程池中没有空闲的线程时，新的连接会被加入队列。只有当队列中的等待连接数量超过队列的最大值时，才会为这些等待中的连接创建新的线程，直到线程数量达到最大线程数。当线程数量超过最大线程数时，Thrift Server就会开始丢弃连接。
解决办法
在HBase中加入上述三个参数并设置合适的线程数后，启动HBase Thrift Server服务，之前出现的阻塞问题即可解决。
```



