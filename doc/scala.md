scala
========
1. [Scala-lang](http://www.scala-lang.org/download/)
2. [scala deb](http://downloads.lightbend.com/scala/2.11.8/scala-2.11.8.deb)
3. [twitter scala](https://twitter.github.io/scala_school/zh_cn/)
4. [scala learn](http://zh.scala-tour.com/#/basics-contents)

###Install
-------------
1. debian 
```
dpkg -i scala-2.11.8.deb or apt-get install scala
```

2. common
```
tar -xzf scala-2.11.8.tgz`
```

3. configure
```
add ENV
export SCALA_HOME=/usr/lib/scala
export PATH=$PATH:$SCALA_HOME/bin
source ~/.bashrc
scala -version
Scala code runner version 2.11.8 -- Copyright 2002-2016, LAMP/EPFL
```

4. interactive<br />
`scala` will go into scala interactive shell, 
`:q`  to quit scala shell

###Grammar
-------------
1. val 定义常量, 值赋值后不能再改变
    val aa = 1 + 1
2. var 定义变量, 可以修改名称和结果的绑定.注意一定是双引号
    var name = "tommy"
        name = "clare"
3. 函数def 
    def addOne(m: Int): Int = m + 1


###ENV
