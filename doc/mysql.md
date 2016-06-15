mysql
=========

### install
------------
centos7
```
yum install mysql mysql-devel mariadb-server mariadb 
systemctl enable mariadb
systemctl start mariadb
systemctl stop mariadb
systemctl restart mariadb
```
debian7

### configure
------------
my.cnf
```
[client]
port        = 3306
socket      = /var/run/mysqld/mysqld.sock
default-character-set=utf8

[mysqld_safe]
socket      = /var/run/mysqld/mysqld.sock
nice        = 0

[mysqld]
default-storage-engine=INNODB
character-set-server=utf8
collation-server=utf8_general_ci

user		= mysql
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
port		= 3306
basedir		= /usr
datadir		= /var/lib/mysql
tmpdir		= /tmp
lc-messages-dir	= /usr/share/mysql
skip-external-locking
#bind-address		= 192.168.85.133
bind-address		= 0.0.0.0
key_buffer_size     = 384M
max_allowed_packet	= 16M
thread_stack		= 192K
thread_cache_size       = 8
myisam-recover         = BACKUP
max_connections        = 1000
max_connect_errors = 1000
open_files_limit = 65536
table_cache = 64
#thread_concurrency = 10
query_cache_type = 1
query_cache_limit = 1M
query_cache_size = 64M
general_log_file = /var/log/mysql/mysql.log
#general_log = 1
slow-query-log = 1
log-error = /var/log/mysql/mysql_error.log
long_query_time = 1
#log-queries-not-using-indexes
#server-id = 1
#log_bin = /var/log/mysql/mysql-bin.log
#log_bin = /var/log/mysql/mysql-bin.log
expire_logs_days = 30
#max_binlog_size = 100M
#binlog_do_db = include_database_name
#binlog_ignore_db = include_database_name
# chroot = /var/lib/mysql/
# ssl-ca=/etc/mysql/cacert.pem
# ssl-cert=/etc/mysql/server-cert.pem
# ssl-key=/etc/mysql/server-key.pem

[mysqldump]
quick
quote-names
max_allowed_packet = 1024M

[mysql]
#no-auto-rehash # faster start of mysql but no tab completition
prompt=\\u@\\d \\r:\\m:\\s>

[isamchk]
key_buffer = 384M
sort_buffer_size= 256M
read_buffer = 2M
write_buffer = 2M
[myisamchk]
key_buffer = 384M
sort_buffer_size= 256M
read_buffer = 2M
write_buffer = 2M
!includedir /etc/mysql/conf.d/
```

### privileges
------------
```
mysql>grant all privileges on *.* to root@'%'identified by 'password';
    grant all privileges on *.* to 'root'@'%' identified by 'your_password' with grant option;
    FLUSH PRIVILEGES;
mysql>create user 'username'@'%' identified by 'password';
```


### 58.MYSQL
------------
```
导出指定表 
mysqldump -uroot -p dbname tbname > ./path.sql
    -d = no-data

删除指定数据库的所有表, 但是不删除数据库
    SELECT CONCAT('DROP TABLE IF EXISTS ', table_name, ';') FROM  information_schema.tables WHERE table_schema='wordpress';

导出整个数据库
    mysqldump -u 用户名 -p 数据库名 > 导出的文件名 
    mysqldump -u wcnc -p smgp_apps_wcnc > wcnc.sql
    mysqldump --single-transaction -u wcnc -p smgp_apps_wcnc > xxx.sql
导出一个表
    mysqldump -u 用户名 -p 数据库名 表名> 导出的文件名
    mysqldump -u wcnc -p smgp_apps_wcnc users> wcnc_users.sql
    mysqldump -u user -p database_name table_1 table_2 table_3 > filename.sql
导出一个数据库结构
    mysqldump -u wcnc -p -d --add-drop-table smgp_apps_wcnc >d:\wcnc_db.sql
        -d 不导出数据只导出结构 --add-drop-table 在每个create语句之前增加一个drop table 
导入数据库,常用source 命令
进入mysql数据库控制台,
    mysql -u root -p 
    mysql>use 数据库
    mysql>set names utf8; (先确认编码,如果不设置可能会出现乱码,注意不是UTF-8) 
然后使用source命令,后面参数为脚本文件(如这里用到的.sql)
    mysql>source d:\wcnc_db.sql
上边的实例只是最基础的,有的时候我们可能需要批量导出多个库,我们就可以加上--databases 或者-B,如下语句: 

可以进去mysql后用load infile 来导入txt格式的,需要有自增的id之类的.
格式
    1,xxx,xxx
    2,xxx,xxx
load data infile "/home/www/dbm/bigdb/test.txt" into table `12306_14` fields terminated by ',' lines terminated by '\n';

mysqldump -uroot -p --databases test mysql #空格分隔

还有的时候我们可能需要把数据库内所有的库全部备份,我们就可以使用-all-databases,如下语句: 
mysqldump -uroot -p -all-databases

可能我们还会有更多的需求,下面是我在网上找的感觉比较全的参数说明,贴出来供大家参考.
参数说明 --all-databases , -A 导出全部数据库.
mysqldump -uroot -p --all-databases
--all-tablespaces , -Y

导出全部表空间.mysqldump -uroot -p --all-databases --all-tablespaces

--no-tablespaces , -y 不导出任何表空间信息.
mysqldump -uroot -p --all-databases --no-tablespaces

--add-drop-database 每个数据库创建之前添加drop数据库语句.
mysqldump -uroot -p --all-databases --add-drop-database

--add-drop-table 每个数据表创建之前添加drop数据表语句.(默认为打开状态,使用--skip-add-drop-table取消选项)
mysqldump -uroot -p --all-databases (默认添加drop语句)
mysqldump -uroot -p --all-databases –skip-add-drop-table (取消drop语句)

--add-locks 在每个表导出之前增加LOCK TABLES并且之后UNLOCK TABLE.(默认为打开状态,使用--skip-add-locks取消选项)
mysqldump -uroot -p --all-databases (默认添加LOCK语句)
mysqldump -uroot -p --all-databases –skip-add-locks (取消LOCK语句)

--allow-keywords 允许创建是关键词的列名字.这由表名前缀于每个列名做到.
mysqldump -uroot -p --all-databases --allow-keywords

--apply-slave-statements 在'CHANGE MASTER'前添加'STOP SLAVE',并且在导出的最后添加'START SLAVE'.
mysqldump -uroot -p --all-databases --apply-slave-statements

--character-sets-dir
字符集文件的目录
mysqldump -uroot -p --all-databases --character-sets-dir=/usr/local/mysql/share/mysql/charsets

--comments 附加注释信息.默认为打开,可以用--skip-comments取消

mysqldump -uroot -p --all-databases (默认记录注释)
mysqldump -uroot -p --all-databases --skip-comments (取消注释)

--compatible
导出的数据将和其它数据库或旧版本的MySQL 相兼容.值可以为ansi,mysql323,mysql40,postgresql,oracle,mssql,db2,maxdb,no_key_options,no_tables_options,no_field_options等,
要使用几个值,用逗号将它们隔开.它并不保证能完全兼容,而是尽量兼容.

mysqldump -uroot -p --all-databases --compatible=ansi
--compact
导出更少的输出信息(用于调试).去掉注释和头尾等结构.可以使用选项: --skip-add-drop-table --skip-add-locks --skip-comments --skip-disable-keys
mysqldump -uroot -p --all-databases --compact

--complete-insert, -c
使用完整的insert语句(包含列名称).这么做能提高插入效率,但是可能会受到max_allowed_packet参数的影响而导致插入失败.
mysqldump -uroot -p --all-databases --complete-insert

--compress, -C
在客户端和服务器之间启用压缩传递所有信息
mysqldump -uroot -p --all-databases --compress

--create-options, -a
在CREATE TABLE语句中包括所有MySQL特性选项.(默认为打开状态)
mysqldump -uroot -p --all-databases

--databases, -B
导出几个数据库.参数后面所有名字参量都被看作数据库名.
mysqldump -uroot -p --databases test mysql

--debug
输出debug信息,用于调试.默认值为: d:t:o,/tmp/mysqldump.trace
mysqldump -uroot -p --all-databases --debug
mysqldump -uroot -p --all-databases --debug=" d:t:o,/tmp/debug.trace"

--debug-check
检查内存和打开文件使用说明并退出.
mysqldump -uroot -p --all-databases --debug-check

--debug-info
输出调试信息并退出
mysqldump -uroot -p --all-databases --debug-info

--default-character-set
设置默认字符集,默认值为utf8
mysqldump -uroot -p --all-databases --default-character-set=latin1

--delayed-insert
采用延时插入方式(INSERT DELAYED)导出数据
mysqldump -uroot -p --all-databases --delayed-insert

--delete-master-logs
master备份后删除日志. 这个参数将自动激活--master-data.
mysqldump -uroot -p --all-databases --delete-master-logs

--disable-keys
对于每个表,用/*!40000 ALTER TABLE tbl_name DISABLE KEYS */;和/*!40000 ALTER TABLE tbl_name ENABLE KEYS */;语句引用INSERT语句.这样可以更快地导入dump出来的文件,因为它是在插入所有行后创建索引的.该选项只适合MyISAM表,默认为打开状态.
mysqldump -uroot -p --all-databases

--dump-slave
该选项将导致主的binlog位置和文件名追加到导出数据的文件中.设置为1时,将会以CHANGE MASTER命令输出到数据文件;设置为2时,在命令前增加说明信息.该选项将会打开--lock-all-tables,除非--single-transaction被指定.该选项会自动关闭--lock-tables选项.默认值为0.
mysqldump -uroot -p --all-databases --dump-slave=1
mysqldump -uroot -p --all-databases --dump-slave=2

--events, -E
导出事件.
mysqldump -uroot -p --all-databases --events

--extended-insert, -e
使用具有多个VALUES列的INSERT语法.这样使导出文件更小,并加速导入时的速度.默认为打开状态,使用--skip-extended-insert取消选项.
mysqldump -uroot -p --all-databases
mysqldump -uroot -p --all-databases--skip-extended-insert (取消选项)

--fields-terminated-by
导出文件中忽略给定字段.与--tab选项一起使用,不能用于--databases和--all-databases选项
mysqldump -uroot -p test test --tab="/home/mysql" --fields-terminated-by="#"

--fields-enclosed-by
输出文件中的各个字段用给定字符包裹.与--tab选项一起使用,不能用于--databases和--all-databases选项
mysqldump -uroot -p test test --tab="/home/mysql" --fields-enclosed-by="#"

--fields-optionally-enclosed-by
输出文件中的各个字段用给定字符选择性包裹.与--tab选项一起使用,不能用于--databases和--all-databases选项
mysqldump -uroot -p test test --tab="/home/mysql" --fields-enclosed-by="#" --fields-optionally-enclosed-by ="#"

--fields-escaped-by
输出文件中的各个字段忽略给定字符.与--tab选项一起使用,不能用于--databases和--all-databases选项
mysqldump -uroot -p mysql user --tab="/home/mysql" --fields-escaped-by="#"

--flush-logs
开始导出之前刷新日志.
请注意: 假如一次导出多个数据库(使用选项--databases或者--all-databases),将会逐个数据库刷新日志.除使用--lock-all-tables或者--master-data外.在这种情况下,日志将会被刷新一次,相应的所以表同时被锁定.因此,如果打算同时导出和刷新日志应该使用--lock-all-tables 或者--master-data 和--flush-logs.
mysqldump -uroot -p --all-databases --flush-logs

--flush-privileges
在导出mysql数据库之后,发出一条FLUSH PRIVILEGES 语句.为了正确恢复,该选项应该用于导出mysql数据库和依赖mysql数据库数据的任何时候.
mysqldump -uroot -p --all-databases --flush-privileges

--force
在导出过程中忽略出现的SQL错误.
mysqldump -uroot -p --all-databases --force

--help 显示帮助信息并退出.mysqldump --help

--hex-blob
使用十六进制格式导出二进制字符串字段.如果有二进制数据就必须使用该选项.影响到的字段类型有BINARY,VARBINARY,BLOB.
mysqldump -uroot -p --all-databases --hex-blob

--host, -h
需要导出的主机信息
mysqldump -uroot -p --host=localhost --all-databases

--ignore-table
不导出指定表.指定忽略多个表时,需要重复多次,每次一个表.每个表必须同时指定数据库和表名.例如: --ignore-table=database.table1 --ignore-table=database.table2 ......
mysqldump -uroot -p --host=localhost --all-databases --ignore-table=mysql.user

--include-master-host-port
在--dump-slave产生的'CHANGE MASTER TO..'语句中增加'MASTER_HOST=<host>,MASTER_PORT=<port>' 
mysqldump -uroot -p --host=localhost --all-databases --include-master-host-port

--insert-ignore
在插入行时使用INSERT IGNORE语句.
mysqldump -uroot -p --host=localhost --all-databases --insert-ignore

--lines-terminated-by
输出文件的每行用给定字符串划分.与--tab选项一起使用,不能用于--databases和--all-databases选项.
mysqldump -uroot -p --host=localhost test test --tab="/tmp/mysql" --lines-terminated-by="##"

--lock-all-tables, -x
提交请求锁定所有数据库中的所有表,以保证数据的一致性.这是一个全局读锁,并且自动关闭--single-transaction 和--lock-tables 选项.
mysqldump -uroot -p --host=localhost --all-databases --lock-all-tables

--lock-tables, -l
开始导出前,锁定所有表.用READ LOCAL锁定表以允许MyISAM表并行插入.对于支持事务的表例如InnoDB和BDB,--single-transaction是一个更好的选择,因为它根本不需要锁定表.
请注意当导出多个数据库时,--lock-tables分别为每个数据库锁定表.因此,该选项不能保证导出文件中的表在数据库之间的逻辑一致性.不同数据库表的导出状态可以完全不同.
mysqldump -uroot -p --host=localhost --all-databases --lock-tables

--log-error
附加警告和错误信息到给定文件
mysqldump -uroot -p --host=localhost --all-databases --log-error=/tmp/mysqldump_error_log.err

--master-data
该选项将binlog的位置和文件名追加到输出文件中.如果为1,将会输出CHANGE MASTER 命令;如果为2,输出的CHANGE MASTER命令前添加注释信息.该选项将打开--lock-all-tables 选项,除非--single-transaction也被指定(在这种情况下,全局读锁在开始导出时获得很短的时间;其他内容参考下面的--single-transaction选项).该选项自动关闭--lock-tables选项.
mysqldump -uroot -p --host=localhost --all-databases --master-data=1;
mysqldump -uroot -p --host=localhost --all-databases --master-data=2;

--max_allowed_packet
服务器发送和接受的最大包长度.
mysqldump -uroot -p --host=localhost --all-databases --max_allowed_packet=10240

--net_buffer_length
TCP/IP和socket连接的缓存大小.
mysqldump -uroot -p --host=localhost --all-databases --net_buffer_length=1024

--no-autocommit
使用autocommit/commit 语句包裹表.
mysqldump -uroot -p --host=localhost --all-databases --no-autocommit

--no-create-db, -n
只导出数据,而不添加CREATE DATABASE 语句.
mysqldump -uroot -p --host=localhost --all-databases --no-create-db

--no-create-info, -t
只导出数据,而不添加CREATE TABLE 语句.
mysqldump -uroot -p --host=localhost --all-databases --no-create-info

--no-data, -d
不导出任何数据,只导出数据库表结构.
mysqldump -uroot -p --host=localhost --all-databases --no-data

--no-set-names, -N
等同于--skip-set-charset
mysqldump -uroot -p --host=localhost --all-databases --no-set-names

--opt
等同于--add-drop-table, --add-locks, --create-options, --quick, --extended-insert, --lock-tables, --set-charset, --disable-keys 该选项默认开启, 可以用--skip-opt禁用.
mysqldump -uroot -p --host=localhost --all-databases --opt

--order-by-primary
如果存在主键,或者第一个唯一键,对每个表的记录进行排序.在导出MyISAM表到InnoDB表时有效,但会使得导出工作花费很长时间.
mysqldump -uroot -p --host=localhost --all-databases --order-by-primary

--password, -p
连接数据库密码

--pipe(windows系统可用)
使用命名管道连接mysql
mysqldump -uroot -p --host=localhost --all-databases --pipe

--port, -P
连接数据库端口号

--protocol
使用的连接协议,包括: tcp, socket, pipe, memory.
mysqldump -uroot -p --host=localhost --all-databases --protocol=tcp

--quick, -q
不缓冲查询,直接导出到标准输出.默认为打开状态,使用--skip-quick取消该选项.
mysqldump -uroot -p --host=localhost --all-databases 
mysqldump -uroot -p --host=localhost --all-databases --skip-quick

--quote-names,-Q
使用(`)引起表和列名.默认为打开状态,使用--skip-quote-names取消该选项.
mysqldump -uroot -p --host=localhost --all-databases
mysqldump -uroot -p --host=localhost --all-databases --skip-quote-names

--replace
使用REPLACE INTO 取代INSERT INTO.
mysqldump -uroot -p --host=localhost --all-databases --replace

--result-file, -r
直接输出到指定文件中.该选项应该用在使用回车换行对(\\r\\n)换行的系统上(例如: DOS,Windows).该选项确保只有一行被使用.
mysqldump -uroot -p --host=localhost --all-databases --result-file=/tmp/mysqldump_result_file.txt

--routines, -R
导出存储过程以及自定义函数.
mysqldump -uroot -p --host=localhost --all-databases --routines
经常使用 下面的命令来导出函数,存储过程.
mysqldump -uroot -p -hlocalhost -P3306 -ntd -R dbname > procedure_name.sql
        -n --no-create-db
        -t    --no-data
        -d    --no-create-info
        -R    --routines

--set-charset
添加'SET NAMES default_character_set'到输出文件.默认为打开状态,使用--skip-set-charset关闭选项.
mysqldump -uroot -p --host=localhost --all-databases 
mysqldump -uroot -p --host=localhost --all-databases --skip-set-charset

--single-transaction
该选项在导出数据之前提交一个BEGIN SQL语句,BEGIN 不会阻塞任何应用程序且能保证导出时数据库的一致性状态.它只适用于多版本存储引擎,仅InnoDB.本选项和--lock-tables 选项是互斥的,因为LOCK TABLES 会使任何挂起的事务隐含提交.要想导出大表的话,应结合使用--quick 选项.
mysqldump -uroot -p --host=localhost --all-databases --single-transaction

--dump-date
将导出时间添加到输出文件中.默认为打开状态,使用--skip-dump-date关闭选项.
mysqldump -uroot -p --host=localhost --all-databases
mysqldump -uroot -p --host=localhost --all-databases --skip-dump-date

--skip-opt
禁用–opt选项.
mysqldump -uroot -p --host=localhost --all-databases --skip-opt

--socket,-S
指定连接mysql的socket文件位置,默认路径/tmp/mysql.sock
mysqldump -uroot -p --host=localhost --all-databases --socket=/tmp/mysqld.sock

--tab,-T
为每个表在给定路径创建tab分割的文本文件.注意: 仅仅用于mysqldump和mysqld服务器运行在相同机器上.
mysqldump -uroot -p --host=localhost test test --tab="/home/mysql"

--tables
覆盖--databases (-B)参数,指定需要导出的表名.
mysqldump -uroot -p --host=localhost --databases test --tables test

--triggers
导出触发器.该选项默认启用,用--skip-triggers禁用它.
mysqldump -uroot -p --host=localhost --all-databases --triggers

--tz-utc
在导出顶部设置时区TIME_ZONE='+00:00' ,以保证在不同时区导出的TIMESTAMP 数据或者数据被移动其他时区时的正确性.
mysqldump -uroot -p --host=localhost --all-databases --tz-utc

--user, -u
指定连接的用户名.

--verbose, --v
输出多种平台信息.

--version, -V
输出mysqldump版本信息并退出

--where, -w
只转储给定的WHERE条件选择的记录.请注意如果条件包含命令解释符专用空格或字符,一定要将条件引用起来.
mysqldump -uroot -p --host=localhost --all-databases --where=" user='root'"

--xml, -X
导出XML格式.
mysqldump -uroot -p --host=localhost --all-databases --xml

--plugin_dir
客户端插件的目录,用于兼容不同的插件版本.
mysqldump -uroot -p --host=localhost --all-databases --plugin_dir="/usr/local/lib/plugin"

--default_auth
客户端插件默认使用权限.
mysqldump -uroot -p --host=localhost --all-databases --default-auth="/usr/local/lib/plugin/<PLUGIN>"
```

### 61.mysql usage
------------
```
DDL ----Data Definition Language 数据库定义语言 
如 create procedure之类
创建数据库 CREATE DATABASE [IF NOT EXISTS] DBNAME [CHARACTER SET 'CHAR_NAME'] [COLLATE 'COLL_NAME']
修改:ALTER 删除:DROP
创建一张新表
CRTATE TABLE [IF NOT EXISTS] TBNAME(col_name col_definition,...)
mysql>CREATE TABLE students(Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT UNSIGNED,Name CHAR(20) UNIQUE KEY NOT NULL,Age TINYINT UNSIGNED INDEX,Gender CHAR(1) NOT NULL) [ENGINE={MyISAM | InnoDB }];
也可以这样写(区别在于单独定义主键,唯一键和索引):  
mysql>CREATE TABLE students(Id INT NOT NULL AUTO_INCREMENT UNSIGNED,Name CHAR(20) NOT NULL,Age TINYINT UNSIGNED,Gender CHAR(1) NOT NULL,PRIMARY KEY(id),UNIQUE KEY(name),INDEX(age))
查询出一张表的数据后创建新表(字段定义会丢失,数据会保留)
CREATE TABLE TBNAME SELECT...
EXAMPLE:
mysql>CREATE TABLE test SELECT * FROM students WHERE Id>5;
以一张表的格式定义,创建一张新的空表
CREATE TABLE TBNAME1 LIKE TBNAME2
修改表:
ALTER TABLE tb_name
MODIFY #修改字段定义
CHANGE #可以修改字段名和字段定义
ADD
DROP
EXAMPLE:
给表添加字段 
mysql>ALTER TABLE students ADD (course VARCHAR(100),teacher CHAR(20));
添加惟一键
mysql>ALTER TABLE students ADD UNIQUE KEY Name;
修改字段: 
修改course字段为Course字段,并放在Name字段之后(修改字段需要带上新的字段的定义)ps: MODIFY只能修改字段定义
mysql>ALTER TABLE students CHANGE course Course VARCHAR(100) [AFTER Name];
重命名表名
mysql>ALTER TABLE students RENAME TO stu;
mysql>RENAME TABLE stu TO students;
添加一个外键约束
ALTER TABLE students ADD FOREIGN KEY foreign _cid (CID) REFERENCES course (CID);
创建索引
CREATE INDEX index_name ON TABLE (col_name[(length)] [ASC|DESC]) [USING {BTREE|HASH}];
删除索引
DROP INDEX index_name ON TBNAME;
查看表状态:SHOW STATUS LIKE 'TBNAME';
查看表的索引:SHOW INDEXES FROM TBNAME;
```

```
DML
----Data Manipulation Language 数据操纵语言
如insert,delete,update,select(插入,删除,修改,检索)
插入修改数据

如果每个字段都有值,不需要写字段名称,每组值用,隔开
    mysql>INSERT INTO tb_name (col1,col2) VALUES ('STRING',NUM),('STRING',NUM);
    mysql>INSERT INTO tb_name SET col1='string',col2='string';
    mysql>INSERT INTO tb_name (col1,col2,col3) SELECT...;
    EXAMPLE:
    mysql>INSERT INTO students (Name,Gender,teacher) VALUE ('lujunyi','M','mage'),('wusong','M','zhuima');
    mysql>INSERT INTO students SET Name='lujunyi',Gender='M',tearcher='zhuima';
更新数据
    mysql>UPDATE tb_name SET column=value WHERE column=value;
    mysql>UPDATE students SET Course='mysql' WHERE Name='lujunyi';
替换数据: 
和UPDATE使用方式一样,只要将UPDATE换成REPLACE即可

update table_name set  filed_name= REPLACE(filed_name, 'will replace_string', 'replaced_value')

删除数据
    mysql>DELETE FROM tb_name WHERE conditions;
    mysql>DELETE FROM students WHERE Course='mysql';
清空表: 将会重置计数器
    mysql>TRUNCATE tb_name
查询数据
单表查询: 
    mysql>SELECT [DISTINCT] column FROM tb_name WHERE CONDITION;
EXAMPLE:
基本投影查询
    mysql>SELECT Name,teacher FROM students WHERE Name='wusong';
重复的结果只显示一次
    mysql>SELECT DISTINCT Gender FROM students;
组合条件,可以使用AND,OR,NOT,XOR组合多个条件
    mysql>SELECT * FROM students WHERE Age>20 AND Gender='M';
使用BETWEEN...AND...筛选出年龄介于20-25之间的数据
    mysql>SELECT * FROM students WHERE Age BETWEEN 20 AND 25;
查询Name以Y开头的的数据,%表示任意长度的任意字符,_表示任意单个字符
    mysql>SELECT * FROM student WHERE Name LIKE 'Y%';
使用正则表达式匹配查询,关键词为RLINK或者REGEXP
    mysql> SELECT * FROM students WHERE Name RLINK '^[MNY].*$';
使用IN关键词,将条件限定在一个列表中.用IS关键词,表示条件是否为空(IS NULL 或者 IS NOT NULL)
    mysql>SELECT * FROM students WHERE Age IN (20,22,24);
将查询的结果进行排序
    mysql>SELECT * FROM students ORDER BY Name {ASC|DESC};
查询结果别名显示
    mysql>SELECT Name AS Stu_Name FROM students;
LIMIT限定查询结果的条数,LIMIT 2,3表示偏移2条数据后,取3条数据
    mysql>SELECT * FROM students LIMIT 2;
求平均数:AVG(),最大值:MAX() 最小值MIN() 数量:COUNT() 求和:SUM()
    mysql>SELECT AVG(age) FROM students;
分组GROUP BY
    mysql>SELECT Age, Gender FROM students GROUP BY Gender;
别名:AS
    mysql>SELECT COUNT(Age) AS Num,Age FROM students GROUP BY Age;
过滤:HAVING
    mysql>SELECT COUNT(Age) AS Num,Age FROM students GROUP BY Age HAVING Num>2;
多表查询:
指定已哪个字段连接2张表
    mysql>SELECT students.Name,courses.Cname FROM students,courses WHERE students.CID1 = courses.CID;
连接时指定别名
    mysql>SELECT students.Name,courses.Cname FROM students,courses WHERE students.CID1 = courses.CID;
左外连接...LEFT JION...ON...
    mysql>SELECT s.Name,c.Cname FROM students AS s LEFT JION courses AS c ON s.CID1=c.CID;
右外连接...RIGHT JION...ON...
    mysql>SELECT s.Name,c.Cname FROM students AS s RIGHT JION courses AS c ON s.CID1=c.CID;
子查询
查询年龄大于平均年龄的数据
    mysql>SELECT * FROM students WHERE Age > (SELECT AVG(Age) FROM students);
在FROM中使用子查询
    mysql>SELECT Name,Age FROM (SELECT * FROM students WHERE CID IN (2,3)) AS t WHERE Age>20;
联合查询
    mysql>(SELECT Name,Age FROM students) UNION (SELECT Tname,Age FROM tutors);
创建视图
CREATE VIEW VIEW_NAME AS SELECT....
```

```
DCL
----Data Control Language 数据库控制语言
如grant,deny,revoke等,只有管理员才有这样的权限.
创建用户
mysql>CREATE USER 'USERNAME'@'HOST' IDENTIFIED BY 'PASSWORD'
删除用户
mysql>DROP USER 'USERNAME'@'HOSHOST支持通配符
_:任意单个字符
%:任意多个字符
授权
mysql>GRANT pri1,pri2...ON DB_NAME.TB_NAME TO 'USERNAME'@'HOST' [IDENTIFIED BY 'PASSWORD']
取消授权
mysql>REVOKE pri1,pri2...ON DB_NAME.TB_NAME FROM 'USERNAME'@'HOST';
查看授权
mysql>SHOW GRANTS FOR 'USERNAME'@'HOST';
EXAMPLE:
mysql>CREATE USER 'lujunyi'@'%' IDENTIFIED BY '123456';
mysql>SHOW GRANTS FOR 'lujunyi'@'%';
mysql>GRANT ALL PRIVILEGES ON testdb.* TO 'lujunyi'@'%';

对于centos6,7的远程连接失败问题, 普遍是新装的server
没有root密码的: mysqladmin -uroot password "newpass"
已经有root密码: mysqladmin -uroot password 'oldpasswd' 'newpasswd'
也可以直接登录mysql, mysql -u root;use mysql;UPDATE user SET Password = PASSWORD('newpass') WHERE user = 'root';FLUSH PRIVILEGES;
丢失密码: mysqld_safe --skip-grant-tables& mysql -u root mysql;
 UPDATE user SET password=PASSWORD("new password") WHERE user='root'; FLUSH PRIVILEGES;

给用户授权远程访问, 首先确认端口[client] port=3307 [mysqld] port=3307 其次看mysql是否启动起来, netstat -anp | grep 3307看端口占用
然后grant all privileges on *.* to 'root'@'%' identified by 'your_password' with grant option; FLUSH PRIVILEGES;
防火墙开放3307端口,  iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 3307 -j ACCEPT 
查看规则是否生效, iptables -L -n
删除老的规则iptables -D INPUT -p tcp -m state --state NEW -m tcp --dport 3306 -j ACCEPT
同时防火墙需要保存service iptables save /etc/init.d/iptables save
或者直接修改vi /etc/sysconfig/iptables 加入
-A INPUT -p tcp -m state --state NEW -m tcp --dport 3307 -j ACCEPT
这样就可以远程登录了.



下面列出了您可以使用的 JOIN 类型,以及它们之间的差异.
JOIN: 如果表中有至少一个匹配,则返回行
LEFT JOIN: 即使右表中没有匹配,也从左表返回所有的行
RIGHT JOIN: 即使左表中没有匹配,也从右表返回所有的行
FULL JOIN: 只要其中一个表中存在匹配,就返回行

mysql 备份和ibdata1瘦身
1.备份数据库
/usr/local/mysql/bin/mysqldump -uDBUSER -pPWD --quick --force --routines --add-drop-database
--all-databases --add-drop-table > /data/bkup/mysqldump.sql
2.停止数据库
service mysqld stop
3.删除大文件
rm /usr/local/mysql/var/ibdata1
rm /usr/local/mysql/var/ib_logfile*
rm /usr/local/mysql/var/mysql-bin.index
手动删除除了mysql外的其他数据库文件.然后重启db
service mysqld start
4.还原数据库
/usr/local/mysql/bin/mysql -uroot -pPWD < /data/bkup/mysqldump.sql

5.mysqldump增量备份配置
前提要mysql打开log-bin日志开关.在my.ini or my.cnf 加入
log-bin=/opt/data/mysql-bin
MyISAM
mysqldump --local-all-tables --flush-logs --master-data=2 -u root -p pwd > backup_xxx.sql
InnoDB
将--local-all-tables 替换成--single-transaction
flush-logs 为结束当前日志,生成新日志文件,master-data=2会在输出sql记录后完全备份新日志文件的名称.
输出的备份SQL含有
CHANGE MASTER TO MASTER_LOG_FILE='MySQL-bin.000002',MASTER_LOG_POS=106;

--default-character-set=charset 指定导出数据的字符集
--disabke-keys 告诉mysqldup在insert语句的开头结尾增加/*!40000 ALTER table TABLE disable KEYS */;
和对应的结尾,这能大大提高插入语句的速度,因为它是插入完所有数据后才重建索引的.该选项只适合MyISAM表.
--lock-all-tables ,-x
在开始导出前,提交请求锁定所有数据库的所有表.以保证数据的一致性.这是一个全局读锁,会自动关闭
--single-transaction 和 --lock-tables选项
--lock-tables 锁定当前导出的数据库,只适合MyISAM,如果是InnoDB用--single-transaction
--no-create-info,-t
只导出数据,不添加CREATE TABLE语句
--no-data,-d
不导出数据,只导出数据库表结构
-opt 是快捷选项,包含了--add-drop-tables --add-locking --create-option --disable-keys
--extended-insert --lock-tables --quick -set-charset
等.能让MYSQLDUMP很快导出数据,能很块导回.默认开启,单可以用--skip-opt禁用,如果没有指定--quick
或--opt选项,mysqldump会把整个结果集放在内存中,这样在导出大数据库的时候会出现性能问题.
--quick,-q
在导出大表时有用,强制mysqldump从服务器查询取得记录直接输出而不是取得所有记录后将它们缓存到内存中.
--routines,-R
导出存储过程以及自定义函数
--single-transaction
在导出数据前提交一个BEGIN SQL语句,BEGIN不会阻塞任何应用程序并能保证导出数据库的一致性状态,
它只适用于事务表,比如InnoDB和BDB. 本选项和--lock-tables选项是互斥的. 因为LOCK
TABLES会让任何挂起的事务隐含提交. 要想导出大表的话,应结合使用--quick选项
--triggers
同时导出触发器. 默认启用,可用--skip-triggers禁用
 
myqsl 查询格式化的时间戳为时间 select *, FROM_UNIXTIME(*.TIMESTAMP) as FT FROM xxx_table ;
```

### 65.mysql 优化
------------
```
show variables like 'thread%';
show status like '%connections%';
show status like '%thread%';
```

### 82.mysqldump 转码
------------
```
    Mysql 字符集的修改步骤 
    如果在应用开始阶段没有正确的设置字符集,在运行一段时间以后才发现　存在不能满足要求需要调整,又不想丢弃这段时间的数据,那么就需要进行字符集的修改.　字符集的修改不能直接通过　
    alter dataabase character set *** 或者　alter table tablename character set ***; 命令进行,这两个命令都没有更新已有记录的字符集,　而只是对新创建的表或者记录生效.
    已有的记录的字符集调整,需要先将数据导出,经过适当的调整重新导入后才可完成.
    以下模拟的是将latin1字符集的数据库修改成GBK字符集的数据库的过程.
    1> 导出表结构: 
    mysqldump -uroot -p --default-character-set=gbk -d databasename > createtab.sql
    其中　--default-character-set=gbk 表示设置以什么字符集连接,　-d 表示只导出表结构,不导出数据.
    2>手工修改　createtab.sql 中表结构定义中的字符集为新的字符集.
    3>确保记录不再更新,导出所有记录.
    mysqldump -uroot -p --quick --no-create-info --extended-insert --default-character-set=latin1 databasename > data.sql
    --quick: 该选项用于转储大的表.　它强制　mysqldump 从服务器一次一行地检索表中的行而不是　检索所有行,并在输出前将它缓存到内存中.
    --extended-insert: 使用包括几个　values 列表的多行insert语法,这样使转储文件更小,重载文件时可以加速插入.
    --no-create-info: 不写重新创建每个转储表的create table 语句.
    --default-character-set=latin1: 按照原有的字符集导出所有数据,这样导出的文件中,所有中文都是可见的,不会保存成乱码.
    4>打开data.sql,将　set names latin1 修改成　set names gbk .
    5>使用新的字符集创建新的数据库.
    create database databasename default charset gbk;
    6>创建表,执行　createtab.sql
    mysql -uroot -p databasename < createtab.sql
    7>导入数据,执行data.sql
    mysql -uroot -p databasename < data.sql

    在导入大的csv sql文件时,可以用load data 命令
        use db;
        创建好表,执行
        load data infile '/home/tom/Desktop/tmall_1111/运动鞋服.csv'  into table `product` fields terminated by ',' (band_name,p_name,now_price,mall_price,low_price,1111_price,links,click); 
    mysql -h xxx -u xxx -p -Pxxx --prompt="\\u@\\d \\R:\\m:\\s>"
```

### 110.mysql procedure
-------------
```
创建create procedure sp_name(参数列表)
        BEGIN
        ...
        END
调用call sp_name()
删除drop procedure sp_name
显示show procedure status
show create procedure sp_name

存储过程参数有三种类型:
IN: 输入参数,必须在调用存储过程时指定, 默认未指定类型时则是此类型
    在存储过程中修改该参数的值不能被返回. 为默认值
    CREATE PROCEDURE SP_IN_PARA(IN p_in INT)
        BEGIN
        select p_in;
        set p_in=2;
        select p_in;
        END;

        执行:
        set @p_in=1;
        call SP_IN_PARA(@p_in);
        select @p_in;   输出1
OUT:输出参数,在存储过程内部可以被改变,并且可返回
    CREATE PROCEDURE sp_out_param(OUT p_out INT)
        begin
        select p_out;
        set p_out=2;
        select p_out;
        END;

        执行:
        set @p_out=1;
        call sp_out_param(@p_out); 输出3
        select @p_out;  输出2
INOUT:输入输出参数,IN和OUT结合,调用时指定,并且可被改变和返回
    CREATE PROCEDURE sp_inout_param(INOUT p_inout INT)
        BEGIN
        select p_inout;
        SET p_inout=5;
        select p_inout;
        END;

        set @p_input=3;
        call sp_inout_param(@p_inout); 输出3
        select @p_inout;    输出3
DECLARE var_name,[var_name...] data_type DEFAULT default_value 声明局部变量
    e.g: DECLARE a,b,c INT DEFAULT 5;
SET 对已声明的变量复制或者重新赋值. SET var_name=表达式值[.variable_name=expression...]
SELECT 显示变量, SELECT var into out_var 将变量值写入OUT参数
    e.g: SELECT 'hello world' into @x;
        SELECT @x;
        SET @y='Good bye !';
        SELECT @y;

CREATE TABLE fruits (
  type varchar(10) NOT NULL,
  variety varchar(20) NOT NULL,
  price decimal(5,2) NOT NULL default 0,
  PRIMARY KEY  (type,variety)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

insert into fruits(type, variety, price) values
('apple',  'gala',       2.79),
('apple',  'fuji',       0.24),
('apple',  'limbertwig', 2.87),
('orange', 'valencia',   3.59),
('orange', 'navel',      9.36),
('pear',   'bradford',   6.05),
('pear',   'bartlett',   2.14),
('cherry', 'bing',       2.55),
('cherry', 'chelan',     6.33);

set @type := '', @num := 1;

select type, variety,
   @num := if(@type = type, @num + 1, 1) as row_number,
   @type := type as dummy
from fruits
order by type, variety;

+--------+------------+------------+--------+
| type   | variety    | row_number | dummy  |
+--------+------------+------------+--------+
| apple  | fuji       |          1 | apple  | 
| apple  | gala       |          2 | apple  | 
| apple  | limbertwig |          3 | apple  | 
| cherry | bing       |          1 | cherry | 
| cherry | chelan     |          2 | cherry | 
| orange | navel      |          1 | orange | 
| orange | valencia   |          2 | orange | 
| pear   | bartlett   |          1 | pear   | 
| pear   | bradford   |          2 | pear   | 
+--------+------------+------------+--------+





事件Event 可以定义一些任务调度,首先需要开启事件调度的支持 SET GLOBAL event_scheduler = 1;
创建语法:
    CREATE EVENT [IF NOT EXISTS] <event_name>
    ON SCHEDULE <schedule>
    DO
    <event_body>;
SHOW EVENTS列出所有事件 show events\G;
SHOW CREATE EVENT <event_name>查看一个已存在的事件的信息

注释: -- , # 用于单行注释, /* ...*/ 多行注释
存储过程名字后面的()是必须的.
不能在存储过程参数名称前+@,只能 b int
存储过程的参数不能指定默认值,不能省略参数, 可以用null代替, 不需要在procedure body前加as,
比如mysql存储过程包含多条mysql语句, 需要begin end 关键字
create procedure pr_add(
            a int,
            b int.
            )
            BEGIN
            mysql statement1 ...;
            mysql statement2 ...;
            end;
每条语句的末尾,都要分号;
declare c int;
if a is null then
set a = 0;
end if;
...
end;

DROP procedure if exists selectnum;
DELIMITER //
CREATE PROCEDURE  selectnum(IN num INT)
BEGIN
    select num;
    set num=100;
    select num * 100;
END //
DELIMITER ;

set @a=555;
CALL selectnum(@a);




算术运算符: +,-,*,/,DIV,%
    SET var5=10 DIV 3; 3
    SET var6=10%3;   1
比较运算符, 下面的返回True/False
>,<,<=,>=,BETWEEN,NOT BETWEEN, IN, NOT IN, =, <> !=  , <=>, LIKE, REGEXP, IS NULL, IS NOT NULL
    5 BETWEEN 1 AND 10    True 5 IN (1,2,3,4) False
    2 <> 3 False
    NUll <=> NULL  True 严格比较两个值是否相等
    "Guy Harrison" LIKE "Guy%" True
    "Guy Harrison" REGEXP "[Gg]reg" False 
    0 IS NULL  False
逻辑运算符
位运算符
|或, &与, <<左移位, >>右, ~非(取反)
流程控制:
    分支
        if
        case
    循环
        for循环
        while循环
        loop循环
        repeat until循环
    区块定义
        BEGIN
        ...
        END;
        或者取别名:
        lable1:BEGIN
        ...
        END lable1;
        可以用levae label1; 来跳出区块,执行区块后的代码

函数库,字符串类型,数值类型,日期类型
一,字符串类
CHARSET(str) //返回字串字符集
CONCAT (string2 [,... ]) //连接字串
INSTR (string ,substring ) //返回substring首次在string中出现的位置,不存在返回0
LCASE (string2 ) //转换成小写
LEFT (string2 ,length ) //从string2中的左边起取length个字符
LENGTH (string ) //string长度
LOAD_FILE (file_name ) //从文件读取内容
LOCATE (substring , string [,start_position ] ) 同INSTR,但可指定开始位置
LPAD (string2 ,length ,pad ) //重复用pad加在string开头,直到字串长度为length
LTRIM (string2 ) //去除前端空格
REPEAT (string2 ,count ) //重复count次
REPLACE (str ,search_str ,replace_str ) //在str中用replace_str替换search_str
RPAD (string2 ,length ,pad) //在str后用pad补充,直到长度为length
RTRIM (string2 ) //去除后端空格
STRCMP (string1 ,string2 ) //逐字符比较两字串大小,
SUBSTRING (str , position [,length ]) //从str的position开始,取length个字符,
注: mysql中处理字符串时,默认第一个字符下标为1,即参数position必须大于等于1
mysql> select substring('abcd',0,2);
+-------–+
| substring('abcd',0,2) |
+-------–+
|                       |
+-------–+
1 row in set (0.00 sec)

mysql> select substring('abcd',1,2);
+-------–+
| substring('abcd',1,2) |
+-------–+
| ab                    |
+-------–+
1 row in set (0.02 sec)

TRIM([[BOTH|LEADING|TRAILING] [padding] FROM]string2) //去除指定位置的指定字符
UCASE (string2 ) //转换成大写
RIGHT(string2,length) //取string2最后length个字符
SPACE(count) //生成count个空格

二,数值类型

ABS (number2 ) //绝对值
BIN (decimal_number ) //十进制转二进制
CEILING (number2 ) //向上取整
CONV(number2,from_base,to_base) //进制转换
FLOOR (number2 ) //向下取整
FORMAT (number,decimal_places ) //保留小数位数
HEX (DecimalNumber ) //转十六进制
注: HEX()中可传入字符串,则返回其ASC-11码,如HEX('DEF')返回4142143
也可以传入十进制整数,返回其十六进制编码,如HEX(25)返回19
LEAST (number , number2 [,..]) //求最小值
MOD (numerator ,denominator ) //求余
POWER (number ,power ) //求指数
RAND([seed]) //随机数
ROUND (number [,decimals ]) //四舍五入,decimals为小数位数]

注: 返回类型并非均为整数,如: 

(1)默认变为整形值
mysql> select round(1.23);
+-----+
| round(1.23) |
+-----+
|           1 |
+-----+
1 row in set (0.00 sec)

mysql> select round(1.56);
+-----+
| round(1.56) |
+-----+
|           2 |
+-----+
1 row in set (0.00 sec)

(2)可以设定小数位数,返回浮点型数据

mysql> select round(1.567,2);
+------+
| round(1.567,2) |
+------+
|           1.57 |
+------+
1 row in set (0.00 sec)

SIGN (number2 ) //返回符号,正负或0
SQRT(number2) //开平方

三,日期类型

ADDTIME (date2 ,time_interval ) //将time_interval加到date2
CONVERT_TZ (datetime2 ,fromTZ ,toTZ ) //转换时区
CURRENT_DATE ( ) //当前日期
CURRENT_TIME ( ) //当前时间
CURRENT_TIMESTAMP ( ) //当前时间戳
DATE (datetime ) //返回datetime的日期部分
DATE_ADD (date2 , INTERVAL d_value d_type ) //在date2中加上日期或时间
DATE_FORMAT (datetime ,FormatCodes ) //使用formatcodes格式显示datetime
DATE_SUB (date2 , INTERVAL d_value d_type ) //在date2上减去一个时间
DATEDIFF (date1 ,date2 ) //两个日期差
DAY (date ) //返回日期的天
DAYNAME (date ) //英文星期
DAYOFWEEK (date ) //星期(1-7) ,1为星期天
DAYOFYEAR (date ) //一年中的第几天
EXTRACT (interval_name FROM date ) //从date中提取日期的指定部分
MAKEDATE (year ,day ) //给出年及年中的第几天,生成日期串
MAKETIME (hour ,minute ,second ) //生成时间串
MONTHNAME (date ) //英文月份名
NOW ( ) //当前时间
SEC_TO_TIME (seconds ) //秒数转成时间
STR_TO_DATE (string ,format ) //字串转成时间,以format格式显示
TIMEDIFF (datetime1 ,datetime2 ) //两个时间差
TIME_TO_SEC (time ) //时间转秒数]
WEEK (date_time [,start_of_week ]) //第几周
YEAR (datetime ) //年份
DAYOFMONTH(datetime) //月的第几天
HOUR(datetime) //小时
LAST_DAY(date) //date的月的最后日期
MICROSECOND(datetime) //微秒
MONTH(datetime) //月
MINUTE(datetime) //分

注: 可用在INTERVAL中的类型: DAY ,DAY_HOUR ,DAY_MINUTE ,DAY_SECOND ,HOUR ,HOUR_MINUTE ,HOUR_SECOND ,MINUTE ,MINUTE_SECOND,MONTH ,SECOND ,YEAR
DECLARE variable_name [,variable_name...] datatype [DEFAULT value]; 
其中,datatype为mysql的数据类型,如:INT, FLOAT, DATE, VARCHAR(length)

例: 
DECLARE l_int INT unsigned default 4000000; 
DECLARE l_numeric NUMERIC(8,2) DEFAULT 9.95; 
DECLARE l_date DATE DEFAULT '1999-12-31'; 
DECLARE l_datetime DATETIME DEFAULT '1999-12-31 23:59:59';
DECLARE l_varchar VARCHAR(255) DEFAULT 'This will not be padded';
```

### 105.mysql perfermance
-------------
```
    需要10s,30s,60s这样来计算每个选项的差异值, 然后再计算
    (1)QPS(每秒Query量) 
    QPS = Questions(or Queries) / seconds 
    mysql> show global status like 'Question%';

    (2)TPS(每秒事务量)
    TPS = (Com_commit + Com_rollback) / seconds
    mysql> show global status like 'Com_commit';
    mysql> show global status like 'Com_rollback';

    (3)key Buffer 命中率
    mysql> show global status like 'key%';
    key_buffer_read_hits = (1-key_reads / key_read_requests) * 100%
    key_buffer_write_hits = (1-key_writes / key_write_requests) * 100%

    (4)InnoDB Buffer命中率 
    mysql> show status like 'innodb_buffer_pool_read%';
    innodb_buffer_read_hits = (1 - innodb_buffer_pool_reads / innodb_buffer_pool_read_requests) * 100%

    (5)Query Cache命中率
    mysql> show status like 'Qcache%';
    Query_cache_hits = (Qcahce_hits / (Qcache_hits + Qcache_inserts )) * 100%;

    (6)Table Cache状态量 
    mysql> show global  status like 'open%';
    比较 open_tables  与 opend_tables 值

    (7)Thread Cache 命中率 
    mysql> show global status like 'Thread%'; =
    mysql> show global status like 'Connections';
    Thread_cache_hits = (1 - Threads_created / connections ) * 100%

    (8)锁定状态
    mysql> show global  status like '%lock%';
    Table_locks_waited/Table_locks_immediate=0.3%  如果这个比值比较大的话,说明表锁造成的阻塞比较严重
    Innodb_row_lock_waits innodb行锁,太大可能是间隙锁造成的 

    (9)复制延时量
    mysql > show slave status 
    查看延时时间 

    (10) Tmp Table 状况(临时表状况) 
    mysql > show status like 'Create_tmp%'; 
    Created_tmp_disk_tables/Created_tmp_tables比值最好不要超过10%,如果Created_tmp_tables值比较大, 
    可能是排序句子过多或者是连接句子不够优化 

    (11) Binlog Cache 使用状况 
    mysql > show status like 'Binlog_cache%'; 
    如果Binlog_cache_disk_use值不为0 ,可能需要调大 binlog_cache_size大小 

    (12) Innodb_log_waits 量 
    mysql > show status like 'innodb_log_waits'; 
    Innodb_log_waits值不等于0的话,表明 innodb log  buffer 因为空间不足而等待 

    比如命令:  
    >#show global status; 
    虽然可以使用:  
    >#show global status like %...%; 

    TPS - Transactions Per Second(每秒传输的事物处理个数),即服务器每秒处理的事务数,如果是InnoDB会显示,没有InnoDB就不会显示.
    TPS = (COM_COMMIT + COM_ROLLBACK)/UPTIME

    use information_schema;
    select VARIABLE_VALUE into @num_com from GLOBAL_STATUS where VARIABLE_NAME ='COM_COMMIT';
    select VARIABLE_VALUE into @num_roll from GLOBAL_STATUS where VARIABLE_NAME ='COM_ROLLBACK';
    select VARIABLE_VALUE into @uptime from GLOBAL_STATUS where VARIABLE_NAME ='UPTIME';
    select (@num_com+@num_roll)/@uptime;


    QPS - Queries Per Second(每秒查询处理量)MyISAM 引擎
    QUESTIONS/UPTIME

    use information_schema;
    select VARIABLE_VALUE into @num_queries from GLOBAL_STATUS where VARIABLE_NAME ='QUESTIONS';
    select VARIABLE_VALUE into @uptime from GLOBAL_STATUS where VARIABLE_NAME ='UPTIME';
    select @num_queries/@uptime;



mysql 分组按照时间来统计数据条数
select count(id) from ApprovedComponent  group by  date_format(created, '%Y-%m-%d %H') order by id desc limit 10;
```
