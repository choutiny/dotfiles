OpenTSDB
========
OpenTSDB是一个架构在Hbase系统之上的实时监控信息收集和展示平台.它支持秒级数据采集所有metrics,支持永久存储,可以做容量规划,并很容易的接入到现有的报警系统里.OpenTSDB可以从大规模的集群(包括集群中的网络设备,操作系统,应用程序)中获取相应的metrics并进行存储,索引以及服务,从而使得这些数据更容易让人理解,如web化,图形化等.
OpenTSDB是StumbleUpon公司开发出来的.
[OpenTSDB Official](http://opentsdb.net/docs/build/html/index.html)


###Docker
----------------
```
FROM java:7-jdk-alpine

ENV JAVA_HOME=/usr/lib/jvm/java-1.7-openjdk TSDB_VERSION=2.2.0 TSDB_HOME=/opentsdb

RUN apk --update add rsyslog make bash \
	&& apk --update add --virtual builddeps build-base autoconf automake git python openssh

RUN wget -O v${TSDB_VERSION}.zip https://github.com/OpenTSDB/opentsdb/archive/v${TSDB_VERSION}.zip \
	&& unzip v${TSDB_VERSION}.zip \
	&& mv opentsdb-${TSDB_VERSION} ${TSDB_HOME} \
	&& rm -f v${TSDB_VERSION}.zip

WORKDIR $TSDB_HOME

RUN ./build.sh

RUN apk del builddeps \
	&& rm -rf /var/cache/apk/* \
	&& mkdir -p cache /etc/opentsdb

VOLUME ["$TSDB_HOME/cache", "/etc/opentsdb"]

EXPOSE 4242

CMD ["./build/tsdb", "tsd", "--port=4242", "--staticroot=./build/staticroot", "--cachedir=./cache"]
```

###Build
----------------
```
docker build -t private.domain.org:5000/opentsdb ./opentsdb
```

###RUN
----------------
```
docker run -d --restart=always -p 4242:4242 -v /home/softs/opentsdb/opentsdb.conf:/etc/opentsdb.conf --name opentsdb cdkdc.domain.org:5000/opentsdb
docker run -d --rm -p 4242:4242 -v /home/softs/opentsdb/opentsdb.conf:/etc/opentsdb.conf --name opentsdb cdkdc.domain.org:5000/opentsdb
```

###ShortConfig
----------------
need to check hbase shell>zk_dump
```
tsd.storage.hbase.zk_quorum  = hdp.domain.org:2181
tsd.storage.hbase.zk_basedir = /hbase-unsecure
tsd.core.auto_create_metrics = true
tsd.storage.fix_duplicates   = true
tsd.core.meta.enable_realtime_ts = true
```

###OpenTSDB term
----------------
```
metric  监控项, 比如CPU利用率
tags    标签,在OpenTSDB里面,Tags由tagk和tagv组成,即tagk=takv.标签是用来描述Metric的,譬如上面为了标记是服务器A的CpuUsage,tags可为hostname=qatest
tsd     OpenTSDB处理HBase交互的进程. 使用简单的HTTP API接口提供基于HBase的查询服务.
```


###Configuration
----------------
```
tsd.network.port = 4242
tsd.network.bind = 0.0.0.0
tsd.network.tcpnodelay = true
tsd.network.keep_alive = true
tsd.network.reuseaddress = true
tsd.network.worker_threads = 8
tsd.network.async_io = true
tsd.http.staticroot =
tsd.http.cachedir =
tsd.core.auto_create_metrics = false
tsd.storage.enable_compaction = true
tsd.storage.flush_interval = 1000
tsd.storage.hbase.data_table = tsdb
tsd.storage.hbase.uid_table = tsdb-uid
tsd.storage.hbase.zk_basedir = /hbase
tsd.storage.hbase.zk_quorum = localhost
tsd.storage.compaction.flush_interval = 10
tsd.storage.compaction.min_flush_threshold = 100
tsd.storage.compaction.max_concurrent_flushes = 10000
tsd.storage.compaction.flush_speed = 2
```

