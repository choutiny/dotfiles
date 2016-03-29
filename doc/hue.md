HUE
=========
Hue是cdh专门的一套web管理器，它包括3个部分hue ui，hue server，hue db。hue提供所有的cdh组件的shell界面的接口。你可以在hue编写mr，查看修改hdfs的文件，管理hive的元数据，运行Sqoop，编写Oozie工作流等大量工作。

[HUE Docker](http://gethue.com/getting-started-with-hue-in-2-minutes-with-docker/)

Hue是一个开源的Apache Hadoop UI系统，最早是由Cloudera Desktop演化而来，由Cloudera贡献给开源社区，它是基于Python Web框架Django实现的。通过使用Hue我们可以在浏览器端的Web控制台上与Hadoop集群进行交互来分析处理数据，例如操作HDFS上的数据，运行MapReduce Job等等。很早以前就听说过Hue的便利与强大，一直没能亲自尝试使用，下面先通过官网给出的特性，通过翻译原文简单了解一下Hue所支持的功能特性集合：

```
默认基于轻量级sqlite数据库管理会话数据，用户认证和授权，可以自定义为MySQL、Postgresql，以及Oracle
基于文件浏览器（File Browser）访问HDFS
基于Hive编辑器来开发和运行Hive查询
支持基于Solr进行搜索的应用，并提供可视化的数据视图，以及仪表板（Dashboard）
支持基于Impala的应用进行交互式查询
支持Spark编辑器和仪表板（Dashboard）
支持Pig编辑器，并能够提交脚本任务
支持Oozie编辑器，可以通过仪表板提交和监控Workflow、Coordinator和Bundle
支持HBase浏览器，能够可视化数据、查询数据、修改HBase表
支持Metastore浏览器，可以访问Hive的元数据，以及HCatalog
支持Job浏览器，能够访问MapReduce Job（MR1/MR2-YARN）
支持Job设计器，能够创建MapReduce/Streaming/Java Job
支持Sqoop 2编辑器和仪表板（Dashboard）
支持ZooKeeper浏览器和编辑器
支持MySql、PostGresql、Sqlite和Oracle数据库查询编辑器
```

###Docker
----------
```
netstat -anp | grep 8888
docker pull gethue/hue:latest       # >2.0G
docker build --rm -t gethue/hue:latest
docker run -it -d -p 8888:8888 gethue/hue:latest bash
docker run -it -d  --name hue --hostname halo-cnode1.domain.org -p 8888:8888 cdkdc.domain.org:5000/hue:latest bash 
docker exec -it container_name /bin/bash
ip addr   172.17.0.2
./build/env/bin/hue runserver_plus 0.0.0.0:8888

docker run -tid --name hue8888 --hostname halo-cnode1.domain.org -p 8888:8888 cdkdc.domain.org:5000/hue:latest ./build/env/bin/hue runserver_plus 0.0.0.0:8888
http://172.17.0.2:8888/accounts/login/?next=/
http://halo-cnode1.domain.org:8888

运行image
```
docker run -tid --name hue8888 --hostname cnode1.domain.org -p 8888:8888 -v /usr/hdp:/usr/hdp -v /etc/hadoop:/etc/hadoop -v /etc/hive:/etc/hive -v /etc/hbase:/etc/hbase -v /docker-config/pseudo-distributed.ini:/hue/desktop/conf/pseudo-distributed.ini  c-docker.domain.org:5000/hue:latest ./build/env/bin/hue runserver_plus 0.0.0.0:8888
```
解释下上面的命令,
    -i 标志保证容器中STDIN是开启的
    -t 表示告诉docker要为创建的容器分配一个伪tty终端
    -d 会把容器放到后台运行
    --name alias_name 可以为这个docker指定一个别名, 要放前面, e.g.:docker run -tid --name alias_name images:version /bin/bash
    --hostname 指定hostname, 类似--ip
    -p docker 容器的端口:外部主机的端口, 作端口映射, 来公开在dockerfile里面定义的expose的所有端口.
    -v 挂在目录, 外部主机目录:容器内部目录, 这里我挂在了 ambari的 hadoop配置文件/etc/hadoop, hive配置路径/etc/hive, hbase配置路径/etc/hbase
    最后是要启动容器后要运行的命令 ./build/env/bin/hue runserver_plus 0.0.0.0:8888
    cnode1.domain.org 是我的一台服务器的域名. 拿来跑hue的
    c-docker.domain.org 是我的私有docker仓库. 注意这里需要在docker daemon里面加上 --insecure-registry c-docker.domain.org:5000来允许不安全的授权拉取

修改相关参数后, docker restart hue8888 
```

###配置hue
-----------
hue-docker的相关配置文件在/hue/desktop/conf/pseudo-distributed.ini
修改相关参数
```
http_port=8888
fs_defaultfs=hdfs://halo-cnode1.domain.org:8020
logical_name=halo-cnode1.domain.org
webhdfs_url=http://halo-cnode1.domain.org:50070/webhdfs/v1
hadoop_conf_dir=/etc/hadoop/conf

hive_server_host=halo-cnode2.domain.org
hive_server_port=10000
hive_conf_dir=/etc/hive/conf

hbase_clusters=(cluster1|halo-cnode2.domain.org:9090)
hbase_conf_dir=/etc/hbase/conf
    [[[mysql]]]
      nice_name="Hyve-ENG UAT MySQL"
      name=mysqldbname
      engine=mysql
      host=192.168.85.116
      port=3306
      user=tommy
      password=p12391kfjkew

    [[[mysql2]]]
      nice_name="Hyve-ENG UAT MySQL"
      name=mysqldbname2
      engine=mysql
      host=192.168.85.116
      port=3306
      user=tommy
      password=p12391kfjkew
      options={ "init_command":"SET NAMES 'utf8'"}

```

scp pseudo-distributed.ini to cnode1 /docker-config/
注意上面的地址 hbase_clusters 的cluster1只是hue里面显示的, 可以随便命名, cnode2.domain.org:9090 是hbase thrift 1的地址, 在ambari的主机里面用如下命令启动起来
```
/usr/hdp/2.4.0.0-169/hbase/bin/hbase-daemon.sh start thrift
```

相关配置段
```
Hue配置段	Hue配置项	Hue配置值	说明
desktop	default_hdfs_superuser	hadoop	HDFS管理用户
desktop	http_host	192.168.85.109	Hue Web Server所在主机/IP
desktop	http_port	8888	Hue Web Server服务端口
desktop	server_user	hadoop	运行Hue Web Server的进程用户
desktop	server_group	hadoop	运行Hue Web Server的进程用户组
desktop	default_user	admin	Hue管理员
hadoop/hdfs_clusters	fs_defaultfs	hdfs://hadoop6:8020	对应core-site.xml配置项fs.defaultFS
hadoop/hdfs_clusters	hadoop_conf_dir	/usr/local/hadoop/etc/hadoop	Hadoop配置文件目录
hadoop/yarn_clusters	resourcemanager_host	hadoop6	对应yarn-site.xml配置项yarn.resourcemanager.hostname
hadoop/yarn_clusters	resourcemanager_port	8032	ResourceManager服务端口号
hadoop/yarn_clusters	resourcemanager_api_url	http://hadoop6:8088	对应于yarn-site.xml配置项yarn.resourcemanager.webapp.address
hadoop/yarn_clusters	proxy_api_url	http://hadoop6:8888	对应yarn-site.xml配置项yarn.web-proxy.address
hadoop/yarn_clusters	history_server_api_url	http://hadoo6:19888	对应mapred-site.xml配置项mapreduce.jobhistory.webapp.address
beeswax	hive_server_host	192.168.85.119	Hive所在节点主机名/IP
beeswax	hive_server_port	10000	HiveServer2服务端口号
beeswax	hive_conf_dir	/usr/local/hive/conf	Hive配置文件目录
```
kerberos for HUE
```
addprinc -randkey hue/hue.server.fully.qualified.domain.name@DOMAIN.ORG
kadmin.local -q "xst -norandkey -k hue.keytab hue/fully.qualified.domain.name host/fully.qualified.domain.name"
kinit -k -t ./hue.keytab hue/halo-cnode1.domain.org@DOMAIN.ORG
klist -ket ./hue.keytab
vim /etc/hue/hue.ini
Replace the kinit_path value, /usr/kerberos/bin/kinit

 [[kerberos]]
 # Path to Hue's Kerberos keytab file
 hue_keytab=/etc/hue/hue.keytab
 # Kerberos principal name for Hue
 hue_principal=hue/FQDN@REALM
 # add kinit path for non root users
 kinit_path=/usr/kerberos/bin/kinit
```

###参考
-----------
* [HUE offiical site](http://gethue.com/getting-started-with-hue-in-2-minutes-with-docker/)
* [高可用Hadoop平台－Hue In Hadoop](http://www.cnblogs.com/smartloli/p/4527168.html)
