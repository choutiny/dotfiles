Java
=======
[`Download JDK8`](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
[`Download JDK7`](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)

### Install
-----------------
```
mkdir /usr/java && cd /usr/java
tar -zxvf jdk8-xxx-linux-x64.tar.gz && mv jdk1.8.0_xx /usr/java/java8
update-alternative --install /usr/bin/java java /usr/java/java8/bin/java 1100
update-alternative --install /usr/bin/javac javac /usr/java/java8/bin/javac 1100
update-alternative --install /usr/bin/jar jar /usr/java/java8/bin/jar 1100
```
select java8
```
update-alternative --config java
update-alternative --config javac
update-alternative --config jar
```
add the blow part into `.bashrc` or `.zshrc`
```
export JAVA_HOME=/usr/java/java8
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar
export PATH=$PATH:$JAVA_HOME/bin
java -version
