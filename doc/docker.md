Dodcker manual
==============

###Install on different system
-----------
1, Docker hosts

```
54.234.135.251  get.docker.io
54.234.135.251  cdn-registry-1.docker.io
```
2, Debian8

```
deb http://http.debian.net/debian jessie-backports main
apt-get purge docker.io
usermod -aG docker your_username #有docker 的用户组, 为了避免使用sudo, 需要把当前用户加入到docker组,
apt-get install apt-transport-https ca-certificates
apt-get update
vim /etc/apt/sources.list
    deb https://apt.dockerproject.org/repo debian-jessie main
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

apt-get update
apt-get install docker-engine

remove docker
apt-get purge docker-io
    or
apt-get autoremove --purge docker-io
rm -rf /var/lib/docker
```
3, Centos7
```
yum install docker
systemctl start docker
systemctl enable docker
```

###Verify Installation
-----------
```
docker version
Client version: 1.6.2
Client API version: 1.18
Go version (client): go1.3.3
Git commit (client): 7c8fca2
OS/Arch (client): linux/amd64
Server version: 1.6.2
Server API version: 1.18
Go version (server): go1.3.3
Git commit (server): 7c8fca2
OS/Arch (server): linux/amd64
```

###Docs
-----------
```
docker info
docker search xxxx 搜索相关的官方docker镜像(index.docker.io)
docker pull xxxx 下载相关的镜像,    用户名/镜像名, 
                (根据 /var/lib/docker/repositories-aufs 存储在/var/lib/docker/graph/
                 /var/lib/docker/aufs/diff 里面存在的镜像)
    e.g. docker run user/project_image command 
docker run xxxx echo "hello world"  运行xxxx镜像, 并且在镜像中运行echo 命令

docker 无法实现交互模式, 也就是比如apt-get install xxx 需要增加-y 参数默认
    当你对某一个容器做了修改之后（通过在容器中运行某一个命令），可以把对容器的修改保存下来，
    这样下次可以从保存后的最新状态运行该容器。
    docker中保存状态的过程称之为committing，它保存的新旧状态之间的区别，从而产生一个新的版本。

    首先使用docker ps -l命令获得安装完ping命令之后容器的id。然后把这个镜像保存为learn/ping。
docker ps -l
    CONTAINER ID        IMAGE                   COMMAND                CREATED             STATUS                     PORTS               NAMES
    66a36c7e1bfc        learn/tutorial:latest   "apt-get install -y    8 minutes ago       Exited (0) 8 minutes ago                       nostalgic_euclid 

运行docker commit，可以查看该命令的参数列表。
2. 你需要指定要提交保存容器的ID。(译者按：通过docker ps -l 命令获得)
3. 无需拷贝完整的id，通常来讲最开始的三至四个字母即可区分。（译者按：非常类似git里面的版本号)

docker commit 66a learn/ping
    执行完docker commit命令之后，会返回新版本镜像的id号。

一定要使用新的镜像名learn/ping来运行ping命令。(译者按：最开始下载的learn/tutorial镜像中是没有ping命令的)

docker run learn/tutorial ping www.baidu.com
    exec: "ping": executable file not found in $PATH
    FATA[0000] Error response from daemon: Cannot start container 23af03a7c2e1692b0474437d16165390735cc29ba49734261902de8ba7d6d030: [8] System error: exec: "ping": executable file not found in $PATH 

docker run learn/ping ping www.baidu.com
    PING www.a.shifen.com (220.181.112.244) 56(84) bytes of data.
    64 bytes from 220.181.112.244: icmp_req=1 ttl=53 time=38.1 ms
    64 bytes from 220.181.112.244: icmp_req=2 ttl=53 time=37.5 ms
    64 bytes from 220.181.112.244: icmp_req=3 ttl=53 time=38.0 ms

    使用docker ps命令可以查看所有正在运行中的容器列表，
docker ps -l

    使用docker inspect命令我们可以查看更详细的关于某一个容器的信息。
docker inspect 20f66
docker inspect 20f66 -f
docker inspect --format='{{.State.Running }}' 20f66 来限定输出

    1. docker images命令可以列出所有安装过的镜像。
    2. docker push命令可以将某一个镜像发布到官方网站。
    3. 你只能将镜像发布到自己的空间下面。这个模拟器登录的是learn帐号。

docker run -i -t user/project /bin/bash 进入docker的交互式shell
    -i 标志保证容器中STDIN是开启的. -t表示告诉docker要为创建的容器分配一个伪tty终端
    --name alias_name 可以为这个docker指定一个别名, 要放前面, docker run -tid --name alias_name images:version /bin/bash
docker rm alias_name 来删除同名容器
    #exit 退出该docker

docker start alias_name 来启动指定的docker容器, restart来重启
    也可以使用attach来重连该docker容器 
docker start 23af03a
    Error response from daemon: Cannot start container 23af03a: [8] System error: exec: "ping": executable file not found in $PATH
    FATA[0000] Error: failed to start one or more containers 
docker start 10ae45
    10ae45
docker attach 10ae45
    64 bytes from 220.181.112.244: icmp_req=9 ttl=53 time=38.4 ms
    64 bytes from 220.181.112.244: icmp_req=10 ttl=53 time=37.5 ms
    64 bytes from 220.181.112.244: icmp_req=11 ttl=53 time=38.1 ms
    64 bytes from 220.181.112.244: icmp_req=12 ttl=53 time=37.6 ms
    ^C
    --- www.a.shifen.com ping statistics ---
    12 packets transmitted, 12 received, 0% packet loss, time 11013ms
    rtt min/avg/max/mdev = 37.561/38.483/44.528/1.886 ms


进入docker伪tty后, 可以像正常操作linux一样操作docker

docker ps -a 列出所有docker容器.


    创建守护式容器(deamonized container) 而不是(交互式运行容器)interactive container
docker run --name daemon_dave -d ubuntu /bin/sh -c "while true;do echo hello world; sleep 1; done"
    -d  参数会把容器放到后台运行

docker logs daemon_dave 来查看日志
docker logs -f daemon_dave 类似tail -f
docker logs --tail 10 daemon_dave 获取日志的最后10行
docker logs --tail 0 -f daemon_dave 来跟踪某个容器的最新日志.
docker top daemon_dave  查看容器内部运行的进程

在容器内部运行进程
docker exec -d daemon_dave touch /etc/new_config_file 
docker exec -t -i daemon_dave /bin/bash

docker exec -i -t nginx8888 less /var/log/nginx/error.log
docer exec -ti nginx8888 cat /var/log/error.log

停止守护式容器
docker stop daemon_dave

查看最后x个容器
docker ps -n x

自动重启容器, always/on-failure:5 可选的重启次数,on-failure只有当容器的退出代码为非0值的时候才会自动重启, 可以接数字来限定重启次数
docker run --restart=always --name daemon_dave -d ubuntu /bin/sh -c "while true;do echo hello world; sleep 1; done"
    --restart=always    适用需要升级docker,获取宿主机等导致的容器退出
    --restart=on-failure
    --restart=on-failure:2

docker rm `docker ps -a -q` 一次性删除所有容器

docker run -t -i --name new_container ubuntu:12.04 /bin/bash 通过指定版本号来拉取指定的镜像

创建docker hub帐号
https://hub.docker.com/account/signup
测试帐号
docker login
    Username:xxxxx
    Password: 
    Email: xxxx@gmail.com
    WARNING: login credentials saved in /root/.dockercfg.
    Login Succeede

对镜像作了修改后, 可以commit, 比如安装软件
docker commit 3aab3ce  user_name/project

docker commit dffb66497 rainysia/learn
    b7f12b9b4b29a0d18ccb8e2490aa0fb4eece919ddfe59a712171a90ac963938c

docker commit -m="A new custom image for test base on ubuntu12.04" --author="rainysia" dffb66497 rainysia/learn:test
    最后一个是test是tag,类似alias_name别名
查看该镜像的详细
docker inspect rainysia/learn:test    

运用dockerfile来构建镜像
dockerfile
----------------------------
# Version: 0.0.1
FROM debian                      # FROM来指定一个已经存在的镜像, 后续指令都是基于这个镜像
MAINTAINER rainysia "rainysia@gmail.com"
RUN apt-get update                          # run指定会默认shell用/bin/sh -c来执行.如果不希望或者不支持shell平台.可以用exec方式   RUN ["apt-get", " install", "-y", "nginx"]
RUN apt-get install -y nginx
RUN echo 'Hi, i am in your container' \
        > /usr/share/nginx/html/index.html
EXPOSE 80                                   #指定打开80端口
----------------------------
执行docker build来build一个镜像
$sudo docker build -t="rainysia/static_web" ./

------------------------------------------------
docker build -t="rainysia/static_web" .
Sending build context to Docker daemon 2.048 kB
Sending build context to Docker daemon 
Step 0 : FROM learn/ping:latest
 ---> 9e8823ddedf9
Step 1 : MAINTAINER rainysia "rainysia@gmail.com"
 ---> Running in 5e6fc8254653
 ---> 3077170bae60
Removing intermediate container 5e6fc8254653
Step 2 : RUN apt-get update
 ---> Running in 2026e6c913cf
Ign http://archive.ubuntu.com precise InRelease
Hit http://archive.ubuntu.com precise Release.gpg
Hit http://archive.ubuntu.com precise Release
Hit http://archive.ubuntu.com precise/main amd64 Packages
Get:1 http://archive.ubuntu.com precise/main i386 Packages [1641 kB]
Get:2 http://archive.ubuntu.com precise/main TranslationIndex [3706 B]
Get:3 http://archive.ubuntu.com precise/main Translation-en [893 kB]
....
------------------------------------------------

    也可以为镜像设置tag
docker build -t="rainysia/static_web:tag_v1" .
    也可以指定dockerfile
docker build -t="rainysia/static_web:tag_v1" \
                       git@github.com:rainysia/docker-static_web 

docker 构建文件支持.dockerignore文件来忽视对应的文件, 类似.gitignore
docker 在build失败前, 会在每步生成一个id, 可以基于这个id, 来继续最后一个成功后的步骤.
docker run -t -i xxxeeeeet294 /bin/bash

------------------------------------------------
docker build -t="rainysia/static_web" .                                                                                                                                      [15:37:38]
    Sending build context to Docker daemon 2.048 kB
    Sending build context to Docker daemon 
    Step 0 : FROM debian
    latest: Pulling from debian
    6d1ae97ee388: Pull complete 
    8b9a99209d5c: Pull complete 
    debian:latest: The image you are pulling has been verified. Important: image verification is a tech preview feature and should not be relied on to provide security.
    Digest: sha256:2a5204f0a00510e9b99d7ec0fe40bea495b8e3630b820b04675488aad4188e06
    Status: Downloaded newer image for debian:latest
     ---> 8b9a99209d5c
    Step 1 : MAINTAINER rainysia "rainysia@gmail.com"
     ---> Running in 3de883382215
     ---> 491af30c07dc
    Removing intermediate container 3de883382215
    Step 2 : RUN apt-get update
     ---> Running in d3979fb6827a
    Get:1 http://security.debian.org jessie/updates InRelease [63.1 kB]
    Get:2 http://security.debian.org jessie/updates/main amd64 Packages [217 kB]
    Ign http://httpredir.debian.org jessie InRelease
    Get:3 http://httpredir.debian.org jessie-updates InRelease [136 kB]
    Get:4 http://httpredir.debian.org jessie Release.gpg [2373 B]
    Get:5 http://httpredir.debian.org jessie Release [148 kB]
    Get:6 http://httpredir.debian.org jessie-updates/main amd64 Packages [3619 B]
    Get:7 http://httpredir.debian.org jessie/main amd64 Packages [9035 kB]
    Fetched 9606 kB in 32s (293 kB/s)
    Reading package lists...
     ---> 488df59d3a97
    Removing intermediate container d3979fb6827a
    Step 3 : RUN apt-get install -y nginx
     ---> Running in caee197a17aa
    Reading package lists...
    Building dependency tree...
    Reading state information...
    The following extra packages will be installed:
      fontconfig-config fonts-dejavu-core geoip-database init-system-helpers
      .........
    Setting up nginx-full (1.6.2-5) ...
    invoke-rc.d: policy-rc.d denied execution of start.
    Setting up nginx (1.6.2-5) ...
    Setting up rename (0.20-3) ...
    update-alternatives: using /usr/bin/file-rename to provide /usr/bin/rename (rename) in auto mode
    Setting up xml-core (0.13+nmu2) ...
    Processing triggers for libc-bin (2.19-18+deb8u1) ...
    Processing triggers for systemd (215-17+deb8u2) ...
    Processing triggers for sgml-base (1.26+nmu4) ...
     ---> a74b1ee93ca8
    Removing intermediate container caee197a17aa
    Step 4 : RUN echo 'Hi, i am in your container'         > /usr/share/nginx/html/index.html
     ---> Running in d791b08c3fdd
     ---> 75a3f6d8fd40
    Removing intermediate container d791b08c3fdd
    Step 5 : EXPOSE 80
     ---> Running in cd89bc68a838
     ---> 9987527a0059
    Removing intermediate container cd89bc68a838
    Successfully built 9987527a0059
------------------------------------------------

查看build的镜像
docker images
======================================================= 
docker images
    REPOSITORY            TAG                 IMAGE ID            CREATED              VIRTUAL SIZE
    rainysia/static_web   latest              9987527a0059        19 minutes ago       196.2 MB
    rainysia/learn        test                7dee5de20590        43 minutes ago       139.9 MB
    rainysia/learn        latest              b7f12b9b4b29        44 minutes ago       139.9 MB
    learn/ping            latest              9e8823ddedf9        24 hours ago         139.9 MB
    debian                latest              8b9a99209d5c        2 weeks ago          125.1 MB
    learn/tutorial        latest              8dbd9e392a96        2.697135 years ago   128 MB
=======================================================
docker history 9987527a0059 来查看image的历史操作

基于新构建的镜像启动一个新容器.
docker run -d -p 80 --name static_web rainysia/static_web nginx -g "daemon off;"
    0daff8960db967d4bba0ac4851a17862742b15350a4662582133bacb5ae82192

docker ps -l 查看端口情况
    CONTAINER ID        IMAGE                        COMMAND                CREATED              STATUS              PORTS                   NAMES
    0daff8960db9        rainysia/static_web:latest   "nginx -g 'daemon of   About a minute ago   Up About a minute   0.0.0.0:32768->80/tcp   static_web     
    容器中的80端口被映射到了宿主机的32768端口
    也可以通过docker port 来查看容器的端口占用情况
docker port 0daff8960db9 80
    0.0.0.0:32768
        -p 选项可以指定映射端口
docker run -d -p 80:80 --name static_web rainysia/static_web \
        nginx -g "daemon off;"
可以通过 http://127.0.0.1:32768/ 来查看映射
    -p 127.0.0.1:80:80 把80端口绑定到宿主机的127.0.0.1:80
    -P 来公开在dockerfile里面定义的expose的所有端口
docker run -d -P --name static_web rainysia/static_web nginx -g "daemon off;"
docker run -d -p 192.168.85.123:33333:80 --name static_web rainysia/static_web nginx -g "daemon off;"

docker run -tid --name hue8888 --hostname halo-cnode1.domain.org -p 8888:8888 -v /usr/hdp:/usr/hdp cdkdc.domain.org:5000/hue:latest ./build/env/bin/hue runserver_plus 0.0.0.0:8888
    -i 标志保证容器中STDIN是开启的. 
    -t表示告诉docker要为创建的容器分配一个伪tty终端
    -d  参数会把容器放到后台运行
    --name alias_name 可以为这个docker指定一个别名, 要放前面, docker run -tid --name alias_name images:version /bin/bash
    --hostname 指定hostname, 类似--ip
    -p docker 外部主机的被映射的端口:容器内程序的端口, 作端口映射, 来公开在dockerfile里面定义的expose的所有端口.
    -v 挂在目录, 外部主机目录:容器内部目录, 多个就继续-v external_path:internal_path

docker run --rm -h "new_hostname" -ti images_name bash 修改当前image的hostname
e.g.:
docker run --rm -h "halo-cnode1-docker" -t -i cdkdc.domain.org:5000/hue:latest bash           


更新docker images里面的内容后. 
需要stop掉当前的docker, 然后rm 掉, 启新的
docker ps -a 
docker stop Container_xxxxid
docker rm Container_xxxxid/Name
docker start new_xxxxid
docker rmi image_id 根据image_id删除镜像

Dockerfile 的命令
================
FROM 基于哪个镜像
RUN 安装如那间用
MAINTAINER 镜像创建者
CMD 指定一个容器启动时要运行的命令, 类似RUN, RUN是指定镜像被构建时要运行的命令.一个Dockerfile中只能有一条CMD命令，多条则只执行最后一条CMD
CMD主要用于container时启动指定的服务，当Docker run command的命令匹配到CMD command时，会替换CMD执行的命令
    CMD ["/bin/true"]
    CMD ["/bin/true", "-1"]

ENTRYPOINT 提供的命令不容易在启动容器的时候被覆盖,container启动时执行的命令，但是一个Dockerfile中只能有一条ENTRYPOINT命令，如果多条，则只执行最后一条,ENTRYPOINT没有CMD的可替换特性
    ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]

WORKDIR 用来在镜像创建一个新容器时,在容器内部设置一个工作目录, ENTRYPOINT/CMD 指定的程序会在这目录下运行
切换目录用，可以多次切换(相当于cd命令)，对RUN,CMD,ENTRYPOINT生效
    WORKDIR /opt/webapp/db
    RUN bundle install
    WORKDIR /opt/webapp
    ENTRYPOINT ["rackup"]
    可以通过-w来覆盖工作目录
    docker run -ti -w /var/lig ubuntu pwd

ENV 在镜像构建过程中设置环境变量
    ENV RVM_PATH /home/rvm  #类似RUN gem install unicorn
    ENV LANG en_US.UTF-8
    ENV LC_ALL en_US.UTF-8

USER 指定该镜像会以什么用户来运行,不指定默认root
    USER nginx
    USER uid:gid
    USER user:group
    USER user:gid
    USER uid:group
    USER daemon
EXPOSE container内部服务开启的端口。主机上要用还得在启动container时，做host-container的端口映射
    docker run -d -p 127.0.0.1:33301:22 centos7-ssh  #container ssh服务的22端口被映射到主机的33301端口

VOLUME 向容器添加卷
    VOLUME ["/opt/project"]
    VOLUME ["/opt/project", "/data"]


ADD 将构建环境下的文件和目录复制到镜像中 ADD host_file dest_file, host_file支持url地址
所有拷贝到container中的文件和文件夹权限为0755,uid和gid为0,如果要ADD本地文件，则本地文件必须在 docker build <PATH>，指定的<PATH>目录下
ADD只有在build镜像的时候运行一次，后面运行container的时候不会再重新加载了。
    ADD software.inc /opt/application/software.inc
使用docker build - < somefile方式进行build，是不能直接将本地文件ADD到container中。只能ADD url file.

COPY ,不存在会创建目录
    COPY /etc/nginx/  /etc/apache2/nginx

ONBUILD 为镜像添加触发器, docker inspect 可以看见OnBuild部分
    ONBUILD ADD . /app/src
    ONBUILD RUN cd /app/src && make

==================
$sudo docker push user/alias_name push到docker hub上
$sudo docker push rainysia/static_web
The push refers to a repository [rainysia/static_web] (len: 1)
9987527a0059: Image already exists 
75a3f6d8fd40: Image successfully pushed 
a74b1ee93ca8: Image successfully pushed 
488df59d3a97: Image successfully pushed 
491af30c07dc: Image successfully pushed 
8b9a99209d5c: Image successfully pushed 
6d1ae97ee388: Image successfully pushed 
Digest: sha256:c6ea3b8f3a01dbac27945c576e41c5069adf6aaaa2a7c7d91141437359768edc

为镜像打标签
$sudo docker tag xxxxxxid docker.example.com:5000/rainysia/static_web
然后快速部署
$sudo docker run -t -i docker.example.com:5000/rainysia/static_web /bin/bash


==============================
修改dockerfile

docker iamges
docker build -t rainysia/new_project_name ./
docker rm `docker ps -q -a`
docker history rainysia/nginx
docker push rainysia/new_project_name

-p host_port:container_port
docker run -d -p 127.0.0.1:44444:80 --name website \
        -v $PWD/website:/var/www/html/website \
        rainysia/nginx nginx

docker run -d -p 127.0.0.1:44444:80 --name test_web rainysia/nginx nginx
          daemon port ip:port:external_port alias_name images command_in_container

docker logs -f test_web 查看docker运行的日志
docker port test_web 80 查看docker容器的端口映射
docker top test_web  查看docker容器的正在运行的程序

=======================================
卷可以在容器间共享, 即使容器停止. 卷里的内容依旧存在. 适合对代码作开发和测试
    -v 参数指定了卷的源目录(本地宿主机的目录)和容器里的目的目录. 这两个目录用:分隔,目的目录不存在会自动建
        也可以在目的目录后面加上rw, ro 来指定目的目录的读写状态
    -v host_path:docker_path, 注意一定要全路径.(绝对路径)
docker run -d -p 80 --name website \
        -v $PWD/website:/var/www/html/website:ro \
        rainysia/new_project_name nginx
    通过卷将$PWD/website 挂载到了容器的/var/www/html/webiste 目录.

docker run -d -p 127.0.0.1:44444:80 --name test_web \
-v $PWD/website:/var/www/html:ro \
rainysia/nginx nginx


导出本地镜像到本地文件
docker save

[root@cdkdc]/# docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
registry                          latest              061610023430        7 weeks ago         422.8 MB
halo                              latest              dfb06ee74ae2        11 weeks ago        679 MB
ubuntu                            14.04               123456788990        1 hours ago         300 MB

docker save -o package_name.tar halo:latest
docker save -o ubuntu.tar ubuntu:14.04

载入镜像
docker load --input package_name.tar
docker load < packge_name.tar

改名镜像
docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
192.168.85.116:5000/nginx         latest              3ea8fdece1c5        3 months ago        244.2 MB

docker tag 192.168.85.116:5000/nginx nginx/latest  # old new/version, or use docker tag `IMAGE_ID` new_name:tag_version
docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
192.168.85.116:5000/nginx         latest              3ea8fdece1c5        3 months ago        244.2 MB
nginx/latest                      latest              3ea8fdece1c5        3 months ago        244.2 MB
docker rmi 192.168.85.116:5000/nginx


清理所有未打过标签的本地镜像
docker rmi $(docker images --quiet --filter "dangling=true")

导出容器
docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS               NAMES
7691a814370e        ubuntu:14.04        "/bin/bash"         36 hours ago        Exited (0) 21 hours ago                       test
docker export 7691a814370e > ubuntu.tar

导入容器快照
docker import - test/ubuntu:v1.0
docker images
REPOSITORY          TAG                 IMAGE ID            CREATED              VIRTUAL SIZE
test/ubuntu         v1.0                9d37a6082e97        About a minute ago   171.3 MB

ocker import http://example.com/exampleimage.tgz example/imagerepo  #从网络导入

```

Docker Cheat Sheet
===========

### 生命周期

* [`docker create`](https://docs.docker.com/reference/commandline/create) 创建一个容器但是不启动。
* [`docker run`](https://docs.docker.com/reference/commandline/run) 在同一个操作中创建并启动一个容器.
* [`docker rm`](https://docs.docker.com/reference/commandline/rm) 删除容器。

如果你想要一个临时容器，`docker run --rm` 会在容器停止之后删除它。

如果你想映射宿主(host)的一个文件夹到 docker 容器，`docker run -v $HOSTDIR:$DOCKERDIR`。参考 [Volumes](https://github.com/wsargent/docker-cheat-sheet/#volumes)。

如果你想同时删除和容器关联的 volumes ，那么在删除容器的时候必须包含 -v 选项，像这样 `docker rm -v`。

## 启动和停止

* [`docker start`](https://docs.docker.com/reference/commandline/start) 启动容器。
* [`docker stop`](https://docs.docker.com/reference/commandline/stop) 停止运行中的容器。
* [`docker restart`](https://docs.docker.com/reference/commandline/restart) 停止之后再启动容器。
* [`docker pause`](https://docs.docker.com/engine/reference/commandline/pause/) 暂停运行中的容器，将其 "冻结" 在当前状态。
* [`docker unpause`](https://docs.docker.com/engine/reference/commandline/unpause/) 结束容器暂停状态。
* [`docker wait`](https://docs.docker.com/reference/commandline/wait) 阻塞，到运行中的容器停止为止。
* [`docker kill`](https://docs.docker.com/reference/commandline/kill) 向运行中容器发送 SIGKILL 指令。
* [`docker attach`](https://docs.docker.com/reference/commandline/attach) 链接到运行中容器。

如果你想整合容器到[宿主进程管理(host process manager)](https://docs.docker.com/articles/host_integration/)，那么以 `-r=false` 启动守护进程(daemon)然后使用 `docker start -a`。

如果你想通过宿主暴露容器的端口(ports)，请看[暴露端口](#exposing-ports)一节。

故障 docker 实例的重启策略在[这里](http://container42.com/2014/09/30/docker-restart-policies/)。

### 信息

* [`docker ps`](https://docs.docker.com/reference/commandline/ps) 查看运行中的所有容器。
* [`docker logs`](https://docs.docker.com/reference/commandline/logs) 从容器中获取日志。
* [`docker inspect`](https://docs.docker.com/reference/commandline/inspect) 查看某个容器的所有信息(包括 IP 地址)。
* [`docker events`](https://docs.docker.com/reference/commandline/events) 从容器中获取事件(events)。
* [`docker port`](https://docs.docker.com/reference/commandline/port) 查看容器的公开端口。
* [`docker top`](https://docs.docker.com/reference/commandline/top) 查看容器中活动进程。
* [`docker stats`](https://docs.docker.com/reference/commandline/stats) 查看容器的资源使用情况统计信息。
* [`docker diff`](https://docs.docker.com/reference/commandline/diff) 查看容器的 FS 中有变化文件信息。

`docker ps -a` 查看所有容器，包括正在运行的和已停止的。

### 导入 / 导出

* [`docker cp`](https://docs.docker.com/reference/commandline/cp) 在容器和本地文件系统之间复制文件或文件夹。
* [`docker export`](https://docs.docker.com/reference/commandline/export) 将容器的文件系统切换为压缩包(tarball archive stream)输出到 STDOUT。

### 执行命令

* [`docker exec`](https://docs.docker.com/reference/commandline/exec) 在容器中执行命令。

比如，进入正在运行的容器，在名为 foo 的容器中打开一个新的 shell 进程: `docker exec -it foo /bin/bash`.

## 镜像(Images)

镜像是[docker 容器的模板](https://docs.docker.com/engine/understanding-docker/#how-does-a-docker-image-work)。

### 生命周期

* [`docker images`](https://docs.docker.com/reference/commandline/images) 查看所有镜像。
* [`docker import`](https://docs.docker.com/reference/commandline/import) 从压缩文件中创建镜像。
* [`docker build`](https://docs.docker.com/reference/commandline/build) 从 Dockerfile 创建镜像。
* [`docker commit`](https://docs.docker.com/reference/commandline/commit) 为容器创建镜像，如果容器正在运行则会临时暂停。
* [`docker rmi`](https://docs.docker.com/reference/commandline/rmi) 删除镜像。
* [`docker load`](https://docs.docker.com/reference/commandline/load) 通过 STDIN 从压缩包加载镜像，包括镜像和标签(images and tags) (0.7 起).
* [`docker save`](https://docs.docker.com/reference/commandline/save) 通过 STDOUT 保存镜像到压缩包，包括所有的父层，标签和版本(parent layers, tags & versions) (0.7 起).

### 信息

* [`docker history`](https://docs.docker.com/reference/commandline/history) 查看镜像历史记录。
* [`docker tag`](https://docs.docker.com/reference/commandline/tag) 给镜像命名打标(tags) (本地或者仓库)。

### 清理

虽然你可以用 `docker rmi` 命令来删除指定的镜像，但是这里有个称为 [docker-gc](https://github.com/spotify/docker-gc) 的工具，它可以以一种安全的方式，清理掉那些不再被任何容器使用的镜像。

## 网络(Networks) 

Docker 有[网络(networks)](https://docs.docker.com/engine/userguide/networking/dockernetworks/)功能。我并不是很了解它，所以这是一个扩展本文的好地方。这里有篇笔记指出，这是一种可以不使用端口来达成 docker 容器间通信的好方法。详情查阅[通过网络来工作](https://docs.docker.com/engine/userguide/networking/work-with-networks/)。

### 生命周期

* [`docker network create`](https://docs.docker.com/engine/reference/commandline/network_create/)
* [`docker network rm`](https://docs.docker.com/engine/reference/commandline/network_rm/)

### 信息

* [`docker network ls`](https://docs.docker.com/engine/reference/commandline/network_ls/)
* [`docker network inspect`](https://docs.docker.com/engine/reference/commandline/network_inspect/)

### 链接

* [`docker network connect`](https://docs.docker.com/engine/reference/commandline/network_connect/)
* [`docker network disconnect`](https://docs.docker.com/engine/reference/commandline/network_disconnect/)

## Registry 和 Repository

仓库(repository)是*被托管(hosted)*的已命名镜像(tagged images)集合，这组镜像用于构建容器文件系统。

仓管中心(registry)是一个*托管服务(host)* -- 一个服务，用于存储仓库和提供 HTTP API，以便[管理上传和下载仓库](https://docs.docker.com/userguide/dockerrepos/)。

Docker.com 把它自己的[索引](https://hub.docker.com/)托管到了它的仓管中心，那里有数量众多的仓库。不过话虽如此，这个仓管中心[并没有很好的验证镜像](https://titanous.com/posts/docker-insecurity)，所以如果你很担心安全问题的话，请尽量避免使用它。

* [`docker login`](https://docs.docker.com/reference/commandline/login) 登入仓管中心。
* [`docker search`](https://docs.docker.com/reference/commandline/search) 从仓管中心检索镜像。
* [`docker pull`](https://docs.docker.com/reference/commandline/pull) 从仓管中心拉去镜像到本地。
* [`docker push`](https://docs.docker.com/reference/commandline/push) 从本地推送镜像到仓管中心。

### 本地仓管中心

[如何实现仓管中心](https://github.com/docker/docker-registry)，官方提供了一个镜像，实现了基本的安装，可以通过执行
[`docker run -p 5000:5000 registry`](https://github.com/docker/docker-registry#quick-start)启动。
注意: 该实现并没有提供任何的权限控制。所以你可以通过选项 `-P -p 127.0.0.1:5000:5000` 来限制只能从本机接入。
为了推送仓库到该中心，请把镜像的标签命名为 `repositoryHostName:5000/imageName` ，然后推送该标签。

## Dockerfile

[配置文件](https://docs.docker.com/reference/builder/)。当你执行 `docker build` 的时候会根据该配置文件设置 Docker 容器。远优于使用 `docker commit`。如果你使用 [jEdit](http://jedit.org)，我为 [Dockerfile](https://github.com/wsargent/jedit-docker-mode)做了个语法高亮模块。你还可以试试 [工具集](#tools)部分的内容。

### 指令

* [.dockerignore](https://docs.docker.com/reference/builder/#dockerignore-file)
* [FROM](https://docs.docker.com/reference/builder/#from) 为其他指令设置基础镜像(Base Image)。
* [MAINTAINER](https://docs.docker.com/reference/builder/#maintainer) 为生成的镜像设置作者字段。
* [RUN](https://docs.docker.com/reference/builder/#run) 在当前镜像的基础上生成一个新层并执行命令。
* [CMD](https://docs.docker.com/reference/builder/#cmd) 设置容器默认执行命令。
* [EXPOSE](https://docs.docker.com/reference/builder/#expose) 告知 Docker 容器在运行时所要监听的网络端口。注意：并没有实际上将端口设置为可访问。
* [ENV](https://docs.docker.com/reference/builder/#env) 设置环境变量。
* [ADD](https://docs.docker.com/reference/builder/#add) 将文件，文件夹或者远程文件复制到容器中。缓存无效。尽量用 `COPY` 代替 `ADD`。
* [COPY](https://docs.docker.com/reference/builder/#copy) 将文件或文件夹复制到容器中。
* [ENTRYPOINT](https://docs.docker.com/reference/builder/#entrypoint) 将一个容器设置为可执行。
* [VOLUME](https://docs.docker.com/reference/builder/#volume) 为外部挂载卷标或其他容器设置挂载点(mount point)。
* [USER](https://docs.docker.com/reference/builder/#user) 设置执行 RUN / CMD / ENTRYPOINT 命令的用户名。
* [WORKDIR](https://docs.docker.com/reference/builder/#workdir) 设置工作目录。
* [ARG](https://docs.docker.com/engine/reference/builder/#arg) 定义编译时(build-time)变量。
* [ONBUILD](https://docs.docker.com/reference/builder/#onbuild) 添加触发指令，当该镜像被作为其他镜像的基础镜像时该指令会被触发。
* [STOPSIGNAL](https://docs.docker.com/engine/reference/builder/#stopsignal) 设置通过系统向容器发出退出指令。
* [LABEL](https://docs.docker.com/engine/userguide/labels-custom-metadata/) 将键值对元数据(key/value metadata)应用到你的镜像，容器，或者守护进程。 

### 教程

* [Flux7's Dockerfile Tutorial](http://flux7.com/blogs/docker/docker-tutorial-series-part-3-automation-is-the-word-using-dockerfile/)

### 例子

* [Examples](https://docs.docker.com/reference/builder/#dockerfile-examples)
* [Best practices for writing Dockerfiles](https://docs.docker.com/articles/dockerfile_best-practices/)
* [Michael Crosby](http://crosbymichael.com/) 还有更多的 [Dockerfiles best practices](http://crosbymichael.com/dockerfile-best-practices.html) / [take 2](http://crosbymichael.com/dockerfile-best-practices-take-2.html)
* [Building Good Docker Images](http://jonathan.bergknoff.com/journal/building-good-docker-images) / [Building Better Docker Images](http://jonathan.bergknoff.com/journal/building-better-docker-images)
* [Managing Container Configuration with Metadata](https://speakerdeck.com/garethr/managing-container-configuration-with-metadata)

## 层(Layers)

Docker 的版本化文件系统是基于层的。就像[git的提交或文件变更系统](https://docs.docker.com/engine/userguide/storagedriver/imagesandcontainers/)一样。

注意: 如果你使用 [aufs](https://en.wikipedia.org/wiki/Aufs) 作为你的文件系统，当删除一个容器的时候，Docker 并不一定能成功删除的文件卷标！更多详细信息请参阅 [PR 8484](https://github.com/docker/docker/pull/8484)。

## 链接(Links)

链接(Links)[通过 TCP/IP 端口](https://docs.docker.com/userguide/dockerlinks/)实现了 Docker 容器之间的通讯。[链接到 Redis](https://docs.docker.com/examples/running_redis_service/) 和 [Atlassian](https://blogs.atlassian.com/2013/11/docker-all-the-things-at-atlassian-automation-and-wiring/) 是两个可用的例子。你还可以(0.11 开始)[通过 hostname 关联链接](https://docs.docker.com/userguide/dockerlinks/#updating-the-etchosts-file)。

注意: 如果你希望容器之间**只**通过链接进行通讯，在启动 docker 守护进程的时候请添加参数 `-icc=false` 来禁用内部进程通讯。

如果你有一个名为 CONTAINER 的容器(通过 `docker run --name CONTAINER` 指定) 并且在 Dockerfile 中，它的端口暴露为:

```
EXPOSE 1337
```

然后，我们创建另外一个名为 LINKED 的容器:

```
docker run -d --link CONTAINER:ALIAS --name LINKED user/wordpress
```

然后 CONTAINER 的端口和别名将会以如下的环境变量出现在 LINKED 中:

```
$ALIAS_PORT_1337_TCP_PORT
$ALIAS_PORT_1337_TCP_ADDR
```

之后你就可以通过这种方式来链接它了。

要删除链接，通过命令 `docker rm --link `。

如果你想跨 docker 主机链接，你可以查看 [Swarm](https://docs.docker.com/swarm/) 部分。. 在 [stackoverflow 上的这个链接](https://stackoverflow.com/questions/21283517/how-to-link-docker-services-across-hosts)也提供了一些关于如何跨 docker 主机进行链接的好方式。

## 卷标(Volumes)

Docker 的卷标(volumes)是一个[free-floating 文件系统](https://docs.docker.com/userguide/dockervolumes/)。它们不应该链接到特定的容器上。好的做法是如果可能，应当把卷标挂载到[纯数据容器(data-only containers)](https://medium.com/@ramangupta/why-docker-data-containers-are-good-589b3c6c749e)上。

### 生命周期

* [`docker volume create`](https://docs.docker.com/engine/reference/commandline/volume_create/)
* [`docker volume rm`](https://docs.docker.com/engine/reference/commandline/volume_rm/)

### 信息

* [`docker volume ls`](https://docs.docker.com/engine/reference/commandline/volume_ls/)
* [`docker volume inspect`](https://docs.docker.com/engine/reference/commandline/volume_inspect/)

卷标在不能使用链接(只有 TCP/IP )的情况下非常有用。例如，如果你有两个 docker 实例需要通讯并在文件系统上留下记录。

你可以一次性将其挂载到多个 docker 容器上，通过 `docker run --volumes-from`。

因为卷标是独立的文件系统，它们通常被用于存储各容器之间的瞬时状态。也就是说，你可以配置一个无状态临时容器，关掉之后，当你有第二个这种临时容器实例的时候，你可以从上一次保存的状态继续执行。

查看[卷标进阶](http://crosbymichael.com/advanced-docker-volumes.html)来获取更多细节。Container42 [非常有用](http://container42.com/2014/11/03/docker-indepth-volumes/)。

从 1.3 开始，你可以[映射宿主 MacOS 的文件夹作为 docker 卷标](https://docs.docker.com/userguide/dockervolumes/#mount-a-host-directory-as-a-data-volume)通过 boot2docker:

```
docker run -v /Users/wsargent/myapp/src:/src
```

你也可以用远程 NFS 卷标，如果你觉得你[有足够勇气](http://www.tech-d.net/2014/03/29/docker-quicktip-4-remote-volumes/)。

可还可以考虑运行一个纯数据容器，像[这里](http://container42.com/2013/12/16/persistent-volumes-with-docker-container-as-volume-pattern/)所说的那样，提供可移植数据。

## 暴露端口(Exposing ports)

通过宿主容器暴露输入端口是相当[繁琐，但有效](https://docs.docker.com/reference/run/#expose-incoming-ports)的。

这种方式可以将容器端口映射到宿主端口上(只使用本地主机(localhost)接口)，通过使用 `-p`:

```
docker run -p 127.0.0.1:$HOSTPORT:$CONTAINERPORT --name CONTAINER -t someimage
```

你可以告诉 Docker 容器在运行时监听指定的网络端口，通过使用 [EXPOSE](https://docs.docker.com/reference/builder/#expose):

```
EXPOSE <CONTAINERPORT>
```

但是注意 EXPOSE 并不会暴露端口本身，只有 `-p` 这样做。

如果你是在 Virtualbox 中运行 Docker，那么你需要转发端口(forward the port)，使用 [forwarded_port](https://docs.vagrantup.com/v2/networking/forwarded_ports.html)。它可以用于在 Vagrantfile 上配置暴露端口段，这样你就可以动态的映射它们了:

```
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  ...

  (49000..49900).each do |port|
    config.vm.network :forwarded_port, :host => port, :guest => port
  end

  ...
end
```

如果你忘记你将什么端口映射到宿主容器上的话，使用 `docker port` 来查看它:

```
docker port CONTAINER $CONTAINERPORT
```
## 安全(Security)

这节准备讨论一些关于 Docker 安全性的问题。[安全](https://docs.docker.com/engine/articles/security/)这章讲述了更多细节。

首先第一件事: Docker 是有 root 权限的。如果你在 `docker` 组，那么你就有[ root 权限](http://reventlov.com/advisories/using-the-docker-command-to-root-the-host)。如果你暴露了 docker unix socket 给容器，意味着你赋予了容器[宿主的 root 权限](https://www.lvh.io/posts/dont-expose-the-docker-socket-not-even-to-a-container.html)。Docker 不应该是你唯一的防御措施。

### 安全提示

Docker 镜像 id 属于[敏感信息](https://medium.com/@quayio/your-docker-image-ids-are-secrets-and-its-time-you-treated-them-that-way-f55e9f14c1a4) 所以它不应该向外界公开。你应该把他们当成密码来对待。


关闭内部进程通讯:

```
docker -d --icc=false --iptables
```

设置容器为只读:

```
docker run --read-only
```

通过 hashsum 来验证卷标:

```
docker pull debian@sha256:a25306f3850e1bd44541976aa7b5fd0a29be
```

设置卷标为只读:

```
docker run -v $(pwd)/secrets:/secrets:ro debian
```

设置内存和 CPU 共享:

```
docker -c 512 -mem 512m
```

在 Dockerfile 中定义并运行一个用户，避免在容器中以 root 身份操作:

```
RUN groupadd -r user && useradd -r -g user user
USER user
```

### 最后的 Ids

```
alias dl='docker ps -l -q'
docker run ubuntu echo hello world
docker commit `dl` helloworld
```

### 带命令行的提交 (需要 Dockerfile)

```
docker commit -run='{"Cmd":["postgres", "-too -many -opts"]}' `dl` postgres
```

### 获取 IP 地址

```
docker inspect `dl` | grep IPAddress | cut -d '"' -f 4
```

或者

```
wget http://stedolan.github.io/jq/download/source/jq-1.3.tar.gz
tar xzvf jq-1.3.tar.gz
cd jq-1.3
./configure && make && sudo make install
docker inspect `dl` | jq -r '.[0].NetworkSettings.IPAddress'
```

或者用[go 模板](https://docs.docker.com/reference/commandline/inspect)

```
docker inspect -f '{{ .NetworkSettings.IPAddress }}' <container_name>
```

### 获取端口映射

```
docker inspect -f '{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}' <containername>
```

### 通过正则获取容器

```
for i in $(docker ps -a | grep "REGEXP_PATTERN" | cut -f1 -d" "); do echo $i; done`
```

### 获取环境设定

```
docker run --rm ubuntu env
```

### 强迫关闭正在运行的容器

```
docker kill $(docker ps -q)
```

### 删除旧容器

```
docker ps -a | grep 'weeks ago' | awk '{print $1}' | xargs docker rm
```

### 删除停止容器

```
docker rm -v `docker ps -a -q -f status=exited`
```

### 删除 dangling 镜像

```
docker rmi $(docker images -q -f dangling=true)
```

### 删除所有镜像

```
docker rmi $(docker images -q)
```

### 删除 dangling 卷标

Docker 1.9 开始:

```
docker volume rm $(docker volume ls -q -f dangling=true)
```

1.9.0 中，过滤器 `dangling=false` 居然 _没_ 用 - 它会被忽略然后列出所有的卷标。

### 查看镜像依赖

```
docker images -viz | dot -Tpng -o docker.png
```

### Docker 容器瘦身  [Intercity 博客](http://bit.ly/1Wwo61N)

- 在当前运行层(RUN layer)清理 APT

这应当和其他 apt 命令在同一层中完成。
否则，前面的层将会保持原有信息，而你的镜像则依旧臃肿。
 
```
RUN {apt commands} \
  && apt-get clean \  
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
```
- 压缩镜像
```
ID=$(docker run -d image-name /bin/bash)
docker export $ID | docker import – flat-image-name
```

- 备份
```
ID=$(docker run -d image-name /bin/bash)
(docker export $ID | gzip -c > image.tgz)
gzip -dc image.tgz | docker import - flat-image-name
```

### 监视运行中容器的系统资源利用率

检查某个单独容器的 CPU, 内存, 和 网络 i/o 使用情况，你可以:

```
docker stats <container>
```

按 id 列出所有的容器:

```
docker stats $(docker ps -q)
```

按名称列出所有容器:

```
docker stats $(docker ps --format '{{.Names}}')
```

###Private docker repository
------------------------------------------------
```
server
docker pull registry
docker run -d -p 5000:5000 registry
docker run -d -p 5000:5000 -v /opt/data/registry:/tmp/registry registry 自定义仓库地址
docker run -d --hostname domain.com -p 5000:5000 -v /opt/data/registry:/tmp/registry registry 自定义仓库地址,和bind域名

docker stop `ps -a`
 
client
docker tag image_name server_ip:5000/tag_name
docker push server_ip:5000/tag_name

docker pull williamyeh/scala
docker tag  2.11.6 cdcbi.domain.org:5000/scala
docker tag  williamyeh/scala 192.168.85.116:5000/scala
docker push cdcbi.domain.org:5000/scala

docker pull cdcbi.domain.org:5000/scala:2.11.6 #default latest

docker search private registry
v2 registry
curl -X GET http://cdkdc.domain.org:5000/v1/search
curl -k https://cdcbi.domain.org:5000/v2/_catalog

curl -X GET http://localhost:5000/v2/_catalog
{"repositories":["ubuntu"]}
$ curl -X GET http://localhost:5000/v2/ubuntu/tags/list
{"name":"ubuntu","tags":["latest"]}

删除用curl -X DELETE http://cddc.domain.org:5000/v1/repositories/images_name/


对container
docker commit container_id new_image_name  #container_id 来自docker ps -l, 这样会暂停docker容器的运行,并且保存为一个image


error: docker user https
因为Docker从1.3.X之后，与docker registry交互默认使用的是https，然而此处搭建的私有仓库只提供http服务，所以当与私有仓库交互时就会报上面的错误。为了解决这个问题需要在启动docker server时增加启动参数为默认使用http访问。修改docker启动配置文件
vim /etc/init/docker.conf
    --insecure-registry server_ip:5000

	exec "$DOCKER" -d $DOCKER_OPTS --insecure-registry=192.168.85.116:5000 --insecure-registry=cdcbi.domain.org:5001
restart docker
if not work:
    kill docker,
run 
docker -d --insecure-registry 192.168.85.116:5000
or 
docker daemon --insecure-registry cdkdc.domain.org:5000

or 
vim /lib/systemd/system/docker.service

add the below
    EnvironmentFile=-/etc/default/docker
change ExecStart
    ExecStart=/usr/bin/docker daemon -H fd:// $DOCKER_OPTS or $OPTIONS

EnvironmentFile 变量后面 =- 表示 ignore_errors=yes 的意思，$DOCKER_OPTS 添加到 ExecStart 里意思应该是让 systemd 把 EnvironmentFile 里的 $DOCKER_OPTS 作为 docker 的启动参数。错误的原因是 $DOCKER_OPTS 好像没有被解析，docker 直接以 /usr/bin/docker -d $DOCKER_OPTS -H fd:// 启动，而不是

vim /etc/default/docker
add the below
    DOCKER_OPTS="-D --insecure-registry cdcbi.domain.org:5000"
or 
    OPTIONS="-D --insecure-registry cdcbi.domain.org:5000"
    OPTIONS="-D --insecure-registry 192.168.85.116:5000 --insecure-registry cdcbi.domain.org:5000 --insecure-registry hi-docker.domain.org"

systemctl restart docker
systemctl daemon-reload


centos7:
vim /etc/systemd/system/docker.service
add [Service]
EnvironmentFile=-/etc/sysconfig/docker
ExecStart=/usr/bin/docker daemon -H fd:// $OPTIONS

vim /etc/sysconfig/docker
add
    OPTIONS="-D --selinux-enabled --insecure-registry 192.168.85.116:5000 --insecure-registry cdcbi.domain.org:5000 --insecure-registry hi-docker.domain.org"
systemctl restart docker
systemctl daemon-reload

    
```

# Docker simple
----------------------
```
docker简单操作
1. 查看
1.1 当前容器 docker ps / docker ps -a
1.2 当前镜像 docker images
1.3 某容器具体情况 docker inspect 719d98db9d43
1.4 某容器的内部情况 docker top 719d98db9d43
2. 建立/启动/关闭容器
1.1 建立 docker run -d ubuntu [-name XXXX]
1.2 关闭 docker stop 719d98db9d43
1.3 启动 docker start 719d98db9d43
1.4 重启 docker restart 719d98db9d43
1.5 删除 docker rm 719d98db9d43
1.6 删除一个镜像 docker rmi ubuntu
1.7 修改容器名称 docker rename amb1 amba
3. 进入容器
3.1 建立同时进入 docker run -ti -d ubuntu /bin/bash
3.2 标准进入 docker attach ubuntu
3.2.1 出来 ctrl p + ctrl q
3.3 直接运行 docker exec ubuntu ls
3.3.1 另一种进入方式 docker exec -it 3c7579fabe0a /bin/bash
3.4 复制容器中的文件或文件夹到主机系统中 docker cp 23ad234:~/test.txt ./test.txt
4. 备份回滚
4.1 将容器导出为tar包 docker export 23ad234 > mytest.docker.tar
4.2 创建一个空容器并导入tar包 docker import ./mytest.docker.tar
4.3 将容器改动提交到镜像中 docker commit 23ad234 mytest
4.4 导出镜像 docker save -o a.tar amb1
5. 编译镜像
5.1 docker build ./mydir/
6. dockerfile 写法
6.1 基本上, 在基础镜像上改吧, 有些东西太难测了
6.2 具体的指令, 只需要在基础盘上, 明白
6.2.1 FROM 基础os盘
6.2.2 RUN 跑指令, 并保存变动, 在build时运行
6.2.3 COPY 将外部文件拷贝入镜像
6.2.4 EXPOSE 暴露端口
6.2.5 ENV 设置环境变量
6.2.6 ENTRYPOINT 容器启动后运行什么, 不会被命令行覆盖
6.2.7 CMD 容器启动后运行什么, 会被命令行覆盖. CMD和ENTRYPOINT只有最后一个生效
7. docker网站
docker search, pull, login, and push
```

# Docker Advanced 
----------------------
```
Machine(Docker管理工具)：解决的是操作系统异构安装Docker困难的问题，没有Machine的时候，CentOS是一种，Ubuntu又是一种，AWS又是一种。有了Machine，所有的系统都是一样的安装方式。
Swarm(Docker集群工具)：我们有了Machine就意味着有了docker环境，但是那是单机的，而通常我们的应用都是集群的。这正是Swarm要做的事情，给你提供docker集群环境和调度策略等。
Compose(Docker编排工具)：有了环境，我们下一步要做什么？部署应用。然后我们需要docker run image1、docker run image2...一次一次不厌其烦的重复这些操作，每次都写大量的命令参数。Compose简化了这个流程，只需要把这些内容固话到docker-compose.yml中。
目前Machine、Swarm、Compose已经可以结合使用，创建集群环境，简单的在上面部署应用

swarm:客户端通过它的网络端口（2375）与Swarm交互,Swarm守护进程本身相当于是一个调度器和一个路由器。它实际上并没有运行容器，也就是说，如果Swarm服务停止了，它在终端Docker主机上已分配好的容器仍然是开启的。另外，由于它不处理任何网络路由（网络连接需要被直接发送到后端的Docker主机上），即使Swarm守护进程意外终止，运行的容器仍然可用。当Swarm从这样的崩溃中恢复，它依然能够查询终端以重建其元数据的列表。
```

# tips
-----------
```
docker容器的hosts文件。
在正在运行的容器 用docker exec 进入修改 /etc/hosts 文件 ，这个容器被重启后会发现 hosts文件会被还原。 所以不要直接修改hosts文件， 需要增加hosts ，在docker run时 用 –add-host 参数。

虚拟目录不会提交到镜像
Dockerfile 中 VOLUME 指定的目录 或 docker run 时 -v 参数指定的目录， 在docker commit 时不会提交到镜像中。 如果-v 参数指定的容器内的目录原本有文件， 原本的文件都会被删除， 只存在宿主机目录的文件。

docker容器的重启。
容器一个容器运行中apache 我们要重启Apache ， 应该怎么重启？ 可能新手会 docker exec -it container_name bash 进入容器， 然后运行 service apache2 restart 启动Apache ， 这样是不能启动apache的， 只会把容器停止掉。 因为容器的主进程就是Apache ， 主进程退出时会退出容器， 在重启apache的时候 主进程先退出了， 这时候docker容器也跟着退出了，所以Apache不会重启。 要重启Apache 用docker命令： docker restart container_name

退出容器的方法
如果是docker run 运行一个容器， 没有加 -d 参数让它后台运行， 这时候 ctrl+c 退出进程也会让容器停止， 如果先退出但不停止容器可以ctrl+p 然后 ctrl+q

容器内可以用supervision管理进程，防止进程异常退出。
```
