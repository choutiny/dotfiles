HDFS
=========
[hdfs configuration](https://hadoop.apache.org/docs/r2.6.0/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml)

###command
---------
bin/hadoop fs -cmd <args> #cmd的命名通常与unix对应的命名名相同,如hadoop fs -ls

1. 添加目录和文件
```
HDFS有一个默认的工作目录 /user/$USER,其中$USER是你的登录用户名.不过目录不会自动建立,
`hadoop fs -mkdir /user/$USER` #mkdir 类似mkdir -p
`hadoop fs -put example.txt` . #会把本地example.txt的文件放到用户目录去,.就是/user/$USER
```
2. 检索文件
```
get命令与put命令相反,它从HDFS复制文件回到本地文件系统.
`hadoop fs -get example.txt`
复制到本地的当前工作目录中. 另一种是显示数据,用cat
`hadoop fs -cat example.txt`
```
3. 删除文件
```
rm命令
`hadoop fs -rm example.txt`
也可以用来删除空目录
`hadoop fs -rm -r /path/all file`
删除后到/user/username/.Trash下. 会有fs.trash.interval 垃圾回收周期, core-site.xml default=1440minutes
清空回收站
`hadoop fs -expunge`
`sudo -u hdfs  hadoop fs -du -s -h /user`
```

4. others
```
hadoop fs -ls /
hadoop fs -ls -R .
hadoop fs -put <local file> <hdfs file>         #列出hdfs文件系统所有的目录和文件
hadoop fs -put <local file or dir> <hdfs file>  #hdfs file的父目录一定要存在,否则命令不会执行
hadoop fs -put <local file or dir> <hdfs file>  #hdfs dir 一定要存在,否则命令不会执行
hadoop fs -put - <hdsf file>                    #从键盘读取输入到hdfs file中,按Ctrl+D结束输入,hdfs file不能存在,否则命令不会执行
hadoop fs -moveFromLocal <local src> <hdfs dst> #与put相类似,命令执行后源文件 local src 被删除,也可以从从键盘读取输入到hdfs file中
hadoop fs -copyFromLocal <local src> <hdfs dst> #与put相类似,也可以从从键盘读取输入到hdfs file中
hadoop fs -get <hdfs file> <local file/dir>     #local file不能和 hdfs file名字不能相同,否则会提示文件已存在,没有重名的文件会复制到本地
hadoop fs -get <hdfs file/dir> <local dir>      #拷贝多个文件或目录到本地时,本地要为文件夹路径,注意:如果用户不是root, local 路径要为用户文件夹下的路径,否则会出现权限问题,
hadoop fs -copyToLocal <local src> <hdfs dst>   #与get相类似
hadoop fs -mkdir <hdfs path>                    #只能一级一级的建目录,父目录不存在的话使用这个命令会报错
hadoop fs -mkdir -p <hdfs path>                 #所创建的目录如果父目录不存在就创建该父目录
hadoop fs -chown  -R <owner>:<group> <hdfs dst>
hadoop fs -chmod -R <mode> <hdfs dst>
hadoop fs -chgrp -R <groupp>  <hdfs url>
hadoop fs -getmerge <hdfs dir> <local file>     #将hdfs指定目录下所有文件排序后合并到local指定的文件中,文件不存在时会自动创建,文件存在时会覆盖里面的内容
hadoop fs -getmerge -nl <hdfs dir> <local file> #加上nl后,合并到local file中的hdfs文件之间会空出一行
hadoop fs -cp <hdfs file> <hdfs file>           #目标文件不能存在,否则命令不能执行,相当于给文件重命名并保存,源文件还存在
hadoop fs -cp <hdfs file/dir> <hdfs dir>        #目标文件夹要存在,否则命令不能执行
hadoop fs -mv <hdfs file>  <hdfs file>          #目标文件不能存在,否则命令不能执行,相当于给文件重命名并保存,源文件不存在
hadoop fs -mv  <hdfs file/dir> <hdfs dir>       #源路径有多个时,目标路径必须为目录,且必须存在. 注意:跨文件系统的移动(local到hdfs或者反过来)都是不允许的
hadoop fs -count <hdfs path>                    #统计hdfs对应路径下的目录个数,文件个数,文件总计大小 显示为目录个数,文件个数,文件总计大小,输入路径
hadoop fs -du <hdfs path>                       #显示hdfs对应路径下每个文件夹和文件的大小
hadoop fs -du -s <hdfs path>                    #显示hdfs对应路径下所有文件和的大小
hadoop fs -du -h <hdfs path>                    #显示hdfs对应路径下每个文件夹和文件的大小,文件的大小用方便阅读的形式表示,例如用64M代替67108864
hadoop fs -text <hdfs file>                     #将文本文件或某些格式的非文本文件通过文本格式输出
hadoop fs -setrep -R 3 <hdfs path>              #改变一个文件在hdfs中的副本个数,上述命令中数字3为所设置的副本个数,-R选项可以对一个人目录下的所有目录+文件递归执行改变副本个数的操作
hadoop fs -stat [format] <hdfs path>            #返回对应路径的状态信息 [format]可选参数有:%b(文件大小),%o(Block大小),%n(文件名),%r(副本个数),%y(最后一次修改日期和时间) `hadoop fs -stat %b%o%n <hdfs path>`
hadoop fs -tail <hdfs file>                     #在标准输出中显示文件末尾的1KB数据
hadoop archive -archiveName name.har -p <hdfs parent dir> <src >* <hdfs dst >
                            命令中参数name:压缩文件名,自己任意取;<hdfs parent dir> :压缩文件所在的父目录;< src >:要压缩的文件名;<hdfs dst >:压缩文件存放路径
                            *示例:hadoop archive -archiveName hadoop.har -p /user 1.txt 2.txt /des
                            示例中将hdfs中/user目录下的文件1.txt,2.txt压缩成一个名叫hadoop.har的文件存放在hdfs中/des目录下,如果1.txt,2.txt不写就是将/user目录下所有的目录和文件压缩成一个名叫hadoop.har的文件存放在hdfs中/des目录下
hadoop fs -ls /des/hadoop.jar                   #显示har的内容可以用如下命令:显示har压缩的是那些文件可以用如下命令
hadoop fs -ls -R har:///des/hadoop.har          #全选复制放进笔记, har文件不能进行二次压缩.如果想给.har加文件,只能找到原来的文件,重新创建一个.har文件中原来文件的数据并没有变化,har文件真正的作用是减少NameNode和DataNode过多的空间浪费.
hdfs balancer                                   #如果管理员发现某些DataNode保存数据过多,某些DataNode保存数据相对较少,可以使用上述命令手动启动内部的均衡过程
hdfs dfsadmin -help                             #管理员可以通过dfsadmin管理HDFS,用法可以通过上述命令查看
hdfs dfsadmin -report                           #显示文件系统的基本数据
hdfs dfsadmin -safemode < enter | leave | get | wait > #enter:进入安全模式;leave:离开安全模式;get:获知是否开启安全模式; wait:等待离开安全模式
distcp                                          #用来在两个HDFS之间拷贝数据
hdfs dfsadmin -refreshNodes
```

5. backup
```
你可以使用distcp命令在不同的datanode之间并行地复制大文件:
$ hadoop distcp hdfs://datanode1/foo hdfs://datanode2/bar
HDFS上的文件是使用URI来定位的,前缀都是hdfs://localhost:9000,你可以把这个前缀赋给属性fs.default.name(属性可以在配置文件中指定,也可以在代码中指定),这样你就不用每次都写这个前缀了,比如以下2个命令是等价的:
hfds://namenode.domain.org:8020/path/to/directory
$ hadoop fs -ls /
$ hadoop fs -ls hsfs://localhost:9000/
本地文件系统的前缀是file://
HDFS默认的文件备份数量是3,这个可以在dfs.replication属性中设置,在伪分布式模式中由于datanode只有一个,所以要把该值设为1.当你使用hadoop fs -ls命令时会得到形如:
drwxr-xr-x   　　- 　　tester 　　supergroup        0 　　2012-08-20 14:23　　 /tmp
-rw------- 　　　1 　　tester 　　supergroup 　　4 　　2012-08-20 14:23 　　/tmp/jobtracker.info
跟UNIX下的ls命令很像,其中第2列就是replication的数目,第5列是文件的长度,以B为单位(文件夹的长度是0,而在UNIX文件系统中目录的长度是512B的整倍数,因为目录所占的空间是以块为分配单位的,每块为512B).
上面已经提到大量的小文件会极大消耗namenode的内存,所以在这种情况下我们需要使用Hadoop Archives(HAR)把文件归档为一个大文件.
$ hadoop archive -archiveName tester.har -p /user/tester /user
把/user/tester下的所有文件打包成tester.tar放在/user目录下.
还可以查看一个har文件中包含哪些文件:
tester@testerpc:~$ hadoop fs -lsr har:///user/tester.har
drwxr-xr-x   - tester supergroup          0 2012-08-20 16:49 /user/tester.har/mse
-rw-r--r--   1 tester supergroup          0 2012-08-20 16:49 /user/tester.har/mse/list
-rw-r--r--   1 tester supergroup          0 2012-08-20 16:49 /user/tester.har/book
`hadoop fs -ls har:///user/tester.har/mse`
Found 1 items
-rw-r--r--   1 tester supergroup          0 2012-08-20 16:49 /user/tester.har/mse/list
HAR也是一个文件系统,一个Har URI的完整模式是har://<scheme>-<host>/<path>
tester@testerpc:~$ hadoop fs -lsr har://hdfs-localhost:9000/user/tester.har/mse
-rw-r--r--   1 tester supergroup          0 2012-08-20 16:49 /user/tester.har/mse/list
删除har文件必须使用rmr命令,用rm是不行的.
$ hadoop fs -rmr /user/tester.har
 使用HAR的一些限制:
会产生原始文件的完整备份,占用磁盘空间.当然你可以以在建好har文件后把原文件删掉.
HAR只是把多个文件打包成一个文件并没有采用任何的压缩策略.
HAR文件是不可变,如何你想增加或从har中删除一个文件,你只能重新归档.
InputFormat不理会har的存在,这意味着har文件对于MapReduce来说仍然会产生多个InputSlit,不会提高效率.要解决"小文件很多导致map task很多"的问题,可以采用CombineFileInputFormat.
Hadoop的备份系数是指每个block在hadoop集群中有几份,系数越高,冗余性越好,占用存储也越多.备份系数在hdfs-site.xml中定义,默认值为3.
修改hadoop的备份系数dfs.replication
查看hadoop集群的备份冗余情况 `hadoop fsck /`
sudo -u hdfs hadoop fsck /
su - hdfs
hdfs fsck / -files -blocks
 Total size:    14866531168 B (Total open files size: 415 B)
 Total dirs:    344
 Total files:   712
 Total symlinks:                0 (Files currently being written: 6)
 Total blocks (validated):      758 (avg. block size 19612837 B) (Total open file blocks (not validated): 5)
 Minimally replicated blocks:   758 (100.0 %)
 Over-replicated blocks:        0 (0.0 %)
 Under-replicated blocks:       0 (0.0 %)
 Mis-replicated blocks:         0 (0.0 %)
 Default replication factor:    1
 Average block replication:     3.0
 Corrupt blocks:                0
 Missing replicas:              0 (0.0 %)
 Number of data-nodes:          3
 Number of racks:               1
FSCK ended at Wed Mar 30 17:34:10 CST 2016 in 111 milliseconds
可以看见Average block replication 仍是3
需要修改hdfs中文件的备份系数.
修改hdfs文件备份系数:hadoop dfs -setrep [-R] <path>  如果有-R将修改子目录文件的性质.
`hadoop dfs -setrep -w 3 -R /user/hadoop/dir1` 就是把目录下所有文件备份系数设置为3, 如果你只有3个datanode,但是你却指定副本数为4,是不会生效的,因为每个datanode上只能存放一个副本
`sudo -u hdfs hadoop fs -setrep -R 2 /`
如果再fsck时候出错,往往是由于某些文件的备份不正常导致的,可以用hadoop的balancer工具修复
自动负载均衡hadoop文件:hadoop balancer, 不同节点之间复制数据的带宽是受限的,默认是1MB/s,可以通过hdfs-site.xml文件中的dfs.balance.bandwithPerSec属性指定(单位是字节).
sudo -u hdfs hadoop balancer
查看各节点的磁盘占用情况 hadoop dfsadmin -report
sudo -u hdfs /bin/hadoop dfsadmin -report
sudo -u hdfs hdfs dfsadmin -refreshNodes
sudo -u yarn yarn rmadmin -refreshNodes
sudo -u hdfs hadoop balancer
Ambari web->Services->HDFS->Summary-> Service Actions->Rebalance HDFS->Start
./bin/start-balancer.sh -threshold 10
hadoop fsck -locations 可以看到相应的提示信息,可以看到副本丢失率为0%:
`sudo -u hdfs hadoop fsck -locations  /` 
`Fix under-replicated blocks`
su - <$hdfs_user>
bash-4.1$ hdfs fsck / | grep 'Under replicated' | awk -F':' '{print $1}' >> /tmp/under_replicated_files 
-bash-4.1$ for hdfsfile in `cat /tmp/under_replicated_files`; do echo "Fixing $hdfsfile :" ;  hadoop fs -setrep 3 $hdfsfile; done
otal size:    14866530469 B (Total open files size: 415 B)
 Total dirs:    337
 Total files:   706
 Total symlinks:                0 (Files currently being written: 6)
 Total blocks (validated):      755 (avg. block size 19690768 B) (Total open file blocks (not validated): 5)
 Minimally replicated blocks:   755 (100.0 %)
 Over-replicated blocks:        0 (0.0 %)
 Under-replicated blocks:       0 (0.0 %)
 Mis-replicated blocks:         0 (0.0 %)
 Default replication factor:    1
 Average block replication:     1.0
 Corrupt blocks:                0
 Missing replicas:              0 (0.0 %)
 Number of data-nodes:          3
 Number of racks:               1
FSCK ended at Wed Mar 30 18:08:58 CST 2016 in 64 milliseconds
```

6. webhdfs
```
curl --negotiate -u : -b ~/cookiejar.txt -c ~/cookiejar.txt http://node1.domain.org:50070/webhdfs/v1/?op=liststatus   
```

7. HBASE in HDFS
```
hbase or hbase-unsecure, maybe in /apps/hbase
/hbase/.tmp             当对表做创建或者删除操作的时候,会将表move 到该 tmp 目录下,然后再去做处理操作
/hbase/archive          HBase 在做 Split或者 compact 操作完成之后,会将 HFile 移到.archive 目录中,
                        然后将之前的 hfile 删除掉,该目录由 HMaster 上的一个定时任务定期去清理
/hbase/corrupt          存储HBase做损坏的日志文件,一般都是为空的
/hbase/data             这个才是 hbase 的核心目录,0.98版本里支持 namespace 的概念模型,系统会预置两个 namespace 即:hbase和default
/hbase/data/default         这个默认的namespace即没有指定namespace 的表都将会flush 到该目录下面.
/hbase/data/hbase           这个namespace 下面存储了 HBase 的 namespace,meta 和acl 三个表,这里的 meta 表跟0.94版本的.META.是一样的,
                                自0.96之后就已经将 ROOT 表去掉了,直接从Zookeeper 中找到meta 表的位置,
                                然后通过 meta 表定位到 region. namespace 中存储了 HBase 中的所有 namespace 信息,
                                包括预置的hbase 和 default.acl 则是表的用户权限控制.
                            如果自定义一些 namespace 的话,就会再/hbase/data 目录下新建一个 namespace 文件夹,该 namespace 下的表都将 flush 到该目录下.
/hbase/WALs             HBase 是支持 WAL(Write Ahead Log)的,HBase在第一次启动之初会给每一台RegionServer在.log 下创建一个目录,
                            若客户端如果开启WAL模式,会先将数据写入一份到.log 下,当 RegionServer crash 或者目录达到一定大小,会开启 replay 模式,类似 MySQL 的 binlog.
/hbase/oldWALs          当WALs文件夹中的 HLog 没用之后会 move 到oldWALs中,HMaster会定期去清理, 
                            由参数hadoop.logfile.size 和 hadoop.logfile.count 来指定每个log file最大size和最大超出多少个logfile后作清理
                            以及hbase.master.logcleaner.ttl Hlog存在oldWALs的最长时间,默认600000
/hbase/.snapshot        hbase若开启了 snapshot 功能之后,对某一个用户表建立一个 snapshot 之后,snapshot 都存储在该目录下,
                            如对表test 做了一个 名为sp_test 的snapshot,就会在/hbase/.snapshot/目录下创建一个sp_test 文件夹,
                            snapshot 之后的所有写入都是记录在这个 snapshot 之上
/hbase/hbase.id         它是一个文件,存储集群唯一的 cluster id 号,是一个 uuid.
/hbase/hbase.version    同样也是一个文件,存储集群的版本号,貌似是加密的,看不到,只能通过web-ui 才能正确显示出来.
HBase 在HDFS上的文件可以被分为俩类,一类位于Hbase根目录下,另一类位于根目录的表目录下
.根级文件
### /hbase/WALs 被HLog实例管理的WAL文件.
### /hbase/WALs/data-hbase.com,60020,1443159380730
对于每个HregionServer,日志目录中都包含一个对应的子目录
### hbase/WALs/data-hbase.com,60020,1443159380730/data-hbase.com%2C60020%2C1443159380730.1443787240573
在每个子目录下有多个HLog文件(因为日志滚动)
### /hbase/oldWALs
当/hbase/WALs 中的HLog文件被持久化到存储文件中,不再需要日志文件时,它们会被移动到/hbase/oldWALs目录.
### /hbase/oldWALs/data-hbase.com%2C60020%2C1443159381290.1443787452518
具体的oldWALs文件.
### /hbase/hbase.id
集群的唯一ID
### /hbase/hbase.version
集群的文件格式版本信息
### /hbase/corrupt
损坏的日志文件,一般为空
### /hbase/archive/
存储表的归档和快照,HBase 在做 Split或者 compact 操作完成之后,会将 HFile 移到archive 目录中,然后将之前的 hfile 删除掉,该目录由 HMaster 上的一个定时任务定期去清理.
存储表的归档和快照具体目录:
/hbase/archive/data/default/表名/region名/列族名/fd2221d8d1ae4e579c21882f0ec4c5a5
### /hbase/.tmp
当对表做创建或者删除操作的时候,会将表move 到该 tmp 目录下,然后再去做处理操作.
### /hbase/data
hbase存储数据的核心目录
### /hbase/data/hbase
该目录存储了存储了 HBase 的 namespace,meta 和acl 三个系统级表.
namespace 中存储了 HBase 中的所有 namespace 信息,包括预置的hbase 和 default.acl 则是表的用户权限控制.
-/hbase/data/hbase/meta
-/hbase/data/hbase/namespace
-/hbase/data/hbase/acl
### /hbase/data/default/
该目录存储所有用户数据表
/hbase/data/default/表名
表目录
### /hbase/data/default/表名/.tabledesc
表的元数据信息
#### /hbase/data/default/PERFORMANCE_TEST/.tabledesc/.tableinfo.0000000008
表的元数据信息具体文件
### /hbase/data/default/表名/.tmp
中间临时数据,当.tableinfo被更新时该目录就会被用到
### /hbase/data/default/表名/f569a17359edb2250cdf07964be606a7(由region的表名+Start Key+时间戳产生的hashcode)
表中每一个region的目录
region 目录
### /hbase/data/default/表名/region名/.regioninfo
包含了对应region的HRegionInfo的序列化信息,类似.tableinfo.hbase hbck 工具可以用它来生成丢失的表条目元数据
### /hbase/data/default/表名/region名/列族名
每个列族的所有实际数据文件
#### /hbase/data/default/表名/region名/列族名/文件名
hbase实际数据文件
### /hbase/data/default/表名/region名/.tmp(按需创建)
存储临时文件,比如某个合并产生的重新写回的文件.
```

