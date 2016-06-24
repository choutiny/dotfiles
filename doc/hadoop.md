Hadoop
=======
Hadoop Download [Hadoop Apache](https://hadoop.apache.org/releases.html)
China Hadoop Fastest Node [China Hadoop Node](http://mirrors.cnnic.cn/apache/hadoop/common)
Hadoop Opencas Node [Hadoop Opencas Node](http://apache.opencas.org/hadoop/common/)
Hadoop Fayea Node[Hadoop Fayea Node](http://apache.fayea.com/hadoop/common/)

#Install

###Install JAVA
------
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
#export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
#export PATH=$PATH:$JAVA_HOME/bin
do it both in user mode
java -version
```

###Install Hadoop
------
```
1. 
#cd /tmp && wget http://apache.fayea.com/hadoop/common/current/hadoop-2.7.1.tar.gz
#tar -zxvf hadoop-2.7.1.tar.gz -C /usr/
#cd /usr && mv hadoop-2.7.1 hadoop

2.
###debian###
adduser --system --shell /bin/bash --home /home/hadoop hadoop
###centos###
adduser --system --shell /bin/bash --create-home --home-dir /home/hadoop hadoop

passwd hadoop  123456

3.
need three server, one master, two cluster
vi three server hosts file && add 
192.168.85.109 project-cnode1 NameNode
192.168.85.115 project-cnode2 node1
192.168.85.119 project-cnode3 node2

4.
ssh-keygen -t rsa in project-cnode1 use hadoop user
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

do it in two node server under hadoop user

ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@project-cnode1
ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@project-cnode2
ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@project-cnode3
ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@NameNode
ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@node1
ssh-copy-id -i ~/.ssh/id_rsa.pub hadoop@node2

login each server and ssh project-cnode1,project-cnode2,project-cnode3

5.
go to three server and add sudo user for hadoop
sudo vim /etc/sudoers


6.
cd project-cnode1 home
vim /etc/profile

export HADOOP_HOME=/home/hadoop/hadoop-2.7.1
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin

source /etc/profile

7.
vim /home/hadoop/hadoop-2.7.1/etc/hadoop/hadoop-env.sh    
add
export JAVA_HOME=/usr/java/java7

8.
mkdir /home/hadoop/hadoop-2.7.1/tmp
mkdir /home/hadoop/hadoop-2.7.1/hdfs/data
mkdir /home/hadoop/hadoop-2.7.1/hdfs/data
mkdir /home/hadoop/hadoop-2.7.1/hdfs/name

9.
vim /home/hadoop/hadoop-2.7.1/etc/hadoop/core-site.xml  
add the below content into configuration

    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://NameNode:9000</value> 
    </property>
    <property>
        <name>dfs.replication</name> 
        <value>1</value> 
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/hadoop/hadoop-2.7.1/tmp</value> 
    </property>
    <property>
        <name>io.file.buffer.size</name>
        <value>131072</value>
    </property>

10.
cp /home/hadoop/hadoop-2.7.1/etc/hadoop/mapred-site.xml.template /home/hadoop/hadoop-2.7.1/etc/hadoop/mapred-site.xml
add the below content into configuration
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
        <final>true</final>
    </property>
    <property>
        <name>mapred.job.tracker</name>
        <value>NameNode:9001</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.address</name>
        <value>NameNode:10020</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>NameNode:19888</value>
    </property>
    <property>
        <name>mapreduce.jobtracker.http.address</name>
        <value>NameNode:50030</value>
    </property>

11.
vim /home/hadoop/hadoop-2.7.1/etc/hadoop/hdfs-site.xml
add the below content into configuration
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/hadoop/hadoop-2.7.1/hdfs/name</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/hadoop/hadoop-2.7.1/hdfs/data</value>
    </property>
    <property>
        <name>dfs.replication</name>
        <value>2</value>
    </property>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>NameNode:50090</value>
    </property>
    <property>
        <name>dfs.webhdfs.enabled</name>
        <value>true</value>
    </property>

12.
vim /home/hadoop/hadoop-2.7.1/etc/hadoop/yarn-site.xml
add the below content into configuration
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>NameNode</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>NameNode:8032</value>
    </property>
    <property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>NameNode:8030</value>
    </property>
    <property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>NameNode:8031</value>
    </property>
    <property>
        <name>yarn.resourcemanager.admin.address</name>
        <value>NameNode:8033</value>
    </property>
    <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>NameNode:8088</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>2048</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>1</value>
    </property>

13.
vim slaves
delete localhost
add
halo
project-cnode2
project-cnode3

14.
copy project-cnode1,halo
modify ulimit -n
vim /etc/security/limits.conf, for centos7
add the below content at the end of file then restart server

* soft nofile 102400
* hard nofile 102400

cat /proc/sys/fs/file-max  will affect the limits

15.
ntpdate
ntpdate time.windows.com

16.
close iptables,selinux
systemctl stop iptables
systemctl disable firewalld
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux; setenforce 0

17.
start
su - hadoop on project-cnode1
hdfs namenode -format
start-all.sh
stop-all.sh

#export YARN_LOG_DIR=$HADOOP_LOG_DIR
```

###Verify Install
------
```

#hadoop version
jps
hadoop dfsadmin -report
```

#HADOOP Q&A
----------------------
1 ScannerTimeoutException
```
修改配置文件:$HBASE_HOME/conf/hbase-site.xml,修改或添加此属性
<property>
<name>hbase.regionserver.lease.period</name>
<value>180000</value>
</property>
二是修改程序,换一种思路,最好一次scan在60秒内总能返回至少一条结果.
看 HBase权威指南,发现还有中简单的方法:
Configuration conf = HBaseConfiguration.create()  
conf.setLong(HConstants.HBASE_REGIONSERVER_LEASE_PERIOD_KEY, 120000)  
```
2 RegionServer dead
```
一将Zookeeper的timeout时间加长.
二是配置"hbase.regionserver.restart.on.zk.expire" 为true. 这样子,遇到ZooKeeper session expired , regionserver将选择 restart 而不是 abort
具体的配置是,在hbase-site.xml中加入
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
3 如果一个HDFS上的文件大小(file size) 小于块大小(block size) ,那么HDFS会实际占用Linux file system的多大空间?
```
1. 往hdfs里面添加新文件前,hadoop在linux上面所占的空间为 464 MB:
2. 往hdfs里面添加大小为2673375 byte(大概2.5 MB)的文件: 2673375 derby.jar
3. 此时,hadoop在linux上面所占的空间为 467 MB--增加了一个实际文件大小(2.5 MB)的空间,而非一个block size(128 MB):
4. 使用hadoop dfs -stat查看文件信息: 这里就很清楚地反映出: 文件的实际大小(file size)是2673375 byte, 但它的block size是128 MB.
5. 通过NameNode的web console来查看文件信息: 文件的实际大小(file size)是2673375 byte, 但它的block size是128 MB

值得注意的是,结果中有一个 '1(avg.block size 2673375 B)'的字样.这里的 'block size' 并不是指平常说的文件块大小(Block Size)-- 后者是一个元数据的概念,相反它反映的是文件的实际大小(file size).以下是Hadoop Community的专家给我的回复: 
"The fsck is showing you an "average blocksize", not the block size metadata attribute of the file like stat shows. In this specific case, the average is just the length of your file, which is lesser than one whole block."
最后一个问题是: 如果hdfs占用Linux file system的磁盘空间按实际文件大小算,那么这个"块大小"有必要存在吗?
其实块大小还是必要的,一个显而易见的作用就是当文件通过append操作不断增长的过程中,可以通过来block size决定何时split文件.以下是Hadoop Community的专家给我的回复: 
"The block size is a meta attribute. If you append tothe file later, it still needs to know when to split further - so it keeps that value as a mere metadata it can use to advise itself on write boundaries." 
```

4 dfs.replication
```
hdfs - general - Block replication = 3 (default value)
hdfs - hdfs.site - dfs.replication.max = 50 (default value)

查看hadoop集群的备份冗余情况 `hadoop fsck /`
Total size: 14866531168 B (Total open files size: 415 B)
Total dirs: 344
Total files: 712
Total symlinks: 0 (Files currently being written: 6)
Total blocks (validated): 758 (avg. block size 19612837 B) (Total open file blocks (not validated): 5)
Minimally replicated blocks: 758 (100.0 %)
Over-replicated blocks: 0 (0.0 %)
Under-replicated blocks: 0 (0.0 %)
Mis-replicated blocks: 0 (0.0 %)
Default replication factor: 1
Average block replication: 3.0
Corrupt blocks: 0
Missing replicas: 0 (0.0 %)
Number of data-nodes: 3
Number of racks: 1
FSCK ended at Wed Mar 30 17:34:10 CST 2016 in 111 milliseconds
可以看见Average block replication 仍是3
需要修改hdfs中文件的备份系数.
修改hdfs文件备份系数:hadoop dfs -setrep [-R] <path> 如果有-R将修改子目录文件的性质.
`hadoop dfs -setrep -w 3 -R /user/hadoop/dir1` 就是把目录下所有文件备份系数设置为3
`sudo -u hdfs hadoop fs -setrep -R 2 /`
如果再fsck时候出错,往往是由于某些文件的备份不正常导致的,可以用hadoop的balancer工具修复
自动负载均衡hadoop文件:hadoop balancer
查看各节点的磁盘占用情况 hadoop dfsadmin -report
```

5 ERROR: org.apache.hadoop.hbase.NotServingRegionException: Region hbase:meta,,1 is not online on xxxxx
```
可能原因1:
zookeeper引起的, 通常这种情况往往是在你正在运行一个进程正在操作hbase数据库的时候, hbase进程被杀掉或hbase服务被停掉所引起的, 如果是hbase自身管理的zookeeper
解决方法1:
可以将hbase的zookeeper目录下的文件全都删除掉, 然后再重启hbase服务就可以了.
解决方法2:
检查一下是否只有master创建了zookeeper目录
注释:
配置zookeeper的的目录为属性hbase.zookeeper.property.dataDir

可能原因2:
数据损坏导致当前数据存放的region无法使用, 使用hadoop fsck检查是否有损坏块
解决方案:
此时使用hadoop fsck 进行分析 就能看到CORRUPT 的storefile路径 hadoop fs -rm 当前storefile
可能原因3:
集群中各节点的时间不一致造成RegionServer启动失败:集群节点和master的时间误差阀值由hbase.master.maxclockskew参数设定的.
hbase-site.xml
```

6 HBase corrupt block
```
`hdfs fsck /` to check the file block data is recoverable or not. it depends hdfs replication.
`hdfs fsck / | egrep -v '^\.+$' | grep -v eplica` to get corrupt file blocks
`hdfs fsck /path/to/corrupt/file -locations -blocks -files` 
`hadoop fs -rm or  hadoop fsck -delete /path/to/file/with/permanently/missing/blocks` to remove corrupt blocks 
or
`hdfs dfs -rm /corrupt_block`
`hbase hbck` to check again

switch to hbase user: su hbase
hbase hbck -details to understand the scope of the problem
hbase hbck -fix to try to recover from region-level inconsistencies
hbase hbck -repair tried to auto-repair, but actually increased number of inconsistencies by 1
hbase hbck -fixMeta -fixAssignments
hbase hbck -repair this time tables got repaired
hbase hbck -details to confirm the fix
At this point, HBase was healthy, added additional region, and de-referenced corrupted files. However, HDFS still had 5 corrupted files. Since they were no longer referenced by HBase, we deleted them:

switch to hdfs user: su hdfs
hdfs fsck / to understand the scope of the problem
hdfs fsck / -delete remove corrupted files only
hdfs fsck / to confirm healthy status

```

7 YARN NodeManager  can't Start
```
Retrying after 1 seconds. Reason: Execution of 'ambari-sudo.sh su yarn -l -s /bin/bash -c 'ls /var/run/hadoop-yarn/yarn/yarn-yarn-nodemanager.pid && ps -p `cat /var/run/hadoop-yarn/yarn/yarn-yarn-nodemanager.pid`'' returned 1. /var/run/hadoop-yarn/yarn/yarn-yarn-nodemanager.pid
  PID TTY          TIME CMD
delete /var/log/hadoop-yarn/nodemanager/recovery-state/[nm-aux-services  yarn-nm-state].
retart yarn nodemanager
```

8 hbase regionserver dump
```
gc.log
2016-05-23T23:07:09.499-0700: 5.432: [GC (Allocation Failure) 5.432: [ParNew: 334336K->22126K(376064K), 0.0469211 secs] 334336K->22126K(2055424K), 0.0470048 secs] [Times: user=0.03 sys=0.01, real=0.05 secs]
hbase-hbase-master-log
2016-05-23 23:09:56,061 WARN  [MASTER_META_SERVER_OPERATIONS-project-lab:16000-1] master.SplitLogManager: returning success without actually splitting and deleting all the log files in path hdfs://project-lab.domain.org:8020/apps/hbase/data/WALs/hyve-hdata2-lab.domain.org,16020,1464070023271-splitting
hbase-hbase-regionserver-.log
2016-05-23 23:09:23,043 INFO  [ReplicationExecutor-0.replicationSource,1-hyve-hdata1-lab.domain.org,16020,1464070024825] regionserver.ReplicationSource: Log hdfs://project-lab.domain.org:8020/apps/hbase/data/oldWALs/hyve-hdata1-lab.domain.org%2C16020%2C1464070024825.default.1464070029141 still exists at hdfs://project-lab.domain.org:8020/apps/hbase/data/WALs/hyve-hdata1-lab.domain.org,16020,1464070024825-splitting/hyve-hdata1-lab.domain.org%2C16020%2C1464070024825.default.1464070029141
2016-05-23 23:09:23,176 WARN  [ReplicationExecutor-0] regionserver.ReplicationSource: Queue size: 3 exceeds value of replication.source.log.queue.warn: 2
2016-05-23 23:09:23,176 WARN  [ReplicationExecutor-0] regionserver.ReplicationSource: Queue size: 4 exceeds value of replication.source.log.queue.warn: 2
2016-05-23 23:09:23,176 WARN  [ReplicationExecutor-0] regionserver.ReplicationSource: Queue size: 5 exceeds value of replication.source.log.queue.warn: 2
2016-05-23 23:09:23,176 WARN  [ReplicationExecutor-0] regionserver.ReplicationSource: Queue size: 6 exceeds value of replication.source.log.queue.warn: 2
```
 
9 hbase master server crash
```
Check hbase-hbase-master-project-cnode1.domain.org.log 
Fix the WARN and FATAL error
[root@project-cnode1 ~]# sudo -u hdfs hadoop fs -ls hdfs://project-cnode1.domain.org:8020/apps/hbase/data
Found 9 items
drwxr-xr-x   - hbase hdfs          0 2016-05-27 13:58 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/.tmp
drwxr-xr-x   - hbase hdfs          0 2016-05-27 13:58 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/MasterProcWALs
drwxr-xr-x   - hbase hdfs          0 2016-05-27 13:50 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/WALs
drwxr-xr-x   - hbase hdfs          0 2016-05-25 21:18 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/archive
drwxr-xr-x   - hbase hdfs          0 2016-04-05 23:22 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/corrupt
drwxr-xr-x   - hbase hdfs          0 2016-04-22 13:45 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/data
-rw-r--r--   3 hbase hdfs         42 2016-04-01 15:48 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/hbase.id
-rw-r--r--   3 hbase hdfs          7 2016-04-01 15:48 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/hbase.version
drwxr-xr-x   - hdfs  hdfs          0 2016-05-27 10:33 hdfs://project-cnode1.domain.org:8020/apps/hbase/data/oldWALs
sudo -u hdfs hadoop fs -chown hbase:hdfs hdfs://project-cnode1.domain.org:8020/apps/hbase/data/oldWALs
then restart hbase-hmaster service
```

10 DataXceiver error processing unknown operation src:
```
https://issues.apache.org/jira/secure/attachment/12745526/HDFS-8738.001.patch
```

11 RegionServers Health Summary Dead RegionServer(s)2 out of 4
```
hbase shell>status
hbase shell>status 'detailed'
hbase shell>status 'simple'

4 live servers
    project-cnode3.domain.org:16020 1465194697532
        requestsPerSecond=0.0, numberOfOnlineRegions=45, usedHeapMB=133, maxHeapMB=1004, numberOfStores=50, numberOfStorefiles=14, storefileUncompressedSizeMB=19585, storefileSizeMB=2557, compressionRatio=0.1306, memstoreSizeMB=0, storefileIndexSizeMB=0, readRequestsCount=0, writeRequestsCount=0, rootIndexSizeKB=156, totalStaticIndexSizeKB=33615, totalStaticBloomSizeKB=8816, totalCompactingKVs=0, currentCompactedKVs=0, compactionProgressPct=NaN, coprocessors=[GroupedAggregateRegionObserver, Indexer, ScanRegionObserver, SecureBulkLoadEndpoint, SequenceRegionObserver, ServerCachingEndpointImpl, UngroupedAggregateRegionObserver]
    project-cnode1.domain.org:16020 1465194413601
        requestsPerSecond=0.0, numberOfOnlineRegions=73, usedHeapMB=216, maxHeapMB=1004, numberOfStores=76, numberOfStorefiles=4, storefileUncompressedSizeMB=13947, storefileSizeMB=1721, compressionRatio=0.1234, memstoreSizeMB=0, storefileIndexSizeMB=0, readRequestsCount=130, writeRequestsCount=0, rootIndexSizeKB=36, totalStaticIndexSizeKB=29184, totalStaticBloomSizeKB=10402, totalCompactingKVs=0, currentCompactedKVs=0, compactionProgressPct=NaN, coprocessors=[GroupedAggregateRegionObserver, Indexer, MetaDataEndpointImpl, MetaDataRegionObserver, ScanRegionObserver, SecureBulkLoadEndpoint, SequenceRegionObserver, ServerCachingEndpointImpl, UngroupedAggregateRegionObserver]
    project-cnode2.domain.org:16020 1465194558180
        requestsPerSecond=0.0, numberOfOnlineRegions=54, usedHeapMB=75, maxHeapMB=1004, numberOfStores=63, numberOfStorefiles=17, storefileUncompressedSizeMB=53389, storefileSizeMB=6532, compressionRatio=0.1223, memstoreSizeMB=0, storefileIndexSizeMB=0, readRequestsCount=1470, writeRequestsCount=193, rootIndexSizeKB=300, totalStaticIndexSizeKB=113830, totalStaticBloomSizeKB=19444, totalCompactingKVs=4857, currentCompactedKVs=4857, compactionProgressPct=1.0, coprocessors=[GroupedAggregateRegionObserver, Indexer, MetaDataEndpointImpl, MultiRowMutationEndpoint, ScanRegionObserver, SecureBulkLoadEndpoint, SequenceRegionObserver, ServerCachingEndpointImpl, UngroupedAggregateRegionObserver]
    cdkdc.domain.org:16020 1465194274253
        requestsPerSecond=0.0, numberOfOnlineRegions=63, usedHeapMB=170, maxHeapMB=1004, numberOfStores=65, numberOfStorefiles=4, storefileUncompressedSizeMB=18523, storefileSizeMB=2186, compressionRatio=0.1180, memstoreSizeMB=0, storefileIndexSizeMB=0, readRequestsCount=0, writeRequestsCount=0, rootIndexSizeKB=51, totalStaticIndexSizeKB=39803, totalStaticBloomSizeKB=6656, totalCompactingKVs=0, currentCompactedKVs=0, compactionProgressPct=NaN, coprocessors=[GroupedAggregateRegionObserver, Indexer, ScanRegionObserver, SecureBulkLoadEndpoint, SequenceRegionObserver, ServerCachingEndpointImpl, UngroupedAggregateRegionObserver]
2 dead servers
    project-cnode2,16020,1459497079870
    project-cnode2,16020,1464071314940
Aggregate load: 0, regions: 235


delete wrong WALs ,   sudo -u hdfs  hadoop fs -ls /apps/hbase/data/WALs, sudo -u hdfs hadoop fs -rm -r /apps/hbase/data/WALs/<wrong dead server>
restart hbase-daemon.sh
```

12 Delete wrong replication 
```
zookeeper-client -server domain2.org:2181
ls /hbase-unsecure/replication/rs/
delete the wrong zookeeper node
```

13 Under Replicated Blocks in 'sudo -u hdfs hdfs dfsadmin -report'
```
su - <$hdfs_user>
bash-4.1$ hdfs fsck / | grep 'Under replicated' | awk -F':' '{print $1}' >> /tmp/under_replicated_files
-bash-4.1$ for hdfsfile in `cat /tmp/under_replicated_files`; do echo "Fixing $hdfsfile :" ; hadoop fs -setrep 3 $hdfsfile; done
```

### Hadoop ports
----------------------
```
1.系统
8080,80 用于tomcat和apache的端口.
22 ssh的端口

2.Web UI
用于访问和监控Hadoop系统运行状态
Daemon	缺省端口	配置参数
HDFS	Namenode	50070	dfs.http.address
Datanodes	50075	dfs.datanode.http.address
Secondarynamenode	50090	dfs.secondary.http.address
Backup/Checkpoint node*	50105	dfs.backup.http.address
MR	Jobracker	50030	mapred.job.tracker.http.address
Tasktrackers	50060	mapred.task.tracker.http.address
HBase	HMaster	60010	hbase.master.info.port
HRegionServer	60030	hbase.regionserver.info.port
* hadoop 0.21以后代替secondarynamenode .

3.内部端口
Daemon	缺省端口	配置参数	协议	用于
Namenode	9000	fs.default.name	IPC: ClientProtocol	Filesystem metadata operations.
Datanode	50010	dfs.datanode.address	Custom Hadoop Xceiver: DataNodeand DFSClient	DFS data transfer
Datanode	50020	dfs.datanode.ipc.address	IPC:InterDatanodeProtocol,ClientDatanodeProtocol
ClientProtocol	Block metadata operations and recovery
Backupnode	50100	dfs.backup.address	同 namenode	HDFS Metadata Operations
Jobtracker	9001	mapred.job.tracker	IPC:JobSubmissionProtocol,InterTrackerProtocol	Job submission, task tracker heartbeats.
Tasktracker	127.0.0.1:0*	mapred.task.tracker.report.address	IPC:TaskUmbilicalProtocol	和 child job 通信
* 绑定到未用本地端口

 4.相关产品端口
产品	服务	缺省端口	参数	范围	协议	说明
HBase 	Master	60000	hbase.master.port	External	TCP	IPC
Master	60010	hbase.master.info.port	External	TCP	HTTP
RegionServer	60020	hbase.regionserver.port	External	TCP	IPC
RegionServer	60030	hbase.regionserver.info.port	External	TCP	HTTP
HQuorumPeer	2181	hbase.zookeeper.property.clientPort	TCP	HBase-managed ZK mode
HQuorumPeer	2888	hbase.zookeeper.peerport	TCP	HBase-managed ZK mode
HQuorumPeer	3888	hbase.zookeeper.leaderport	TCP	HBase-managed ZK mode
REST Service	8080	hbase.rest.port	External	TCP
ThriftServer	9090	Pass -p <port> on CLI	External	TCP
 Avro server	9090	Pass –port <port> on CLI	External	TCP
Hive	Metastore	9083	External	TCP
HiveServer	10000	External	TCP
Sqoop	Metastore	16000	sqoop.metastore.server.port	External	TCP
ZooKeeper 	Server	2181	clientPort	External	TCP	Client port
Server	2888	X in server.N=host:X:Y	Internal	TCP	Peer
Server	3888	Y in server.N=host:X:Y	Internal	TCP	Peer
Server	3181	X in server.N=host:X:Y	Internal	TCP	Peer
Server	4181	Y in server.N=host:X:Y	Internal	TCP	Peer
Hue 	Server	8888	External	TCP
Beeswax Server	8002	Internal
Beeswax Metastore	8003	Internal
Oozie	Oozie Server	11000	OOZIE_HTTP_PORT in oozie-env.sh	External	TCP	HTTP
Oozie Server	11001	OOZIE_ADMIN_PORT in oozie-env.sh	localhost	TCP	Shutdown port

5.YARN(Hadoop 2.0)缺省端口
产品	服务	缺省端口	配置参数	协议
Hadoop YARN 	ResourceManager	8032	yarn.resourcemanager.address	TCP
ResourceManager	8030	yarn.resourcemanager.scheduler.address	TCP
ResourceManager	8031	yarn.resourcemanager.resource-tracker.address	TCP
ResourceManager	8033	yarn.resourcemanager.admin.address	TCP
ResourceManager	8088	yarn.resourcemanager.webapp.address	TCP
NodeManager	8040	yarn.nodemanager.localizer.address	TCP
NodeManager	8042	yarn.nodemanager.webapp.address	TCP
NodeManager	8041	yarn.nodemanager.address	TCP
MapReduce JobHistory Server	10020	mapreduce.jobhistory.address	TCP
MapReduce JobHistory Server	19888	mapreduce.jobhistory.webapp.address	TCP

6.第三方产品端口
ganglia用于监控Hadoop和HBase运行情况.kerberos是一种网络认证协议,相应软件由麻省理工开发.
产品	服务	安全	缺省端口	协议	访问	配置
Ganglia	ganglia-gmond	8649	UDP/TCP	Internal
ganglia-web	80	TCP	External	通过 Apache httpd
Kerberos	KRB5 KDC Server	Secure	88	UDP*|TCP	External	[kdcdefaults] 或 [realms]段下的kdc_ports 和 kdc_tcp_ports
KRB5 Admin Server	Secure	749	TCP	Internal	 Kdc.conf 文件:[realms]段kadmind_
```

### add/remove new server/host for existed cluster
----------------------
ADD OS:Centos7, Ambari
```
1. Get master server ssh private key.
ssh-copy-id -i ~/.ssh/id_rsa.pub root@new_server_FQCN
ssh-keygen in new server and sent the public key to  master server.
2. ntpdate
yum install ntp
vi /etc/ntp.conf and add "server asia.pool.ntp.org iburst"
systemctl enable ntpd && systemctl start ntpd
3. timedatectl
timedatectl set-local-rtc yes
timedatectl list-timezones
timedatectl set-timezone Asia/Shanghai
timedatectl set-ntp yes
4. hostname
vi /etc/hosts
add the others host IP and FQCN in /etc/hosts
add the new server host and FQCN in others server /etc/hosts
vim new server /etc/hostname and modify to FQCN name
5. ulimit
vi /etc/security/limits.conf
add 
*	soft	nofile 102400
*	hard	nofile	102400

6. iptables
setenforce 0
vim /etc/selinux/config change to  SELINUX=disabled
systemctl disable firewalld
service firewalld stop
7. ambari admin page to add new host
8. ambari admin page Assign Slaved and Clients:
choose DataNode, NodeManager, RegionServer, Spark Thrift Server, Client
9. issues
DataNode error. Check hosts
RegionServer crash, Check memory
Zookeeper error,  restart the upgrade for each search.'''
WARN [NIOServerCxn.Factory:0.0.0.0/0.0.0.0:2181:NIOServerCnxn@357] - caught end of stream exception
EndOfStreamException: Unable to read additional data from client sessionid 0x0, likely client has closed socket
at org.apache.zookeeper.server.NIOServerCnxn.doIO(NIOServerCnxn.java:228)
at org.apache.zookeeper.server.NIOServerCnxnFactory.run(NIOServerCnxnFactory.java:208)
at java.lang.Thread.run(Thread.java:745)'''
ln -s /home/hdfs/data /hadoop/hdfs/data
ln -s /home/hdfs/namenode /hadoop/hdfs/namenode
chown hdfs:hadoop data -R
chown hdfs:hadoop namenode -R
Make sure all peer_id will update in others DC server.

10. sudo -u hdfs /bin/hadoop dfsadmin -report
11. sudo -u hdfs hdfs dfsadmin -refreshNodes
sudo -u yarn yarn rmadmin -refreshNodes
sudo -u hdfs hadoop balancer
12. Ambari web->Services->HDFS->Summary-> Service Actions->Rebalance HDFS->Start
./bin/start-balancer.sh -threshold 10
```

Remove
```
1. Ambari web->Hosts->select  one hosts->Host Actions->Delete Host

2. sudo -u hdfs /bin/hadoop dfsadmin -report
sudo -u hdfs hdfs dfsadmin -refreshNodes
sudo -u yarn yarn rmadmin -refreshNodes
sudo -u hdfs hadoop balancer
```


### Performance
--------------------

1. hdfs 
    1. linux filesystem ext4 or XFS
        ext4, 支持大文件,单个最大(16GB~16TB),最大支持1EB(exabyte=1024PB petabyte= 1024^2 TB terabyte)
              目录支持64000个子目录(ext3 32000个) 
            多块分配,延迟分配,journal校验,更快的fsck,可以关闭journaling日志,更快的write,read速度
            
    2. hdfs-site.xml
        (old data lost on power outage)当机房突然掉电时, HBase不仅可能丢失最新更新的数据, 如果刚好又在做Compact,也可能丢失较早之前更新的数据
        dfs.datanode.sync.behind.writes         = true  尽全力把数据块同步到本地硬盘
        dfs.datanode.synconclose                = true

        Datanode会发送block reports给Namenode, 如果10分钟没有报告, DN会被报告为已经死了.
        但是NN会继续从这些DN读和写. 所以需要避免去读写死掉的DN
        def.namenode.avoid.read.stale.datanode         = true
        def.namenode.avoid.write.stale.datanode        = true
        def.namenode.stale.datanode.interval           = 30000 (default, ms)

        HDFS short circuit read, 当RegionServer和DataNode在同一server时, HDFS会直接读取本地的文件块而不通过DN
        dfs.client.read.shortcircuit                   = true
        dfs.client.read.shortcircuit.buffer.size       = 131072 (default KB)
        hbase.regionserver.checksum.verify             = true (default)
        dfs.domain.socket.path

        让DataNode 继续在一些有故障的硬盘上运行
        dfs.datanode.failed.volumes.tolerated          = <N>

        在一个DataNode上分布存储数据在整个硬盘, HDFS-1804 当硬盘上有超过10GB的可用空间时, write数据的命中率会更高.
        dsf.datanode.fsdataset.volumen.choosing.policy = AvailableSpaceVolumeChoosingPolicy

        dfs.block.size             = 268435456 (WAL is rolled at 95% of this)
        ipc.server.tcpnodelay      = true
        ipc.client.tcpnodelay      = true
        dfs.datanode.max.xcievers  = 8192
        dfs.namenode.handler.count = 64
        dfs.datanode.handler.count = 8 (match number of spindles)

2. Hbase 
    1. RegionServer settings, hbase-site.xml
        写缓存在内存->内存把内容以HFiles的形式刷新到磁盘上
        需要限制HFiles, 通过重写小Files 到稍大一些的HFiles
        read requires merging HFiles -> fewer is better  读需要合并HFiles, 越少越好
        write throughput better with fewer compactions -> leads to more files. 写吞吐量减少压缩更好 ->导致更多的文件

        hbase.hstore.blockingStoreFiles      = 10  当超过10个文件后将不允许flush操作, small for read, large for write
        hbase.hstore.compactionThreshold     = 3  当文件数量达到3个时开始压缩, small for read, large for write
        hbase.hregion.memstore.flush.size    = 128 最大内存存储大小, 默认就很好. lart good for fewer compaction ( watch RegionServer heap )

        time based compactions, 基于时间的压缩, 昂贵而且总是在错误的时间
        hbase.hregion.majorcompaction        = 604800000 (week, default)
        hbase.hregion.majorcompaction.jitter = 0.5 (1/2 week, default)

        memstore/Cache sizing
        hbase.hregion.memstore.flush.size             = 128
        hbase.hregion.memstore.block.multiplier       = 2     当一个region里的memstore占用内存大小超过hbase.hregion.memstore.flush.size两倍的大小时, block该region的所有请求,进行flush,释放内存.
            比如hfile.block.cache.size和hbase.regionserver.global.memstore.upperLimit/lowerLimit,以预留更多内存,防止HBase server OOM.
        hbase.regionserver.global.memstore.upperLimit = 0.4 (default)  单个Region内所有的memstore大小总和超过指定值时,flush该region的所有memstore,
        hbase.regionserver.global.memstore.size       = 0.4 (default) 读越大,就减少这个值的百分比
        hfile.block.cache.size                        = 0.4 (default) 用于块缓存百分比

        autotune blockcache vs. Memstore 自动调整块缓存和内存存储
        hbase.regionserver.global.memstore.size.{max|min}.range
        hfile.block.cache.size.{max|min}.range
        hbase.regionserver.heapmemory.tuner.class
        hbase.regionserver.heapmemory.tuner.period

        Data Locality 数据本地化
        hbase.hstore.min.locality.to.skip.major.compact  避免压缩即使是最小的本地存储
        hbase.master.wait.on.regionservers.timeout  = 4.5s (default) 允许主等待一段时间,避免所有的在30~90s登录的region去第一台服务器
        Don't use the HDFS balancer

    2. Column family settings
        block encoding 
            (NONE, FAST_DIFF, PREFIX, etc), scan 友好(解压所有扫描), get不友好.(需要解压需要之前的单元)
            alter 'test', { NAME => 'cf', DATA_BLOCK_ENCODING => 'FAST_DIFF'}
            会产生大量的额外的垃圾 
        compression
            NONE,GZIP,SNAPPY,etc
            create 'test', { NAME => 'CF', COMPRESSION => 'SNAPPY' }
            压缩整个块, 对scan 和 get不友好
