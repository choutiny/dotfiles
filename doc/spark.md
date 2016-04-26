Spark
=========
Spark manual[Spark](http://spark.apache.org/docs/latest/spark-standalone.html)


###spark start master and slave
----------------------
```
master server:
 
cd /usr/hdp/current/spark/sbin
./start-master.sh
 
netstat -tlnp|grep 7077|awk '{print $7}'|awk -F '/' '{print $1}'
14742
ps aux | grep 14742
root 14742 0.7 3.8 4742144 308384 pts/6 Sl 13:47 0:04 /usr/jdk64/jdk1.8.0_60/bin/java -Dhdp.version=2.4.0.0-169 -cp /usr/hdp/2.4.0.0-169/spark/sbin/../conf/:/usr/hdp/2.4.0.0-169/spark/lib/spark-assembly-1.6.0.2.4.0.0-169-hadoop2.7.1.2.4.0.0-169.jar:/usr/hdp/2.4.0.0-169/spark/lib/datanucleus-api-jdo-3.2.6.jar:/usr/hdp/2.4.0.0-169/spark/lib/datanucleus-core-3.2.10.jar:/usr/hdp/2.4.0.0-169/spark/lib/datanucleus-rdbms-3.2.9.jar:/usr/hdp/current/hadoop-client/conf/ -Xms1g -Xmx1g org.apache.spark.deploy.master.Master --ip halo-cnode1.domain.org --port 7077 --webui-port 8080
 
 
 
each slave server:
 
cd /usr/hdp/current/spark-client/sbin
./start-slave.sh spark://halo-cnode1.domain.org:7077

```
