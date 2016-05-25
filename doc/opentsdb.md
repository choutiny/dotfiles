OpenTSDB
========
OpenTSDB是一个架构在Hbase系统之上的实时监控信息收集和展示平台。它支持秒级数据采集所有metrics，支持永久存储，可以做容量规划，并很容易的接入到现有的报警系统里。OpenTSDB可以从大规模的集群（包括集群中的网络设备、操作系统、应用程序）中获取相应的metrics并进行存储、索引以及服务，从而使得这些数据更容易让人理解，如web化，图形化等.
OpenTSDB是StumbleUpon公司开发出来的.
[OpenTSDB Official](http://opentsdb.net/docs/build/html/index.html)


###Docker
----------------
```
FROM java:7-jdk-alpine

ENV JAVA_HOME=/usr/lib/jvm/java-1.7-openjdk TSDB_VERSION=2.2.0 TSDB_HOME=/opentsdb

RUN apk --update add rsyslog make bash \
	&& apk --update add --virtual builddeps build-base autoconf automake git python

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

EXPOSE 3636

CMD ["./build/tsdb", "tsd", "--port=3636", "--staticroot=./build/staticroot", "--cachedir=./cache"]
```

###Configuration
----------------
```
# --------- NETWORK ----------
# The TCP port TSD should use for communications
# *** REQUIRED ***
tsd.network.port =

# The IPv4 network address to bind to, defaults to all addresses
# tsd.network.bind = 0.0.0.0

# Disable Nagel's algorithm, default is True
#tsd.network.tcpnodelay = true

# Determines whether or not to send keepalive packets to peers, default
# is True
#tsd.network.keep_alive = true

# Determines if the same socket should be used for new connections, default
# is True
#tsd.network.reuseaddress = true

# Number of worker threads dedicated to Netty, defaults to # of CPUs * 2
#tsd.network.worker_threads = 8

# Whether or not to use NIO or tradditional blocking IO, defaults to True
#tsd.network.async_io = true

# ----------- HTTP -----------
# The location of static files for the HTTP GUI interface.
# *** REQUIRED ***
tsd.http.staticroot =

# Where TSD should write it's cache files to
# *** REQUIRED ***
tsd.http.cachedir =

# --------- CORE ----------
# Whether or not to automatically create UIDs for new metric types, default
# is False
#tsd.core.auto_create_metrics = false

# --------- STORAGE ----------
# Whether or not to enable data compaction in HBase, default is True
#tsd.storage.enable_compaction = true

# How often, in milliseconds, to flush the data point queue to storage,
# default is 1,000
# tsd.storage.flush_interval = 1000

# Name of the HBase table where data points are stored, default is "tsdb"
#tsd.storage.hbase.data_table = tsdb

# Name of the HBase table where UID information is stored, default is "tsdb-uid"
#tsd.storage.hbase.uid_table = tsdb-uid

# Path under which the znode for the -ROOT- region is located, default is "/hbase"
#tsd.storage.hbase.zk_basedir = /hbase

# A comma separated list of Zookeeper hosts to connect to, with or without
# port specifiers, default is "localhost"
#tsd.storage.hbase.zk_quorum = localhost

# --------- COMPACTIONS ---------------------------------
# Frequency at which compaction thread wakes up to flush stuff in seconds, default 10
# tsd.storage.compaction.flush_interval = 10

# Minimum rows attempted to compact at once, default 100
# tsd.storage.compaction.min_flush_threshold = 100

# Maximum number of rows, compacted concirrently, default 10000
# tsd.storage.compaction.max_concurrent_flushes = 10000

# Compaction flush speed multiplier, default 2
# tsd.storage.compaction.flush_speed = 2
```
