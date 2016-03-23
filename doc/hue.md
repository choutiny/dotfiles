HUE
=========
Hue是cdh专门的一套web管理器，它包括3个部分hue ui，hue server，hue db。hue提供所有的cdh组件的shell界面的接口。你可以在hue编写mr，查看修改hdfs的文件，管理hive的元数据，运行Sqoop，编写Oozie工作流等大量工作。
[HUE Docker](http://gethue.com/getting-started-with-hue-in-2-minutes-with-docker/)

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

-v 
docker run -tid --name hue8888 --hostname halo-cnode1.domain.org -p 8888:8888 -v /usr/hdp:/hdp cdkdc.domain.org:5000/hue:latest ./build/env/bin/hue runserver_plus 0.0.0.0:8888
    -i 标志保证容器中STDIN是开启的. 
    -t表示告诉docker要为创建的容器分配一个伪tty终端
    -d  参数会把容器放到后台运行
    --name alias_name 可以为这个docker指定一个别名, 要放前面, docker run -tid --name alias_name images:version /bin/bash
    --hostname 指定hostname, 类似--ip
    -p docker 容器的端口:外部主机的端口, 作端口映射, 来公开在dockerfile里面定义的expose的所有端口.
    -v 挂在目录, 外部主机目录:容器内部目录

/hue/desktop/conf/pseudo-distributed.in

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
