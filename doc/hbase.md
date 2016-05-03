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

hbase(main):004:0> scan "ambarismoketest"
ROW                                                          COLUMN+CELL                                                                                                                                                                     
 row01                                                       column=family:col01, timestamp=1458288344632, value=ida8c07755_date051816                                                                                                       
1 row(s) in 0.0170 seconds

hbase(main):005:0> delete "ambarismoketest", 'row01', 'family:col01'
0 row(s) in 0.0180 seconds
```

7  All command
```
COMMAND GROUPS:
  Group name: general
  Commands: status, table_help, version, whoami

  Group name: ddl
  Commands: alter, alter_async, alter_status, create, describe, disable, disable_all, drop, drop_all, enable, enable_all, exists, get_table, is_disabled, is_enabled, list, show_filters

  Group name: namespace
  Commands: alter_namespace, create_namespace, describe_namespace, drop_namespace, list_namespace, list_namespace_tables
  namespace命名空间指对一组表的逻辑分组，类似RDBMS中的database，方便对表在业务上划分。Apache HBase从0.98.0, 0.95.2两个版本开始支持namespace级别的授权操作，HBase全局管理员可以创建、修改和回收namespace的授权
    hbase>create_namespace 'ai_ns'          #创建namespace
    hbase>drop_namespace 'ai_ns'            #删除namespace
    hbase>describe_namespace 'ai_ns'        #查看namespace
    hbase>list_namespace                    #列出所有namespace
    hbase>create 'ai_ns:testtable', 'fm1'   #在namespace下创建表
    hbase>list_namespace_tables 'ai_ns'     #查看namespace下的表
    具备Create权限的namespace Admin可以对表创建和删除、生成和恢复快照
    具备Admin权限的namespace Admin可以对表splits或major compactions

    hbase>grant 'tenant-A' 'W' '@ai_ns'     #授权tenant-A用户对ai_ns下的写权限
    hbase>revoke 'tenant-A''@ai_ns'         #回收tenant-A用户对ai_ns的所有权限
    hbase>namespace_create 'hbase_perf'     #当前用户：hbase
    hbase>grant 'mike', 'W', '@hbase_perf'  #当前用户：mike
    hbase>create 'hbase_perf.table20', 'family1'  
    hbase>create 'hbase_perf.table50', 'family1'  
        mike创建了两张表table20和table50，同时成为这两张表的owner，意味着有'RWXCA'权限
        此时，mike团队的另一名成员alice也需要获得hbase_perf下的权限，hbase管理员操作如下
    当前用户：hbase

    hbase>grant 'alice', 'W', '@hbase_perf'  

    此时alice可以在hbase_perf下创建表，但是无法读、写、修改和删除hbase_perf下已存在的表
    当前用户：alice

    hbase>scan 'hbase_perf:table20'  

    报错AccessDeniedException
    如果希望alice可以访问已经存在的表，则hbase管理员操作如下
    当前用户：hbase
    hbase>grant 'alice', 'RW', 'hbase_perf.table20'  
    hbase>grant 'alice', 'RW', 'hbase_perf.table50'  

    在HBase中启用授权机制
    hbase-site.xml
    [html] view plain copy
    <property>  
         <name>hbase.security.authorization</name>  
         <value>true</value>  
    </property>  
    <property>  
         <name>hbase.coprocessor.master.classes</name>  
         <value>org.apache.hadoop.hbase.security.access.AccessController</value>  
    </property>  
    <property>  
         <name>hbase.coprocessor.region.classes</name>  
         <value>org.apache.hadoop.hbase.security.token.TokenProvider,org.apache.hadoop.hbase.security.access.AccessController</value>  
    </property>  
    配置完成后需要重启HBase集群


  Group name: dml
  Commands: append, count, delete, deleteall, get, get_counter, get_splits, incr, put, scan, truncate, truncate_preserve

  Group name: tools
  Commands: assign, balance_switch, balancer, balancer_enabled, catalogjanitor_enabled, catalogjanitor_run, catalogjanitor_switch, close_region, compact, compact_rs, flush, major_compact, merge_region, move, normalize, normalizer_enabled
, normalizer_switch, split, trace, unassign, wal_roll, zk_dump

  Group name: replication ,Replication 是基于列族的备份机制
  Commands: add_peer, append_peer_tableCFs, disable_peer, disable_table_replication, enable_peer, enable_table_replication, list_peers, list_replicated_tables, remove_peer, remove_peer_tableCFs, set_peer_tableCFs, show_peer_tableCFs
        peer: 同位体, 在网络结构体系中,任何与另一个实体处在同一层次上的功能单元或操作装置。

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

#Instruction cn
--------------------
```
HBase以表的形式存储数据.表有行和列组成.列划分为若干个列族/列簇(column family).

Row Key	column-family1	column-family2	column-family3
column1	column2	column1	column2	column3	column1
key1						
key2						
key3						
如上图所示,key1,key2,key3是三条记录的唯一的row key值,column-family1,column-family2,column-family3是三个列族,每个列族下又包括几列.比如column-family1这个列族下包括两列,名字是column1和column2,t1:abc,t2:gdxdf是由row key1和column-family1-column1唯一确定的一个单元cell.这个cell中有两个数据,abc和gdxdf.两个值的时间戳不一样,分别是t1,t2, hbase会返回最新时间的值给请求者.

这些名词的具体含义如下:
```

1 Row Key
```
与nosql数据库们一样,row key是用来检索记录的主键.访问hbase table中的行,只有三种方式:
    (1.1) 通过单个row key访问
    (1.2) 通过row key的range
    (1.3) 全表扫描
Row key行键 (Row key)可以是任意字符串(最大长度是 64KB,实际应用中长度一般为 10-100bytes),在hbase内部,row key保存为字节数组.
存储时,数据按照Row key的字典序(byte order)排序存储.设计key时,要充分排序存储这个特性,将经常一起读取的行存储放到一起.(位置相关性)
注意: 字典序对int排序的结果是1,10,100,11,12,13,14,15,16,17,18,19,2,20,21,…,9,91,92,93,94,95,96,97,98,99.要保持整形的自然序,行键必须用0作左填充.
行的一次读写是原子操作 (不论一次读写多少列).这个设计决策能够使用户很容易的理解程序在对同一个行进行并发更新操作时的行为.
```

2 列族 column family
```
hbase表中的每个列,都归属与某个列族.列族是表的chema的一部分(而列不是),必须在使用表之前定义.列名都以列族作为前缀.例如courses:history , courses:math 都属于 courses 这个列族.
访问控制、磁盘和内存的使用统计都是在列族层面进行的.实际应用中,列族上的控制权限能帮助我们管理不同类型的应用:我们允许一些应用可以添加新的基本数据、一些应用可以读取基本数据并创建继承的列族、一些应用则只允许浏览数据（甚至可能因为隐私的原因不能浏览所有数据）.
```

3 单元 Cell
```
HBase中通过row和columns确定的为一个存贮单元称为cell.由{row key, column( =<family> + <label>), version} 唯一确定的单元.cell中的数据是没有类型的,全部是字节码形式存贮.
```

4 时间戳 timestamp
```
每个cell都保存着同一份数据的多个版本.版本通过时间戳来索引.时间戳的类型是 64位整型.时间戳可以由hbase(在数据写入时自动 )赋值,此时时间戳是精确到毫秒的当前系统时间.时间戳也可以由客户显式赋值.如果应用程序要避免数据版本冲突,就必须自己生成具有唯一性的时间戳.每个cell中,不同版本的数据按照时间倒序排序,即最新的数据排在最前面.

为了避免数据存在过多版本造成的的管理 (包括存贮和索引)负担,hbase提供了两种数据版本回收方式.一是保存数据的最后n个版本,二是保存最近一段时间内的版本（比如最近七天）.用户可以针对每个列族进行设置.
```

#HBase shell的基本用法
----------------------

hbase提供了一个shell的终端给用户交互.使用命令hbase shell进入命令界面.通过执行 help可以看到命令的帮助信息.
以网上的一个学生成绩表的例子来演示hbase的用法.
```
name	grad	course
math	art
Tom	5	97	87
Jim	4	89	80
```
这里grad对于表来说是一个只有它自己的列族,course对于表来说是一个有两个列的列族,这个列族由两个列组成math和art,当然我们可以根据我们的需要在course中建立更多的列族,如computer,physics等相应的列添加入course列族.

1 建立一个表scores,有两个列族grad和courese
```
hbase(main):001:0> create 'scores','grade', 'course'

可以使用list命令来查看当前HBase里有哪些表.使用describe命令来查看表结构.（记得所有的表明、列名都需要加上引号）
```

2 按设计的表结构插入值:
```
put 'scores','Tom','grade:','5'
put 'scores','Tom','course:math','97'
put 'scores','Tom','course:art','87'
put 'scores','Jim','grade','4'
put 'scores','Jim','course:','89'
put 'scores','Jim','course:','80'

这样表结构就起来了,其实比较自由,列族里边可以自由添加子列很方便.如果列族下没有子列,加不加冒号都是可以的.
put命令比较简单,只有这一种用法:
hbase> put 't1', 'r1', 'c1', 'value', ts1
t1指表名,r1指行键名,c1指列名,value指单元格值.ts1指时间戳,一般都省略掉了.
```

3 根据键值查询数据
```
get 'scores','Jim'
get 'scores','Jim','grade'

可能你就发现规律了,HBase的shell操作,一个大概顺序就是操作关键词后跟表名,行名,列名这样的一个顺序,如果有其他条件再用花括号加上.
get有用法如下:
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
也可以指定一些修饰词:TIMERANGE, FILTER, LIMIT, STARTROW, STOPROW, TIMESTAMP, MAXLENGTH,or COLUMNS.没任何修饰词,就是上边例句,就会显示所有数据行.

例句如下:
hbase> scan '.META.'
hbase> scan '.META.', {COLUMNS => 'info:regioninfo'}
hbase> scan 't1', {COLUMNS => ['c1', 'c2'], LIMIT => 10, STARTROW => 'xyz'}
hbase> scan 't1', {COLUMNS => 'c1', TIMERANGE => [1303668804, 1303668904]}
hbase> scan 't1', {FILTER => "(PrefixFilter ('row2') AND (QualifierFilter (>=, 'binary:xyz'))) AND (TimestampsFilter ( 123, 456))"}
hbase> scan 't1', {FILTER => org.apache.hadoop.hbase.filter.ColumnPaginationFilter.new(1, 0)}

过滤器filter有两种方法指出:
a. Using a filterString - more information on this is available in the
Filter Language document attached to the HBASE-4176 JIRA
b. Using the entire package name of the filter.

还有一个CACHE_BLOCKS修饰词,开关scan的缓存的,默认是开启的（CACHE_BLOCKS=>true）,可以选择关闭（CACHE_BLOCKS=>false）.
```

5 删除指定数据
```
delete 'scores','Jim','grade'
delete 'scores','Jim'

删除数据命令也没太多变化,只有一个:
hbase> delete 't1', 'r1', 'c1', ts1

hbase(main):070:0> scan "test.domain"
ROW                                                          COLUMN+CELL                                                                                                                                                                     
 r1                                                          column=info:email, timestamp=1457599507962, value=tommyx@domain.com                                                                                                             
 r1                                                          column=info:name, timestamp=1457599498601, value=tommy                                                                                                                          
 r2                                                          column=info:email, timestamp=1457599523633, value=susanl@domain.com                                                                                                             
 r2                                                          column=info:name, timestamp=1457599531716, value=susanl                

hbase(main):071:0> delete "test.domain","r1","info:email"
0 row(s) in 0.4870 seconds

hbase(main):072:0> scan "test.domain"
ROW                                                          COLUMN+CELL                                                                                                                                                                     
 r1                                                          column=info:name, timestamp=1457599498601, value=tommy                                                                                                                          
 r2                                                          column=info:email, timestamp=1457599523633, value=susanl@domain.com                                                                                                             
 r2                                                          column=info:name, timestamp=1457599531716, value=susanl                                                                                                                         
2 row(s) in 1.1770 seconds


hbase(main):013:0> deleteall "test.domain","r2"
0 row(s) in 0.0250 seconds

hbase(main):014:0> scan 'test.domain'
ROW                                                          COLUMN+CELL                                                                                                                                                                     
0 row(s) in 0.7280 seconds



另外有一个deleteall命令,可以进行整行的范围的删除操作,慎用！
如果需要进行全表删除操作,就使用truncate命令,其实没有直接的全表删除命令,这个命令也是disable,drop,create三个命令组合出来的.
```

6 修改表结构
```
disable 'scores'
alter 'scores',NAME=>'info'
enable 'scores'

alter命令使用如下（如果无法成功的版本,需要先通用表disable）:

a、改变或添加一个列族:
hbase> alter 't1', NAME => 'f1', VERSIONS => 5

b、删除一个列族:
hbase> alter 't1', NAME => 'f1', METHOD => 'delete'
hbase> alter 't1', 'delete' => 'f1'

c、也可以修改表属性如MAX_FILESIZE
MEMSTORE_FLUSHSIZE, READONLY,和 DEFERRED_LOG_FLUSH:
hbase> alter 't1', METHOD => 'table_att', MAX_FILESIZE => '134217728'

d、可以添加一个表协同处理器
hbase> alter 't1', METHOD => 'table_att', 'coprocessor'=> 'hdfs:///foo.jar|com.foo.FooRegionObserver|1001|arg1=1,arg2=2'
一个表上可以配置多个协同处理器,一个序列会自动增长进行标识.加载协同处理器（可以说是过滤程序）需要符合以下规则:
[coprocessor jar file location] | class name | [priority] | [arguments]

e、移除coprocessor如下:
hbase> alter 't1', METHOD => 'table_att_unset', NAME => 'MAX_FILESIZE'
hbase> alter 't1', METHOD => 'table_att_unset', NAME => 'coprocessor$1'

f、可以一次执行多个alter命令:
hbase> alter 't1', {NAME => 'f1'}, {NAME => 'f2', METHOD => 'delete'}
```

7 统计行数:
```
hbase> count 't1'
hbase> count 't1', INTERVAL => 100000
hbase> count 't1', CACHE => 1000
hbase> count 't1', INTERVAL => 10, CACHE => 1000

count一般会比较耗时,使用mapreduce进行统计,统计结果会缓存,默认是10行.统计间隔默认的是1000行（INTERVAL）.
```

8 disable 和 enable 操作
```
很多操作需要先暂停表的可用性,比如上边说的alter操作,删除表也需要这个操作.disable_all和enable_all能够操作更多的表.
```

9 表的删除
```
先停止表的可使用性,然后执行删除命令.

drop 't1'

以上是一些常用命令详解,具体的所有hbase的shell命令如下,分了几个命令群,看英文是可以看出大概用处的,详细的用法使用help "cmd" 进行了解.

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
如果有kerberos认证,需要事先使用相应的keytab进行一下认证（使用kinit命令）,认证成功之后再使用hbase shell进入可以使用whoami命令可查看当前用户

hbase(main)> whoami
表的管理

1）查看有哪些表

hbase(main)> list
2）创建表

# 语法:create <table>, {NAME => <family>, VERSIONS => <VERSIONS>}
# 例如:创建表t1,有两个family name:f1,f2,且版本数均为2
hbase(main)> create 't1',{NAME => 'f1', VERSIONS => 2},{NAME => 'f2', VERSIONS => 2}
    

3）删除表

分两步:首先disable,然后drop

例如:删除表t1

hbase(main)> disable 't1'
hbase(main)> drop 't1'
4）查看表的结构

# 语法:describe <table>, desc <table>
# 例如:查看表t1的结构
hbase(main)> describe 't1'
5）修改表结构

修改表结构必须先disable

# 语法:alter 't1', {NAME => 'f1'}, {NAME => 'f2', METHOD => 'delete'}
# 例如:修改表test1的cf的TTL为180天
hbase(main)> disable 'test1'
hbase(main)> alter 'test1',{NAME=>'body',TTL=>'15552000'},{NAME=>'meta', TTL=>'15552000'}
hbase(main)> enable 'test1'
权限管理

1）分配权限

# 语法 : grant <user> <permissions> <table> <column family> <column qualifier> 参数后面用逗号分隔
# 权限用五个字母表示: "RWXCA".
# READ('R'), WRITE('W'), EXEC('X'), CREATE('C'), ADMIN('A')
# 例如,给用户‘test'分配对表t1有读写的权限,
hbase(main)> grant 'test','RW','t1'
2）查看权限

# 语法:user_permission <table>
# 例如,查看表t1的权限列表
hbase(main)> user_permission 't1'
3）收回权限

# 与分配权限类似,语法:revoke <user> <table> <column family> <column qualifier>
# 例如,收回test用户在表t1上的权限
hbase(main)> revoke 'test','t1'
表数据的增删改查

1）添加数据

# 语法:put <table>,<rowkey>,<family:column>,<value>,<timestamp>
# 例如:给表t1的添加一行记录:rowkey是rowkey001,family name:f1,column name:col1,value:value01,timestamp:系统默认
hbase(main)> put 't1','rowkey001','f1:col1','value01'
用法比较单一.

2）查询数据

a）查询某行记录

# 语法:get <table>,<rowkey>,[<family:column>,....]
# 例如:查询表t1,rowkey001中的f1下的col1的值
hbase(main)> get 't1','rowkey001', 'f1:col1'
# 或者:
hbase(main)> get 't1','rowkey001', {COLUMN=>'f1:col1'}
# 查询表t1,rowke002中的f1下的所有列值
hbase(main)> get 't1','rowkey001'
b）扫描表

# 语法:scan <table>, {COLUMNS => [ <family:column>,.... ], LIMIT => num}
# 另外,还可以添加STARTROW、TIMERANGE和FITLER等高级功能
# 例如:扫描表t1的前5条数据
hbase(main)> scan 't1',{LIMIT=>5}
c）查询表中的数据行数

# 语法:count <table>, {INTERVAL => intervalNum, CACHE => cacheNum}
# INTERVAL设置多少行显示一次及对应的rowkey,默认1000;CACHE每次去取的缓存区大小,默认是10,调整该参数可提高查询速度
# 例如,查询表t1中的行数,每100条显示一次,缓存区为500
hbase(main)> count 't1', {INTERVAL => 100, CACHE => 500}
3）删除数据

a )删除行中的某个列值

# 语法:delete <table>, <rowkey>,  <family:column> , <timestamp>,必须指定列名
# 例如:删除表t1,rowkey001中的f1:col1的数据
hbase(main)> delete 't1','rowkey001','f1:col1'
注:将删除改行f1:col1列所有版本的数据

b )删除行

# 语法:deleteall <table>, <rowkey>,  <family:column> , <timestamp>,可以不指定列名,删除整行数据
# 例如:删除表t1,rowk001的数据
hbase(main)> deleteall 't1','rowkey001'
c）删除表中的所有数据

# 语法: truncate <table>
# 其具体过程是:disable table -> drop table -> create table
# 例如:删除表t1的所有数据
hbase(main)> truncate 't1'
Region管理

1）移动region

# 语法:move 'encodeRegionName', 'ServerName'
# encodeRegionName指的regioName后面的编码,ServerName指的是master-status的Region Servers列表
# 示例
hbase(main)>move '4343995a58be8e5bbc739af1e91cd72d', 'db-41.xxx.xxx.org,60020,1390274516739'
2）开启/关闭region

# 语法:balance_switch true|false
hbase(main)> balance_switch
3）手动split

# 语法:split 'regionName', 'splitKey'
4）手动触发major compaction

#语法:

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

hdfs配置位置:/etc/hadoop/conf

# 同步hdfs配置
cat /home/hadoop/slaves|xargs -i -t scp /etc/hadoop/conf/hdfs-site.xml hadoop@{}:/etc/hadoop/conf/hdfs-site.xml
#关闭:
cat /home/hadoop/slaves|xargs -i -t ssh hadoop@{} "sudo /home/hadoop/cdh4/hadoop-2.0.0-cdh4.2.1/sbin/hadoop-daemon.sh --config /etc/hadoop/conf stop datanode"
#启动:
cat /home/hadoop/slaves|xargs -i -t ssh hadoop@{} "sudo /home/hadoop/cdh4/hadoop-2.0.0-cdh4.2.1/sbin/hadoop-daemon.sh --config /etc/hadoop/conf start datanode"
2）修改hbase配置

hbase配置位置:

# 同步hbase配置
cat /home/hadoop/hbase/conf/regionservers|xargs -i -t scp /home/hadoop/hbase/conf/hbase-site.xml hadoop@{}:/home/hadoop/hbase/conf/hbase-site.xml
# graceful重启
cd ~/hbase
bin/graceful_stop.sh --restart --reload --debug inspurXXX.xxx.xxx.org
```

# hbase 设置replication复制
----------------------
HBase replication采用的基本架构模式是：master-push；因为每个region server都有自己的write-ahead-log(即WAL或HLog)，这样就很容易记录下从上次复制之后又发生了什么，非常类似于其他一些著名的解决方案，就像MySQL 的主从复制就只用了一个binary log来进行追踪。一个master集群可以向任意数目的slave集群进行复制，同时每个region server会参与复制它本身所对应的一系列的修改。
Replication是异步进行的，这意味着参与的集群可能在地理位置上相隔甚远，它们之间的连接可以在某段时间内是断开的，插入到master集群中的那些行，在同一时间在slave集群上不一定是可用的(最终一致性)。
在该设计中所采用的replication格式在原理上类似于MySQL的基于状态的replication。在这里，不是SQL语句，而是整个的WALEdits(由来自客户端的put和delete操作的多个cell inserts组成)会被复制以维持原子性。
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
    <description>主集群每次向从集群发送的entry最大的个数,默认值25000,可根据集群规模做出适当调整</description>
    <description>The master send maximum entry numbers to cluster, default, 25000,</description>
</property>
<property>
    <name>replication.source.size.capacity</name>
    <value>67108864</value>
    <description> 主集群每次向从集群发送的entry的包的最大值大小,默认为64M,不推荐过大 </description>
    <description> The master send maximun entry package size to cluster, default 64MB</description>
</property>
<property>
    <name>replication.source.ratio</name>
    <value>1</value>
    <description> 主集群使用的从集群的RS的数据百分比,默认为0.1,需调整为1,充分利用从集群的RS,主集群里使用slave服务器的百分比 </description>
    <description> The master use cluster RS ratio, default 0.1=10%, can increase to 100%</description>
</property>
<property>
    <name>replication.sleep.before.failover</name>
    <value>2000</value>
    <description> 主集群在RS(regionserver)宕机多长时间后(毫秒)进行failover,默认为2秒,具体的sleep时间是: sleepBeforeFailover + (long) (new Random().nextFloat() * sleepBeforeFailover) </description>
    <description> The master will failover after RS dump, default 2 seconds, the failover value=sleepBeforeFailover + (long) (new Random().nextFloat() * sleepBeforeFailover) </description>
</property>
<property>
    <name>replication.executor.workers</name>
    <value>1</value>
    <description> 从事replication的线程数,默认为1,如果写入量大,可以适当调大 </description>
    <description> The thread number of replication, default 1, if put is too large can increase the value</description>
</property>
<property>  
    <name>hbase.regionserver.wal.enablecompression</name>   #Write Ahead Log (WAL)
    <value>false</value> 
    <description> 主集群关闭hlog的压缩</description>  
</property> 

cluster hbase-site.xml
<property>
    <name>hbase.replication</name>
    <value>true</value>
</property>
```

```
create 'table_name1', { NAME => 'cf1', REPLICATION_SCOPE => 1}

add_peer "1",'rs-cnode1.domain.org,rs-cnode2.domain.org,rs-cnod3.domain.org:2181:/hbase' 
     '1' 是peerID, 必须是short型的整数 
    'rs-cnode1.domain.org,rs-cnode2.domain.org,rs-cnod3.domain.org:2181:/hbase'  是一个字符串, 格式是"cluster zookeeper: cluster zookeeper port: cluster hbase zookeeper node"

历史数据迁移 
    $ bin/hbase org.apache.hadoop.hbase.mapreduce.CopyTable [--starttime=X] [--endtime=Y] [--new.name=NEW] [--peer.adr=ADR] tablename  
    sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.CopyTable --peer.adr=rs-cnode2.domain.org:2181:/hbase --families=cf1
    上面命令会复制table_name1:cf1 数据去cluster rs-cnode2.domain.org table_name1
    其他参数 --starttime=1459931000000 --endtime=1459936941022  
        会复制这个时间段的数据 

验证
halo-cnode1> put 't1','row1', 'cf1', 'value1'
rs-cnode2>get 't1','row1'

add_peer <ID> <CLUSTER_KEY>
list_peers #list all peer
enable_peer  <ID>
disable_peer <ID> 
remove_peer <ID>
enable_table_replication <TABLE_NAME>  #其中一个表中所有列族的replication
disable_table_replication <TABLE_NAME> #禁用一个表中所有列族的replication
```

use "verifyrep" to check
```
hbase org.apache.hadoop.hbase.mapreduce.replication.VerifyReplication --starttime=1265875194289 --stoptime=1265878794289 1 TestTable  
```
refer: http://hbase.apache.org/book.html#_cluster_replication


# hbase split table
----------------------
```
Hbase中split是一个很重要的功能,Hbase是通过把数据分配到一定数量的region来达到负载均衡的.一个table会被分配到一个或多个region中,这些region会被分配到一个或者多个regionServer中.在自动split策略中,当一个region达到一定的大小就会自动split成两个region.table在region中是按照row key来排序的,并且一个row key所对应的行只会存储在一个region中,这一点保证了Hbase的强一致性 .
在一个region中有一个或多个stroe,每个stroe对应一个column families(列族).一个store中包含一个memstore 和 0 或 多个store files.每个column family 是分开存放和分开访问的.
disable 'table_name','cf1', {REGION_REPLICATION => 3}


Client 
    Disable auto flush for client writebuffer, close will contain flush.
RegionServer(RS)
    Split region when create table, design rowkey.
    Query
        Order read, close block cache
        Rand read, open block cache, set hfile.block.cache.size, use boolean filter.
    Compact & split, set  hbase.hregion.majorcompaction=0, set hbase.hregion.max.filesize.  when region hbase exceed this value will split it into RS.
    Memory, hbase.regionserver.global.memstore.upperLimit,hbase.regionserver.global.memstore.lowerLimit,memstore.flush .size
    HFile
        压缩只在硬盘上存在, 在内存里(memstore或者blockcache)或者通过网络传输时是没有压缩的
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

hbase修改table压缩格式
disable 'table_name'
alter 'table_name', NAME => 'column family', COMPRESSION => 'snappy'    #alter apData,{NAME=>'cf1',COMPRESSION=>'snappy'}
如果输错cf, 会创建一个新的列族,需要删除掉 alter 'table_name', {NAME => 'cf', METHOD => 'delete'}
enable 'table_name'
enable表后，HBase表的压缩格式并没有生效，还需要一个动作，即HBase major_compact
major_compact 'table_name'  #动作耗时较长，会对服务有很大影响，可以选择在一个服务不忙的时间来做。
通过hadoop fs -du -s -h /hbase/table_name 可以知道通过major_compact后的数据大小

测试是否安装了snappy, hbase org.apache.hadoop.hbase.util.CompressionTest hdfs://host/path/to/hbase snappy




Regions是由每个Column Family的Store组成, hbase会把表切分成小一点儿的数据单位, 然后分配到多台服务器上,
    这些小一点儿的数据单位就叫region, 托管region的服务器就叫region server.
典型情况下, regionServer和HDFS DatNode并且配置在同一物理硬件上, RegionServer本质上是HDFS 客户端.
每个regionServer会托管多个Region
考虑到基础数据存储在HDFS上, 所有客户端都可以在一个命名空间上访问.
所有regionServer都可以访问文件里同一个文件, 理论上RS可以把本地DataNode作为主要DataNode进行读写操作.(减小网络IO)

Region大小, 通过hbase.hregion.max.filesize决定, 大于该值时会切分成两个region
Region的大小是一个棘手的问题,需要考量如下几个因素.
Regions是可用性和分布式的最基本单位
    HBase通过将region切分在许多机器上实现分布式.也就是说,你如果有16GB的数据,只分了2个region, 你却有20台机器,有18台就浪费了.
    region数目太多就会造成性能下降,现在比以前好多了.但是对于同样大小的数据,700个region比3000个要好.
    region数目太少就会妨碍可扩展性,降低并行能力.有的时候导致压力不够分散.这就是为什么,你向一个10节点的Hbase集群导入200MB的数据,大部分的节点是idle的.
    RegionServer中1个region和10个region索引需要的内存量没有太多的差别.
```

# HBase snapshot
----------------------
HBase以往数据的备份基于distcp或者copyTable等工具,这些备份机制或多或少对当前的online数据读写存在一定的影响,Snapshot提供了一种快速的数据备份方式,无需进行数据copy
基于snapshot文件,可以做clone一个新表,restore,export到另外一个集群中操作;其中clone生成的新表只是增加元数据,相关的数据文件还是复用snapshot指定的数据文件

Online
在线方式是enabletable,由Master指示region server进行snapshot操作,在此过程中,master和regionserver之间类似两阶段commit的snapshot操作
```

```
Offline
离线方式是disabletable,由HBase Master遍历HDFS中的table metadata和hfiles,建立对他们的引用.
```

```
快照:
   hbase> snapshot 'myTable','myTableSnapshot-122112'
列出当前所有得快照: 
    hbase> list_snapshots
删除快照信息: 
  hbase> delete_snapshot'myTableSnapshot-122112'
基于快照，clone一个新表: 
  hbase> clone_snapshot'myTableSnapshot-122112', 'myNewTestTable'
基于快照恢复表: 
  hbase> disable 'myTable'
  hbase> restore_snapshot'myTableSnapshot-122112'
 导出到另外一个集群中:
$bin/hbase class org.apache.hadoop.hbase.snapshot.tool.ExportSnapshot -snapshotMySnapshot -copy-to hdfs:///srv2:8082/hbase -mappers 16
```

# HBase thrift
----------------------
```
在查阅HBase文档（http://hbase.apache.org/book.html#config.files）后发现,负责外部系统与HBase通信的Thrift Server服务具有三个参数用来控制同时启动的线程数量.
这三个参数分别是:
l hbase.thrift.minWorkerThreads
l hbase.thrift.maxWorkerThreads
l hbase.thrift.maxQueuedRequests
 
hbase.thrift.minWorkerThreads是thrift server的最小线程数,默认值为16个.hbase.thrift.maxWorkerThreads是thrift server的最大线程数,默认值为1000个.hbase.thrift.maxQueuedRequests是在队列中等待的链接数量,默认值为1000个.
当程序访问HBase Thrift Server时,每当有一个新的连接就会创建一个新的线程,直到线程数量达到最小线程数.当线程池中没有空闲的线程时,新的连接会被加入队列.只有当队列中的等待连接数量超过队列的最大值时,才会为这些等待中的连接创建新的线程,直到线程数量达到最大线程数.当线程数量超过最大线程数时,Thrift Server就会开始丢弃连接.
解决办法
在HBase中加入上述三个参数并设置合适的线程数后,启动HBase Thrift Server服务,之前出现的阻塞问题即可解决.

ambari-hbase thrift
/usr/hdp/2.4.0.0-169/hbase/bin/hbase-daemon.sh start thrift
thrift默认的监听端口是9090，可以用netstat -nl | grep 9090
```

# HBase backup
----------------------
[hbase backup](http://hbase.apache.org/book.html#ops.backup)

1. 完全停掉hbase备份
    stop hbase and distcp, then restore

2. 在线对hbase集群复制备份
    replication, CopyTable, Export
    `$ bin/hbase org.apache.hadoop.hbase.mapreduce.Export <tablename> <outputdir> [<versions> [<starttime> [<endtime>]]]`
    `$ bin/hbase org.apache.hadoop.hbase.mapreduce.Import <tablename> <inputdir>`
inputdir指的是HDFS上的路径，建议使用绝对路径(hdfs://halo-cnode1:8020),  table的结构必须事先已经存在。
当导出数据的HBase版本和需要导入数据的HBase版本不一致时，在数据导入时可以指定备份文件是从哪个版本的HBase中导出来的，如果是从0.94版本的HBase导出来的，则命令如下：
    `$ bin/hbase -Dhbase.import.version=0.94 org.apache.hadoop.hbase.mapreduce.Driver import <tablename> <inputdir>`

$ hbase org.apache.hadoop.hbase.mapreduce.Export backup_table file:///opt/backup_table   
使用单机版做此操作是没有问题的，但是当使用多机版的hbase的时候，如果你的系统中有多个mapreduce的tasktracker。那么数据会被导出到多台机器（每个tasktracker）的local目录。
所以在使用export 命令在进行导出操作时，建议现将数据导出到hdfs中，然后再将数据从hdfs中获取下来
 默认不写file://的时候就是导出到hdfs上了  
hbase org.apache.hadoop.hbase.mapreduce.Export backup_table /tmp/backup_table   
hadoop dfs -get /tmp/backup_table /opt/backup_table  
如果在hbase中的一个row出现大量的数据，那么导出时会报出ScannerTimeoutException的错误。
这时候需要设置hbase.export.scaaner.batch 这个参数。这样导出时的错误就可以避免了。
hbase org.apache.hadoop.hbase.mapreduce.Export -Dhbase.export.scanner.batch=2000 backup_table /tmp/backup_table   
为了节省空间可以使用compress选项
hbase的数据导出的时候，如果不适用compress的选项，数据量的大小可能相差5倍。因此使用compress的选项，备份数据的时候是可以节省不少空间的
hbase org.apache.hadoop.hbase.mapreduce.Export -Dhbase.export.scanner.batch=2000 -D mapred.output.compress=true backup_table /tmp/backup_table  
```
hbase shell
list #get table.name

[root@halo-cnode1 backup]# sudo -u hdfs hadoop fs -mkdir /tommyx
[root@halo-cnode1 backup]# sudo -u hdfs hadoop fs -chown root:root /tommyx
[root@halo-cnode1 backup]# hbase org.apache.hadoop.hbase.mapreduce.Export "test.domain" /tommyx/test.domain

[root@halo-cnode1 backup]# hbase org.apache.hadoop.hbase.mapreduce.Export "ambarismoketest" /home/hdfs/backup
Exception in thread "main" org.apache.hadoop.security.AccessControlException: Permission denied: user=root, access=WRITE^C

[root@halo-cnode1 usr]# sudo -u hdfs hadoop fs -mkdir /user/root
[root@halo-cnode1 usr]# sudo -u hdfs hadoop fs -chown root:root /user/root

                
[root@halo-cnode1 backup]# hadoop dfs -cat /tommyx/test.domain/part-m-00000 #查看hdfs里面的存储的数据
[root@halo-cnode1 backup]# hadoop fs -text /tommyx/test.domain/part-m-00000 #查看hdfs里面的存储的数据
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.

SEQ1org.apache.hadoop.hbase.io.ImmutableBytesWritable%org.apache.hadoop.hbase.client.Result���;��س٩!j]r1V
-
r1infoemail �����*(2tommyx@domain.com
!
r1infoname ���*(2tommyx ([r2T
,
r2infoemail �ͷ��*(2suans@domain.com
 
r2infoname �����*(2suans ([root@halo-cnode1 backup]#

hadoop fs -copyToLocal /hbase/input ~/Documents/output_name
After that, I copied that data back to another hbase (other system) by following command
hadoop fs -copyFromLocal ~/Documents/input /hbase/mydata

hadoop fs -rm -r /user   #需要切换到该user下, 或者看http://halo-cnode1:50070/explorer.html#/ 里面的目录文件权限

hbase shell> deleteall 'test.domain', 'r1'
hbase shell> deleteall 'test.domain', 'r2'
hbase org.apache.hadoop.hbase.mapreduce.Import test.domain /tommyx/test.domain

hbase org.apache.hadoop.hbase.mapreduce.Import test.domain hdfs://halo-cnode1.domain.org:8020/tommyx/test.domain/part-m-00000
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import test.domain hdfs://halo-cnode1.domain.org:8020/tommyx/test.domain/part-m-00000


`restore`
---------------
sudo -h hdfs hadoop fs -mkdir /tommyx
hadoop fs -copyFromLocal /home/backup/test.domain /tommyx/test.domain
hbase shell> 
create "test.domain",{ NAME => 'info', REPLICATION_SCOPE => '1', COMPRESSION => 'snappy'}
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import test.domain /tommyx/test.domain
hbase shell> scan 'test.domain'
ROW COLUMN+CELL 
0 row(s) in 0.2290 seconds
hbase(main):003:0> scan 'test.domain'
ROW COLUMN+CELL 
r1 column=info:email, timestamp=1459335595708, value=tommyx@domain.com 
r1 column=info:name, timestamp=1459335571056, value=tommyx 
r2 column=info:email, timestamp=1459335587513, value=tester@domain.com 
r2 column=info:name, timestamp=1459335579163, value=tester 
2 row(s) in 0.0160 seconds



create_namespace 'testnamespace', {'PROERTY_NAME' => 'ServerStatus', NAME => 'info', REPLICATION_SCOPE => '0', COMPRESSION => 'snappy'}
create 'testnamespace:ServerStatusSnapshot', {NAME=>'f', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0'}, {NAME=>'info', COMPRESSION=>'SNAPPY', REPLICATION_SCOPE => '0'},  {NAME=>'status', COMPRESSION=>'SNAPPY',REPLICATION_SCOPE => '0'}
create 'testnamespace:ServerStatus', {NAME=>'info', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0'}, {NAME=>'sensor', COMPRESSION=>'SNAPPY', REPLICATION_SCOPE => '0'},  {NAME=>'status', COMPRESSION=>'SNAPPY',REPLICATION_SCOPE => '0'}
create 'testnamespace:LatestServerStatus', {NAME=>'f', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0'}, {NAME=>'info', COMPRESSION=>'SNAPPY', REPLICATION_SCOPE => '0'},  {NAME=>'status', COMPRESSION=>'SNAPPY',REPLICATION_SCOPE => '0'}
create 'history.statistics', { NAME => 'cf0', COMPRESSION => 'GZ', REPLICATION_SCOPE => '0'}
create 'history.session', { NAME => 'cf0', COMPRESSION => 'GZ', REPLICATION_SCOPE => '0'}
create 'history.recentstat', { NAME => 'cf0', COMPRESSION => 'GZ', REPLICATION_SCOPE => '0'}
create 'history.history', {NAME =>'cf0', COMPRESSION => 'SNAPPY',REPLICATION_SCOPE => '0'}, {NAME =>'cf1', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0'}
create 'document_demo', {NAME =>'doc', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0', VERSIONS => '3'}
create 'analytics_demo',{NAME =>'day', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0', VERSIONS => '3'}, {NAME =>'hour', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0', VERSIONS => '3'}, {NAME =>'total', COMPRESSION => 'SNAPPY', REPLICATION_SCOPE => '0', VERSIONS => '3'}



sudo -u hdfs hadoop fs -copyFromLocal ./analytics_demo /tommyx/analytics_demo
sudo -u hdfs hadoop fs -copyFromLocal ./document_demo /tommyx/document_demo
sudo -u hdfs hadoop fs -copyFromLocal ./history.recentstat /tommyx/history.recentstat
sudo -u hdfs hadoop fs -copyFromLocal ./history.session /tommyx/history.session
sudo -u hdfs hadoop fs -copyFromLocal ./history.statistics /tommyx/history.statistics
sudo -u hdfs hadoop fs -copyFromLocal ./ps_IdxLatestServerStatus /tommyx/ps_IdxLatestServerStatus
sudo -u hdfs hadoop fs -copyFromLocal ./ps_IdxServerStatusSnapshot /tommyx/ps_IdxServerStatusSnapshot
sudo -u hdfs hadoop fs -copyFromLocal ./ps_ServerStatus /tommyx/ps_ServerStatus
sudo -u hdfs hadoop fs -copyFromLocal ./history.history /tommyx/history.history

sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import analytics_demo /tommyx/analytics_demo
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import document_demo /tommyx/document_demo
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import history.recentstat /tommyx/history.recentstat
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import history.session /tommyx/history.session
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import history.statistics /tommyx/history.statistics
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import ps:IdxLatestServerStatus /tommyx/ps_IdxLatestServerStatus
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import ps:IdxServerStatusSnapshot /tommyx/ps_IdxServerStatusSnapshot
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import ps:ServerStatus /tommyx/ps_ServerStatus
sudo -u hdfs hbase org.apache.hadoop.hbase.mapreduce.Import history.history /tommyx/history.history
 
sudo -u hdfs hadoop fs -rm -r /tommyx/
sudo -u hfds hadoop fs -rm -r /user/hdfs/.Trash/

```


### Hbase Configuration
----------------------
```
zookeeper.session.timeout
默认值：3分钟（180000ms）
说明：RegionServer与Zookeeper间的连接超时时间。当超时时间到后，ReigonServer会被Zookeeper从RS集群清单中移除，HMaster收到移除通知后，会对这台server负责的regions重新balance，让其他存活的RegionServer接管.
调优：
这个timeout决定了RegionServer是否能够及时的failover。设置成1分钟或更低，可以减少因等待超时而被延长的failover时间。
不过需要注意的是，对于一些Online应用，RegionServer从宕机到恢复时间本身就很短的（网络闪断，crash等故障，运维可快速介入），如果调低timeout时间，反而会得不偿失。因为当ReigonServer被正式从RS集群中移除时，HMaster就开始做balance了（让其他RS根据故障机器记录的WAL日志进行恢复）。当故障的RS在人工介入恢复后，这个balance动作是毫无意义的，反而会使负载不均匀，给RS带来更多负担。特别是那些固定分配regions的场景。
hbase.zookeeper.quorum
默认值：localhost
说明：hbase所依赖的zookeeper部署
调优：
部署的zookeeper越多，可靠性就越高，但是部署只能部署奇数个，主要为了便于选出leader。最好给每个zookeeper 1G的内存和独立的磁盘，可以确保高性能。hbase.zookeeper.property.dataDir可以修改zookeeper保存数据的路径。
hbase.regionserver.handler.count
默认值：10
说明：RegionServer的请求处理IO线程数。
调优：
这个参数的调优与内存息息相关。
较少的IO线程，适用于处理单次请求内存消耗较高的Big PUT场景（大容量单次PUT或设置了较大cache的scan，均属于Big PUT）或ReigonServer的内存比较紧张的场景。
较多的IO线程，适用于单次请求内存消耗低，TPS要求非常高的场景。设置该值的时候，以监控内存为主要参考。
这里需要注意的是如果server的region数量很少，大量的请求都落在一个region上，因快速充满memstore触发flush导致的读写锁会影响全局TPS，不是IO线程数越高越好。
压测时，开启Enabling RPC-level logging，可以同时监控每次请求的内存消耗和GC的状况，最后通过多次压测结果来合理调节IO线程数。
这里是一个案例?Hadoop and HBase Optimization for Read Intensive Search Applications，作者在SSD的机器上设置IO线程数为100，仅供参考。
hbase.hregion.max.filesize
默认值：256M
说明：在当前ReigonServer上单个Reigon的最大存储空间，单个Region超过该值时，这个Region会被自动split成更小的region。
调优：
小region对split和compaction友好，因为拆分region或compact小region里的storefile速度很快，内存占用低。缺点是split和compaction会很频繁。
特别是数量较多的小region不停地split, compaction，会导致集群响应时间波动很大，region数量太多不仅给管理上带来麻烦，甚至会引发一些Hbase的bug。
一般512以下的都算小region。
大region，则不太适合经常split和compaction，因为做一次compact和split会产生较长时间的停顿，对应用的读写性能冲击非常大。此外，大region意味着较大的storefile，compaction时对内存也是一个挑战。
当然，大region也有其用武之地。如果你的应用场景中，某个时间点的访问量较低，那么在此时做compact和split，既能顺利完成split和compaction，又能保证绝大多数时间平稳的读写性能。
既然split和compaction如此影响性能，有没有办法去掉？
compaction是无法避免的，split倒是可以从自动调整为手动。
只要通过将这个参数值调大到某个很难达到的值，比如100G，就可以间接禁用自动split（RegionServer不会对未到达100G的region做split）。
再配合RegionSplitter这个工具，在需要split时，手动split。
手动split在灵活性和稳定性上比起自动split要高很多，相反，管理成本增加不多，比较推荐online实时系统使用。
内存方面，小region在设置memstore的大小值上比较灵活，大region则过大过小都不行，过大会导致flush时app的IO wait增高，过小则因store file过多影响读性能。
hbase.regionserver.global.memstore.upperLimit/lowerLimit
默认值：0.4/0.35
upperlimit说明：hbase.hregion.memstore.flush.size 这个参数的作用是当单个Region内所有的memstore大小总和超过指定值时，flush该region的所有memstore。RegionServer的flush是通过将请求添加一个队列，模拟生产消费模式来异步处理的。那这里就有一个问题，当队列来不及消费，产生大量积压请求时，可能会导致内存陡增，最坏的情况是触发OOM。
这个参数的作用是防止内存占用过大，当ReigonServer内所有region的memstores所占用内存总和达到heap的40%时，HBase会强制block所有的更新并flush这些region以释放所有memstore占用的内存。
lowerLimit说明： 同upperLimit，只不过lowerLimit在所有region的memstores所占用内存达到Heap的35%时，不flush所有的memstore。它会找一个memstore内存占用最大的region，做个别flush，此时写更新还是会被block。lowerLimit算是一个在所有region强制flush导致性能降低前的补救措施。在日志中，表现为 " Flush thread woke up with memory above low water."
调优：这是一个Heap内存保护参数，默认值已经能适用大多数场景。
参数调整会影响读写，如果写的压力大导致经常超过这个阀值，则调小读缓存hfile.block.cache.size增大该阀值，或者Heap余量较多时，不修改读缓存大小。
如果在高压情况下，也没超过这个阀值，那么建议你适当调小这个阀值再做压测，确保触发次数不要太多，然后还有较多Heap余量的时候，调大hfile.block.cache.size提高读性能。
还有一种可能性是?hbase.hregion.memstore.flush.size保持不变，但RS维护了过多的region，要知道 region数量直接影响占用内存的大小。
hfile.block.cache.size
默认值：0.2
说明：storefile的读缓存占用Heap的大小百分比，0.2表示20%。该值直接影响数据读的性能。
调优：当然是越大越好，如果写比读少很多，开到0.4-0.5也没问题。如果读写较均衡，0.3左右。如果写比读多，果断默认吧。设置这个值的时候，你同时要参考?hbase.regionserver.global.memstore.upperLimit?，该值是memstore占heap的最大百分比，两个参数一个影响读，一个影响写。如果两值加起来超过80-90%，会有OOM的风险，谨慎设置。
hbase.hstore.blockingStoreFiles
默认值：7
说明：在flush时，当一个region中的Store（Coulmn Family）内有超过7个storefile时，则block所有的写请求进行compaction，以减少storefile数量。
调优：block写请求会严重影响当前regionServer的响应时间，但过多的storefile也会影响读性能。从实际应用来看，为了获取较平滑的响应时间，可将值设为无限大。如果能容忍响应时间出现较大的波峰波谷，那么默认或根据自身场景调整即可。
hbase.hregion.memstore.block.multiplier
默认值：2
说明：当一个region里的memstore占用内存大小超过hbase.hregion.memstore.flush.size两倍的大小时，block该region的所有请求，进行flush，释放内存。
虽然我们设置了region所占用的memstores总内存大小，比如64M，但想象一下，在最后63.9M的时候，我Put了一个200M的数据，此时memstore的大小会瞬间暴涨到超过预期的hbase.hregion.memstore.flush.size的几倍。这个参数的作用是当memstore的大小增至超过hbase.hregion.memstore.flush.size 2倍时，block所有请求，遏制风险进一步扩大。
调优： 这个参数的默认值还是比较靠谱的。如果你预估你的正常应用场景（不包括异常）不会出现突发写或写的量可控，那么保持默认值即可。如果正常情况下，你的写请求量就会经常暴长到正常的几倍，那么你应该调大这个倍数并调整其他参数值，比如hfile.block.cache.size和hbase.regionserver.global.memstore.upperLimit/lowerLimit，以预留更多内存，防止HBase server OOM。
hbase.hregion.memstore.mslab.enabled
默认值：true
说明：减少因内存碎片导致的Full GC，提高整体性能。
调优：
hbase.client.scanner.caching
默认值：1
说明：scanner调用next方法一次获取的数据条数
调优：少的RPC是提高hbase执行效率的一种方法，理论上一次性获取越多数据就会越少的RPC，也就越高效。但是内存是最大的障碍。设置这个值的时候要选择合适的大小，一面一次性获取过多数据占用过多内存，造成其他程序使用内存过少。或者造成程序超时等错误（这个超时与hbase.regionserver.lease.period相关）。
hbase.regionserver.lease.period
默认值：60000
说明：客户端租用HRegion server 期限，即超时阀值。
调优：
这个配合hbase.client.scanner.caching使用，如果内存够大，但是取出较多数据后计算过程较长，可能超过这个阈值，适当可设置较长的响应时间以防被认为宕机。

hbase.rootdir
这 个目录是region server的共享目录，用来持久化Hbase。URL需要是'完全正确'的，还要包含文件系统的scheme。例如，要表示hdfs中的 '/hbase'目录，namenode 运行在namenode.example.org的9090端口。则需要设置为hdfs://namenode.example.org:9000 /hbase。默认情况下Hbase是写到/tmp的。不改这个配置，数据会在重启的时候丢失。
默认: file:///tmp/hbase-${user.name}/hbase
 hbase.master.port
Hbase的Master的端口.
默认: 60000
 hbase.cluster.distributed
Hbase的运行模式。false是单机模式，true是分布式模式。若为false,Hbase和Zookeeper会运行在同一个JVM里面。
默认: false
 hbase.tmp.dir
本地文件系统的临时文件夹。可以修改到一个更为持久的目录上。(/tmp会在重启时清楚)
默认: /tmp/hbase-${user.name}
 hbase.master.info.port
HBase Master web 界面端口. 设置为-1 意味着你不想让他运行。
默认: 60010
 hbase.master.info.bindAddress
HBase Master web 界面绑定的端口
默认: 0.0.0.0
 hbase.client.write.buffer
HTable 客户端的写缓冲的默认大小。这个值越大，需要消耗的内存越大。因为缓冲在客户端和服务端都有实例，所以需要消耗客户端和服务端两个地方的内存。得到的好处 是，可以减少RPC的次数。可以这样估算服务器端被占用的内存： hbase.client.write.buffer * hbase.regionserver.handler.count
默认: 2097152
 hbase.regionserver.port
HBase RegionServer绑定的端口
默认: 60020
 hbase.regionserver.info.port
HBase RegionServer web 界面绑定的端口 设置为 -1 意味这你不想与运行 RegionServer 界面.
默认: 60030
 hbase.regionserver.info.port.auto
Master或RegionServer是否要动态搜一个可以用的端口来绑定界面。当hbase.regionserver.info.port已经被占用的时候，可以搜一个空闲的端口绑定。这个功能在测试的时候很有用。默认关闭。
默认: false
 hbase.regionserver.info.bindAddress
HBase RegionServer web 界面的IP地址
默认: 0.0.0.0
 hbase.regionserver.class
RegionServer 使用的接口。客户端打开代理来连接region server的时候会使用到。
默认: org.apache.hadoop.hbase.ipc.HRegionInterface
 hbase.client.pause
通常的客户端暂停时间。最多的用法是客户端在重试前的等待时间。比如失败的get操作和region查询操作等都很可能用到。
默认: 1000
 hbase.client.retries.number
最大重试次数。例如 region查询，Get操作，Update操作等等都可能发生错误，需要重试。这是最大重试错误的值。
默认: 10
 hbase.client.scanner.caching
当 调用Scanner的next方法，而值又不在缓存里的时候，从服务端一次获取的行数。越大的值意味着Scanner会快一些，但是会占用更多的内存。当 缓冲被占满的时候，next方法调用会越来越慢。慢到一定程度，可能会导致超时。例如超过了 hbase.regionserver.lease.period。
默认: 1
 hbase.client.keyvalue.maxsize
一 个KeyValue实例的最大size.这个是用来设置存储文件中的单个entry的大小上界。因为一个KeyValue是不能分割的，所以可以避免因为 数据过大导致region不可分割。明智的做法是把它设为可以被最大region size整除的数。如果设置为0或者更小，就会禁用这个检查。默认10MB。
默认: 10485760
 hbase.regionserver.lease.period
客户端租用HRegion server 期限，即超时阀值。单位是毫秒。默认情况下，客户端必须在这个时间内发一条信息，否则视为死掉。
默认: 60000
 hbase.regionserver.handler.count
RegionServers受理的RPC Server实例数量。对于Master来说，这个属性是Master受理的handler数量
默认: 10
 hbase.regionserver.msginterval
RegionServer 发消息给 Master 时间间隔，单位是毫秒
默认: 3000
 hbase.regionserver.optionallogflushinterval
将Hlog同步到HDFS的间隔。如果Hlog没有积累到一定的数量，到了时间，也会触发同步。默认是1秒，单位毫秒。
默认: 1000
 hbase.regionserver.regionSplitLimit
region的数量到了这个值后就不会在分裂了。这不是一个region数量的硬性限制。但是起到了一定指导性的作用，到了这个值就该停止分裂了。默认是MAX_INT.就是说不阻止分裂。
默认: 2147483647
 hbase.regionserver.logroll.period
提交commit log的间隔，不管有没有写足够的值。
默认: 3600000
 hbase.regionserver.hlog.reader.impl
HLog file reader 的实现.
默认: org.apache.hadoop.hbase.regionserver.wal.SequenceFileLogReader
 hbase.regionserver.hlog.writer.impl
HLog file writer 的实现.
默认: org.apache.hadoop.hbase.regionserver.wal.SequenceFileLogWriter
 hbase.regionserver.thread.splitcompactcheckfrequency
region server 多久执行一次split/compaction 检查.
默认: 20000
 hbase.regionserver.nbreservationblocks
储备的内存block的数量(译者注:就像石油储备一样)。当发生out of memory 异常的时候，我们可以用这些内存在RegionServer停止之前做清理操作。
默认: 4
 hbase.zookeeper.dns.interface
当使用DNS的时候，Zookeeper用来上报的IP地址的网络接口名字。
默认: default
 hbase.zookeeper.dns.nameserver
当使用DNS的时候，Zookeepr使用的DNS的域名或者IP 地址，Zookeeper用它来确定和master用来进行通讯的域名.
默认: default
 hbase.regionserver.dns.interface
当使用DNS的时候，RegionServer用来上报的IP地址的网络接口名字。
默认: default
 hbase.regionserver.dns.nameserver
当使用DNS的时候，RegionServer使用的DNS的域名或者IP 地址，RegionServer用它来确定和master用来进行通讯的域名.
默认: default
 hbase.master.dns.interface
当使用DNS的时候，Master用来上报的IP地址的网络接口名字。
默认: default
 hbase.master.dns.nameserver
当使用DNS的时候，RegionServer使用的DNS的域名或者IP 地址，Master用它来确定用来进行通讯的域名.
默认: default
 hbase.balancer.period
    
Master执行region balancer的间隔。
默认: 300000
 hbase.regions.slop
当任一regionserver有average + (average * slop)个region是会执行Rebalance
默认: 0
 hbase.master.logcleaner.ttl
Hlog存在于.oldlogdir 文件夹的最长时间, 超过了就会被 Master 的线程清理掉.
默认: 600000
 hbase.master.logcleaner.plugins
LogsCleaner 服务会执行的一组LogCleanerDelegat。值用逗号间隔的文本表示。这些WAL/HLog cleaners会按顺序调用。可以把先调用的放在前面。你可以实现自己的LogCleanerDelegat，加到Classpath下，然后在这里写 下类的全称。一般都是加在默认值的前面。
默认: org.apache.hadoop.hbase.master.TimeToLiveLogCleaner
 hbase.regionserver.global.memstore.upperLimit
单个region server的全部memtores的最大值。超过这个值，一个新的update操作会被挂起，强制执行flush操作。
默认: 0.4
 hbase.regionserver.global.memstore.lowerLimit
当强制执行flush操作的时候，当低于这个值的时候，flush会停止。默认是堆大小的 35% . 如果这个值和 hbase.regionserver.global.memstore.upperLimit 相同就意味着当update操作因为内存限制被挂起时，会尽量少的执行flush(译者注:一旦执行flush，值就会比下限要低，不再执行)
默认: 0.35
 hbase.server.thread.wakefrequency
service工作的sleep间隔，单位毫秒。 可以作为service线程的sleep间隔，比如log roller.
默认: 10000
 hbase.hregion.memstore.flush.size
当memstore的大小超过这个值的时候，会flush到磁盘。这个值被一个线程每隔hbase.server.thread.wakefrequency检查一下。
默认: 67108864
 hbase.hregion.preclose.flush.size
当一个region中的memstore的大小大于这个值的时候，我们又触发了close.会先运行“pre-flush”操作，清理这个需要关闭的 memstore，然后将这个region下线。当一个region下线了，我们无法再进行任何写操作。如果一个memstore很大的时候，flush 操作会消耗很多时间。"pre-flush"操作意味着在region下线之前，会先把memstore清空。这样在最终执行close操作的时 候，flush操作会很快。
默认: 5242880
 hbase.hregion.memstore.block.multiplier
如果memstore有hbase.hregion.memstore.block.multiplier倍数的 hbase.hregion.flush.size的大小，就会阻塞update操作。这是为了预防在update高峰期会导致的失控。如果不设上 界，flush的时候会花很长的时间来合并或者分割，最坏的情况就是引发out of memory异常。(译者注:内存操作的速度和磁盘不匹配，需要等一等。原文似乎有误)
默认: 2
 hbase.hregion.memstore.mslab.enabled
体验特性：启用memStore分配本地缓冲区。这个特性是为了防止在大量写负载的时候堆的碎片过多。这可以减少GC操作的频率。(GC有可能会Stop the world)(译者注：实现的原理相当于预分配内存，而不是每一个值都要从堆里分配)
默认: false
 hbase.hregion.max.filesize
最大HStoreFile大小。若某个Column families的HStoreFile增长达到这个值，这个Hegion会被切割成两个。 Default: 256M.
默认: 268435456
 hbase.hstore.compactionThreshold
当一个HStore含有多于这个值的HStoreFiles(每一个memstore flush产生一个HStoreFile)的时候，会执行一个合并操作，把这HStoreFiles写成一个。这个值越大，需要合并的时间就越长。
默认: 3
 hbase.hstore.blockingStoreFiles
当一个HStore含有多于这个值的HStoreFiles(每一个memstore flush产生一个HStoreFile)的时候，会执行一个合并操作，update会阻塞直到合并完成，直到超过了hbase.hstore.blockingWaitTime的值
默认: 7
 hbase.hstore.blockingWaitTime
hbase.hstore.blockingStoreFiles所限制的StoreFile数量会导致update阻塞，这个时间是来限制阻塞时间的。当超过了这个时间，HRegion会停止阻塞update操作，不过合并还有没有完成。默认为90s.
默认: 90000
 hbase.hstore.compaction.max
每个“小”合并的HStoreFiles最大数量。
默认: 10
 hbase.hregion.majorcompaction
一个Region中的所有HStoreFile的major compactions的时间间隔。默认是1天。 设置为0就是禁用这个功能。
默认: 86400000
 hbase.mapreduce.hfileoutputformat.blocksize
MapReduce 中HFileOutputFormat可以写 storefiles/hfiles. 这个值是hfile的blocksize的最小值。通常在Hbase写Hfile的时候，bloocksize是由table schema(HColumnDescriptor)决定的，但是在mapreduce写的时候，我们无法获取schema中blocksize。这个值 越小，你的索引就越大，你随机访问需要获取的数据就越小。如果你的cell都很小，而且你需要更快的随机访问，可以把这个值调低。
默认: 65536
 hfile.block.cache.size
分配给HFile/StoreFile的block cache占最大堆(-Xmx setting)的比例。默认是20%，设置为0就是不分配。
默认: 0.2
 hbase.hash.type
哈希函数使用的哈希算法。可以选择两个值:: murmur (MurmurHash) 和 jenkins (JenkinsHash). 这个哈希是给 bloom filters用的.
默认: murmur
 hbase.master.keytab.file
HMaster server验证登录使用的kerberos keytab 文件路径。(译者注：Hbase使用Kerberos实现安全)
默认:
 hbase.master.kerberos.principal
例 如. "hbase/_HOST@EXAMPLE.COM". HMaster运行需要使用 kerberos principal name. principal name 可以在: user/hostname@DOMAIN 中获取. 如果 "_HOST" 被用做hostname portion，需要使用实际运行的hostname来替代它。
默认:
 hbase.regionserver.keytab.file
HRegionServer验证登录使用的kerberos keytab 文件路径。
默认:
 hbase.regionserver.kerberos.principal
例如. "hbase/_HOST@EXAMPLE.COM". HRegionServer运行需要使用 kerberos principal name. principal name 可以在: user/hostname@DOMAIN 中获取. 如果 "_HOST" 被用做hostname portion，需要使用实际运行的hostname来替代它。在这个文件中必须要有一个entry来描述 hbase.regionserver.keytab.file
默认:
 zookeeper.session.timeout
ZooKeeper 会话超时.Hbase把这个值传递改zk集群，向他推荐一个会话的最大超时时间。详见http://hadoop.apache.org /zookeeper/docs/current/zookeeperProgrammers.html#ch_zkSessions "The client sends a requested timeout, the server responds with the timeout that it can give the client. "。 单位是毫秒
默认: 180000
 zookeeper.znode.parent
ZooKeeper中的Hbase的根ZNode。所有的Hbase的ZooKeeper会用这个目录配置相对路径。默认情况下，所有的Hbase的ZooKeeper文件路径是用相对路径，所以他们会都去这个目录下面。
默认: /hbase
 zookeeper.znode.rootserver
ZNode 保存的 根region的路径. 这个值是由Master来写，client和regionserver 来读的。如果设为一个相对地址，父目录就是 ${zookeeper.znode.parent}.默认情形下，意味着根region的路径存储在/hbase/root-region- server.
默认: root-region-server
 hbase.zookeeper.quorum
Zookeeper 集群的地址列表，用逗号分割。例 如："host1.mydomain.com,host2.mydomain.com,host3.mydomain.com".默认是 localhost,是给伪分布式用的。要修改才能在完全分布式的情况下使用。如果在hbase-env.sh设置了HBASE_MANAGES_ZK， 这些ZooKeeper节点就会和Hbase一起启动。
默认: localhost
 hbase.zookeeper.peerport
ZooKeeper节点使用的端口。详细参见：http://hadoop.apache.org/zookeeper/docs/r3.1.1/zookeeperStarted.html#sc_RunningReplicatedZooKeeper
默认: 2888
 hbase.zookeeper.leaderport
ZooKeeper用来选择Leader的端口，详细参见：http://hadoop.apache.org/zookeeper/docs/r3.1.1/zookeeperStarted.html#sc_RunningReplicatedZooKeeper
默认: 3888
 hbase.zookeeper.property.initLimit
ZooKeeper的zoo.conf中的配置。 初始化synchronization阶段的ticks数量限制
默认: 10
 hbase.zookeeper.property.syncLimit
ZooKeeper的zoo.conf中的配置。 发送一个请求到获得承认之间的ticks的数量限制
默认: 5
 hbase.zookeeper.property.dataDir
ZooKeeper的zoo.conf中的配置。 快照的存储位置
默认: ${hbase.tmp.dir}/zookeeper
 hbase.zookeeper.property.clientPort
ZooKeeper的zoo.conf中的配置。 客户端连接的端口
默认: 2181
 hbase.zookeeper.property.maxClientCnxns
ZooKeeper的zoo.conf中的配置。 ZooKeeper集群中的单个节点接受的单个Client(以IP区分)的请求的并发数。这个值可以调高一点，防止在单机和伪分布式模式中出问题。
默认: 2000
 hbase.rest.port
HBase REST server的端口
默认: 8080
 hbase.rest.readonly
定义REST server的运行模式。可以设置成如下的值： false: 所有的HTTP请求都是被允许的 - GET/PUT/POST/DELETE. true:只有GET请求是被允许的
默认: false
```

###HBase Q&A
----------------------
1. ScannerTimeoutException
```
修改配置文件：$HBASE_HOME/conf/hbase-site.xml，修改或添加此属性
<property>
<name>hbase.regionserver.lease.period</name>
<value>180000</value>
</property>
二是修改程序，换一种思路，最好一次scan在60秒内总能返回至少一条结果。
看 HBase权威指南，发现还有中简单的方法：
Configuration conf = HBaseConfiguration.create()  
conf.setLong(HConstants.HBASE_REGIONSERVER_LEASE_PERIOD_KEY, 120000)  
```

2. regionServer dead
```
一将Zookeeper的timeout时间加长。
二是配置“hbase.regionserver.restart.on.zk.expire” 为true。 这样子，遇到ZooKeeper session expired ， regionserver将选择 restart 而不是 abort
具体的配置是，在hbase-site.xml中加入
<property>
<name>zookeeper.session.timeout</name>
<value>90000</value>
<description>ZooKeeper session timeout.
</property>

<property>
<name>hbase.regionserver.restart.on.zk.expire</name>
<value>true</value>
<description>
Zookeeper session expired will force regionserver exit.
Enable this will make the regionserver restart.
</description>
</property>

hbase.client.keyvalue.maxsize => 0  # for thrift client timeout
```

3. 如果一个HDFS上的文件大小(file size) 小于块大小(block size) ，那么HDFS会实际占用Linux file system的多大空间?
```
1. 往hdfs里面添加新文件前，hadoop在linux上面所占的空间为 464 MB：
2. 往hdfs里面添加大小为2673375 byte(大概2.5 MB)的文件： 2673375 derby.jar
3. 此时，hadoop在linux上面所占的空间为 467 MB——增加了一个实际文件大小(2.5 MB)的空间，而非一个block size(128 MB)：
4. 使用hadoop dfs -stat查看文件信息： 这里就很清楚地反映出： 文件的实际大小(file size)是2673375 byte， 但它的block size是128 MB。
5. 通过NameNode的web console来查看文件信息: 文件的实际大小(file size)是2673375 byte， 但它的block size是128 MB

值得注意的是，结果中有一个 ‘1（avg.block size 2673375 B）’的字样。这里的 'block size' 并不是指平常说的文件块大小(Block Size)—— 后者是一个元数据的概念，相反它反映的是文件的实际大小(file size)。以下是Hadoop Community的专家给我的回复： 
“The fsck is showing you an "average blocksize", not the block size metadata attribute of the file like stat shows. In this specific case, the average is just the length of your file, which is lesser than one whole block.”
最后一个问题是： 如果hdfs占用Linux file system的磁盘空间按实际文件大小算，那么这个”块大小“有必要存在吗？
其实块大小还是必要的，一个显而易见的作用就是当文件通过append操作不断增长的过程中，可以通过来block size决定何时split文件。以下是Hadoop Community的专家给我的回复： 
“The block size is a meta attribute. If you append tothe file later, it still needs to know when to split further - so it keeps that value as a mere metadata it can use to advise itself on write boundaries.” 
```
