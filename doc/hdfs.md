HDFS
=========

###command
---------
bin/hadoop fs -cmd <args> #cmd的命名通常与unix对应的命名名相同,如hadoop fs -ls

1. 添加目录和文件
```
HDFS有一个默认的工作目录 /user/$USER，其中$USER是你的登录用户名。不过目录不会自动建立，
`hadoop fs -mkdir /user/$USER` #mkdir 类似mkdir -p
`hadoop fs -put example.txt` . #会把本地example.txt的文件放到用户目录去, .就是/user/$USER
```
2. 检索文件
```
get命令与put命令相反，它从HDFS复制文件回到本地文件系统。
`hadoop fs -get example.txt`
复制到本地的当前工作目录中。 另一种是显示数据,用cat
`hadoop fs -cat example.txt`
```
3. 删除文件
```
rm命令
`hadoop fs -rm example.txt`
也可以用来删除空目录
```


