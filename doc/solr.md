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
mv solr-6.1.0 solr && cd solr-6.1.0
```
others, 可作测试
```
./bin/solr start -p 8983
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
3. Add system service, need java8 ENV support
```
mkdir /solr/data && cd /
./solr/bin/install_solr_service.sh solr-6.1.0.tgz -d /solr/data  -s solr -u solr -i /opt/ -f 
    -d 指定索引数据存放目录, -i 执行solr安装在哪儿, -f 强制替换掉以前的配置
```
4. java8 ENV
[`Download JDK8`](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
```
mkdir /usr/java && cd /usr/java
tar -zxvf jdk8-xxx-linux-x64.tar.gz && mv jdk1.8.0_xx /usr/java/java8
update-alternative --install /usr/bin/java java /usr/java/java8/bin/java 1100
update-alternative --install /usr/bin/javac javac /usr/java/java8/bin/javac 1100
update-alternative --install /usr/bin/jar jar /usr/java/java8/bin/jar 1100
```
Select java8
```
update-alternative --config java
update-alternative --config javac
update-alternative --config jar
```
Add the blow part into `.bashrc` or `.zshrc`
```
export JAVA_HOME=/usr/java/java8
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar
export PATH=$PATH:$JAVA_HOME/bin
```
Run `java -version` to check java version
5. Visit by browser
```
ps aux | grep solr  # to check solr process exist 
/etc/init.d/solr start
ip or domain:8983
```
6. Create solr database, Must be use `solr` user
```
su - solr -c "/opt/solr/bin/solr create -c dbname"
```
e.g.:
```
su - solr -c "/opt/solr/bin/solr create -c tff"
```

### Usage
----------
Selct 'Core Selector' dbname you created on http://192.168.0.19:8394
```
Documents:  add index
Query:      Query
```

### Mysql Support
----------
```
cd /solr/data/data/tff/conf   #tff is the Create solr database dbname.
cp /solr/example/example-DIH/solr/db/conf/admin-extra.html ./
cp /solr/example/example-DIH/solr/db/conf/admin-extra.menu-bottom.html ./
cp /solr/example/example-DIH/solr/db/conf/admin-extra.menu-top.html ./
```
Download mysql-connector-java-5.1.39
```
cd /
http://dev.mysql.com/downloads/file/?id=462849
download mysql-connector-java-5.1.39.tar.gz  and tar -zxvf mysql-connector-java-5.1.39.tar.gz
```
Cp mysql-connector-java-5.1.39-bin.jar into /opt/solr/contrib/dataimporthandler/lib
```
mkdir /opt/solr/contrib/dataimporthandler/lib
cp /mysql-connector-java-5.1.39/mysql-connector-java-*.jar /opt/solr/contrib/dataimporthandler/lib
```
Configure tff/conf/solrconfig.xml
```
vim /solr/data/data/tff/conf/solrconfig.xml
```
Find line `<lib dir="" />` and add the below content under this part, maybe line 93.
```
  <lib dir="${solr.install.dir:../../../..}/contrib/dataimporthandler/lib" regex=".*\.jar" />
  <lib dir="${solr.install.dir:../../../..}/dist/" regex="solr-dataimporthandler-.*\.jar" />
```
Find line `<requestHandler name="/select" class="solr.SearchHandler">...</requestHandler>`, add the blow content above this part.
May be line 750.
```
  <requestHandler name="/dataimport" class="org.apache.solr.handler.dataimport.DataImportHandler">
      <lst name="defaults">
      <str name="config">data-config.xml</str>
      </lst>
  </requestHandler>
```
create new `data-config.xml`
```
touch /solr/data/data/tff/conf/data-config.xml
```
Add the below content into data-config.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<!--# define data source1-->
<dataConfig>
<dataSource name="source1" type="JdbcDataSource"
            driver="com.mysql.jdbc.Driver"
            url="jdbc:mysql://localhost:3306/tff_dbname1"
            user="mysql_username_root"
            password="mysql_passwd_123456"
            batchSize="-1"/>
    <document>
        <entity name="mysql_tablename1" dataSource="source1"
            pk="id"
            query="select id,name from products"
            deltaImportQuery="SELECT id,name from products WHERE id='${dih.delta.id}'"
            deltaQuery="SELECT id FROM products  WHERE updated_at > '${dih.last_index_time}'"
            >
            <field column="id" name="id"/>
            <field column="name" name="name"/>
            <field column="number" name="number"/>
            <field column="update_time" name="update_time"/>
        </entity>
    </document>
</dataConfig>
```
Example keywords
```
dataSource          数据库数据源,可以定义多份
Entity              一张表对应的数据实体.
pk                  主键
query               查询语句
Filed               对应一个字段
column              是数据库里面的column名, 后面的name属性对应solr的Filed的名字.
tff_dbname1         是mysql的数据库名
mysql_tablename1    是mysql的表名
mysql_username_root 是mysql的用户名, 同理passwd是密码
3306                是mysql端口,同理localhost是mysql host地址
deltaQuery          是增量索引,原理是从数据库中根据deltaQuery指定的SQL语句查询出所有需要增量导入的数据的ID号,
                        然后根据deltaImportQuery指定的SQL语句返回所有这些ID的数据,即为这次增量导入所要处理的数据.
    核心思想是:通过内置变量 "${dih.delta.id}" 和 "${dataimporter.last_index_time}" 来记录本次要索引的id和最近一次索引的时间

```
mysql_tablename1 结构
```
id
name
number
update_time
```
vim `/solr/data/data/tff/conf/managed-schema` find `<field name=id` type="int" .../>`
在该行后添加对应的mysql表的字段属性, 保存后重启solr
```
<field name="name" type="string" indexed="true" stored="false"/>
<field name="number" type="int" indexed="true" stored="false"/>
<field name="update_time" type="date" indexed="true" stored="true" />
```
8983页面操作
```
1. 进入:8983 页面后, 在core admin 那里选中刚才创建的tff, 点Reload 重新加载配置
2. 左边点Core selector选中之前的tff
3. 选到Dataimport后, 有full-import(全部索引)和delta-import(增量索引),
   选择增量索引需要把clean的选项去掉, 不然会清除之前的.选full-import的最好把原有的索引文件清空重新索引.
4. 点击execute后执行建立索引, 第一次用full-import, 可以看见tff下的磁盘占用在增大(du -sh /solr/data/data/tff).
5. indexing 的时间随着数据量的增大可能会有点儿长.可以点击 refresh status来查看是否indexing完.
6. 点击Query 在q那里输入要查询的内容, 会显示出搜索结果
```

### 中文分词支持 IKAnalyzer, pending.
----------
http://blog.csdn.net/linzhiqiang0316/article/details/51554217

### Php Support, pending
----------
[SolrInputDocument](http://php.net/manual/en/class.solrinputdocument.php)
[Solrclient](http://php.net/manual/en/class.solrclient.php)
[SolrQuery](http://php.net/manual/en/book.solr.php)

### Php laravel support, pending
----------
https://github.com/FbF/Laravel-Solarium
http://stackoverflow.com/questions/33982781/solr-solarium-connection-with-laravel-5-in-database-php

### 地信数据支持, pending
----------
http://www.cnblogs.com/luxiaoxun/p/4477591.html
http://tech.meituan.com/solr-spatial-search.html
http://item.congci.com/item/apache-lucene-he-solr-diliweizhi-ganzhi-sousuo
https://cwiki.apache.org/confluence/display/solr/Spatial+Search

