mapreduce
===========
Mapreduce是一个计算框架,既然是做计算的框架,那么表现形式就是有个输入(input),mapreduce操作这个输入(input),通过本身定义好的计算模型,得到一个输出(output),这个输出就是我们所需要的结果. 
在运行一个mapreduce计算任务时候,任务过程被分为两个阶段:map阶段和reduce阶段,每个阶段都是用键值对(key/value)作为输入(input)和输出(output). 而程序员要做的就是定义好这两个阶段的函数:map函数和reduce函数. 

### flow
--------------
input -> splitting -> mapping -> shuffling -> reducing -> final result

### Concept
--------------
1. 客户端(client): 编写mapreduce程序,配置作业,提交作业,这就是程序员完成的工作;
    首先用户程序 (JobClient) 提交了一个 job, job 的信息会发送到 Job Tracker 中, Job Tracker 是 Map-reduce 框架的中心, 他需要与集群中的机器定时通信 (heartbeat), 需要管理哪些程序应该跑在哪些机器上, 需要管理所有 job 失败、重启等操作.
2. JobTracker:初始化作业,分配作业,与TaskTracker通信,协调整个作业的执行;
3. TaskTracker:保持与JobTracker的通信,在分配的数据片段上执行Map或Reduce任务,TaskTracker和JobTracker的不同有个很重要的方面, 就是在执行任务时候TaskTracker可以有n多个jobtracker, TasTracker是 Map-reduce 集群中每台机器都有的一个部分, 他做的事情主要是监视自己所在机器的资源情况.
4. JobTracker则只会有一个(JobTracker只能有一个就和hdfs里namenode一样存在单点故障,我会在后面的mapreduce的相关问题里讲到这个问题的)
5. Hdfs:保存作业的数据、配置信息等等,最后的结果也是保存在hdfs上面


### Jobtracer
--------------
用户可以通过配置一些参数，以便JobTracker重启后，让所有作业恢复运行。用户配置若干参数后，JobTracker重启前，会在history log中记录各个作业的运行状态，这样在JobTracker关闭后，系统中所有数据目录（包括各种临时目录）均会被保留，待JobTracker重启之后，JobTracker自动重新提交这些作业，并只对未运行完成的task进行重新调度，这样可避免已经计算完的task重新计算。
TaskTracker重启后，它上面的作业也可以自动恢复

### TaskTracker
--------------
1. 汇报心跳
mapred.tasktracker.expiry.interval，默认值是10min
当TaskTracker超过mapred.tasktracker.expiry.interval时间间隔没有向JobTracker汇报心跳，则JobTracker视之为死亡，并将之从调度池中剔除。
2. Exclude nodes
用户可以在mapred.hosts.exclude或者mapred.hosts中指定一个文件，该文件一行是一个tasktracker host，表示这些节点不允许接入集群，也就是不会被分配task。该文件在Hadoop-0.21.0版本中可以动态加载。
3. 黑名单（blacklist）
health-check script脚本判断该节点是健康，不健康，直接加入黑名单。
具体参考： http://hadoop.apache.org/common/docs/current/cluster_setup.html 中的“Configuring the Node Health Check Script”一节。
4. 灰名单（graylist）
采用了启发式算法发现的有问题的节点，加入灰名单。
mapred.jobtracker.blacklist.fault-timeout-window：默认是3小时，时间窗口，计算该时间内失败的task个数
如果满足以下条件，则将tasktracker加入灰名单：
mapred.max.tracker.blacklists：默认是4，bad tasktracker阈值，当一个tasktracker在时间窗口内失败个数超过该阈值，则认为该tasktracker是bad tasktracker
mapred.cluster.average.blacklist.threshold，默认是0.5，如果一个bad tasktracker失败的task个数超过了所有tasktracker平均值的mapred.cluster.average.blacklist.threshold倍，则加入灰名单，不仅会自动加入黑名单。
重新启动该TaskTracker，就能够将它从黑名单和灰名单中删除。

### JOB
--------------
mapred.max.tracker.failures：一个作业在某个tasktracker上失败的task个数超过该值，则该tasktracker被加到该job的blacklist中，从此不再往该tasktracker分配该job的task.

### Task
--------------
mapred.map.max.attempts：每个map task最大尝试次数
mapred.reduce.max.attempts：每个reduce task最大尝试次数

### Record
--------------
mapred.skip.map.max.skip.records：跳过坏记录条数（数据格式不对，空纪录等）。当遇到坏记录时，Hadoop尝试跳过的最多记录条数。

### 磁盘
--------------
用户可以配在mapred.local.dir参数配置多个磁盘目录，将map task中间结果分不到不同磁盘上，增强容错性。Map task临时结果将被轮询写到这些目录中，以避免某个磁盘目录数据过多。（轮询的方式仍然可能导致某个磁盘目录数据过多，最好的策略是每次选择数据最少的磁盘目录写入，采用小顶堆）。
用户日志userlogs可被分布不到不同磁盘目录中，减少单个磁盘日志写入压力。
具体参考：https://issues.apache.org/jira/browse/MAPREDUCE-2657
