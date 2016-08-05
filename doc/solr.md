lucene solr
===========
[solr](http://lucene.apache.org/solr)

### Install
----------
1. [solr6.1.0](http://mirror.bit.edu.cn/apache/lucene/solr/6.1.0)
2. [jdk1.7 or jdk 1.8](java)

```
wget http://mirror.bit.edu.cn/apache/lucene/solr/6.1.0/solr-6.1.0.tgz
tar -zxvf solr-6.1.0.tgz
cd solr-6.1.0
./bin/solr start -p 8984
./bin/solr stop
    -f 前台运行solr并发送stdout, stderr 去solr-PROT-console.log, 默认后台
    -c -cloud, 启动solr以solr云模式, 没有指定-z模式的话, 会启动内置的zookeeper
        端口会是solr端口+1000,
    -h <host>
    -p <port>
    -d <dir> 指定solr 服务器路径
    -m <memory> 设置最小内存-Xms和最大内存-Xmx 为JVM, -Xms4g -Xms4g
    -s <dir> 设置solr.solr.home 系统属性. solr会创建核心目录在这个路径下,
        允许run多个solr实例当用-d 参数.同时需要solr.xml配置文件(除非solr.xml在zookeeper指定了)
    -e <example>
        cloud  solrCloud example
        techproducts 复杂例子
        dih     数据导入处理
        schemaless 少表例子
    -a 扩展参数传递给JVM, 比如设置java debug选项
        -a "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=18983"
    -V 更多输出信息
```

### 中文支持
----------
IKAnalyzer
