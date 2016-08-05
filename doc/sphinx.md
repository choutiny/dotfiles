sphinx & coreseek
==========
1. [sphinx official](http://sphinxsearch.com/)
2. [Coreseek](http://coreseek.cn/)包含
    1. csft-4.1, CSFT(coreseek fulltext search server), 实际就是sphinx-2.1
    2. mmseg-3.2.14, 中文分词算法<br />
3. [solr](http://lucene.apache.org/solr)

### Install
-----------
mysql && mysqlclient-dev package
```
apt-get install mysql-server libmysqlclient-dev
apt-get install sphinxsearch
```

configuration
```
tar -zxvf sphinx-2.1.3.tar.gz 
./configure --prefix=/usr/local/sphinx -with-mysql=/usr/local/mysql
```

coreseek
```
tar -zxvf coreseek-4.1-beta.tar.gz
```
1. 检测系统语言环境, 确保能支持中文显示
```
#locale
LANG=zh_CN.UTF-8
LC_ALL="zh_CN.UTF-8"
cat testpack/var/test/test.xml
```
2. install mmseg3
```
cd mmseg3
./bootstrap
./configure --prefix=/usr/local/mmseg3
make && make install
```
3. 测试
```
/usr/local/mmseg3/bin/mmseg -d /usr/local/mmseg3/etc src/t1.txt
```
4. coreseek
```
cd csft-4.1
apt-get install autoconf-archive
sh buidconf.sh

如果失败, 检查automake 等命令, 需要用automake 1.4切到automake 1.1
curl -O -L http://mirrors.kernel.org/gnu/automake/automake-1.11.tar.gz
tar -zxvf automake-1.11.tar.gz
cd automake-1.11
./configure --prefix=/usr/local
make && make install
update-alternatives --install /usr/bin/automake automake /home/work/develop/automake-1.1/automake 40
update-alternatives --config automake

./configure --prefix=/usr/local/coreseek --without-python --without-unixodbc --with-mmseg
--with-mmseg-includes=/usr/local/mmseg3/include/mmseg/ --with-mmseg-libs=/usr/local/mmseg3/lib/ --with-mysql

注意mysql的路径, 需要mysql.h的头文件所在目录. 一般是/usr/local/mysql/include
libmysqlclient.a一般在/usr/local/mysql/lib
--with-mysql-includes=/usr/local/mysql/include --with-mysql-libs=/usr/local/mysql/lib
make && make install

make && make install

/usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/sphinx-min.conf.dist
```

5. coreseek 中文检索测试
```
cd testpack
/usr/local/coreseek/bin/indexer -c etc/csft.conf --all
##正常索引全部数据 （csft-4.0版类似）
/usr/local/coreseek/bin/search -c etc/csft.conf -a 服务
##以下为正常测试搜索关键词"服务"的数据
/usr/local/coreseek/bin/searchd -c etc/csft.conf
##以下为正常开启搜索服务时的提示信息（csft-4.0版类似）
##如要停止搜索服务, /usr/local/coreseek/bin/searchd -c etc/csft.conf --stop
##如要已启动服务, 要更新索引, /usr/local/coreseek/bin/indexer -c etc/csft.conf --all --rotate
```
