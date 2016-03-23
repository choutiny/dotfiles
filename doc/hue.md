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

docker run -it -d --hostname halo-cnode1.domain.org -p 8888:8888 cdkdc.domain.org:5000/hue:latest bash  hue

docker exec -it container_name /bin/bash
ip addr   172.17.0.2
http://172.17.0.2:8888/accounts/login/?next=/
```
