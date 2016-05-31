HIVE
========

1,hive 命令行模式,直接输入/hive/bin/hive的执行程序,或者输入 hive --service cli
       用于linux平台命令行查询,查询语句基本跟mysql查询语句类似
2, hive web界面的 (端口号9999) 启动方式
       hive –service hwi &
用于通过浏览器来访问hive,感觉没多大用途
3, hive 远程服务 (端口号10000) 启动方式
       hive --service hiveserver & 
       或者
       hive --service hiveserver 10000>/dev/null 2>/dev/null &
备注:
       连接Hive JDBC URL:jdbc:hive://192.168.6.116:10000搜索/default     (Hive默认端口:10000  默认数据库名:default)
