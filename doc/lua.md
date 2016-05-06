lua
========
[LUA 5.3.2 ](http://www.lua.org/ftp/lua-5.3.2.tar.gz)

## Install
----------
```
centos:

yum install gcc readline readline-devel
tar zxvf lua-5.3.2.tar.gz
cd lua-5.3.2 && make linux test
make install

debian:

apt-get install lua5.3
ln -s /usr/bin/lua5.3 /usr/bin/lua
ln -s /usr/bin/lua5.3 /usr/local/bin/lua
```

## run
----------
```
shell#lua5.3
Lua 5.3.1  Copyright (C) 1994-2015 Lua.org, PUC-Rio
>print("hello world")       #Lua脚本的语句的分号是可选的，这个和GO语言很类似。

or 
shell#lua32 hello.lua

or chmod +x hello.lua
#./hello.lua
```

## syntax
----------
1. comments --行注释, --[[ 块注释 --]]
2. add `#!/usr/local/bin/lua` in lua
3. 变量 
``` 
Lua的数字只有double型，64bits，你不必担心Lua处理浮点数会慢（除非大于100,000,000,000,000），或是会有精度问题,你可以以如下的方式表示数字，0x开头的16进制和C是很像的。
num = 1024
num = 3.0
num = 3.1416
num = 314.16e-2
num = 0.31416E1
num = 0xff
num = 0x56
字符串你可以用单引号，也可以用双引号，还支持C类型的转义，比如： ‘\a’ （响铃）， ‘\b’ （退格）， ‘\f’ （表单）， ‘\n’ （换行）， ‘\r’ （回车）， ‘\t’ （横向制表）， ‘\v’ （纵向制表）， ‘\\’ （反斜杠）， ‘\”‘ （双引号）， 以及 ‘\” （单引号)
下面的四种方式定义了完全相同的字符串（其中的两个中括号可以用于定义有换行的字符串）
a = 'alo\n123"'
a = "alo\n123\""
a = '\97lo\10\04923"'
a = [[alo
123"]]
C语言中的NULL在Lua中是nil，比如你访问一个没有声明过的变量，就是nil，比如下面的v的值就是nil
v = UndefinedVariable
布尔类型只有nil和false是 false，数字0啊，‘’空字符串（’\0’）都是true！
另外，需要注意的是：lua中的变量如果没有特殊说明，全是全局变量，那怕是语句块或是函数里。变量前加local关键字的是局部变量。
theGlobalVar = 50
local theLocalVar = "local variable"
```

4. 控制流程
```
控制语句（Lua没有++或是+=这样的操作）
while循环#######
sum = 0
num = 1
while num <= 100 do
    sum = sum + num
    num = num + 1
end
print("sum =",sum)
if-else分支#######
if age == 40 and sex =="Male" then
    print("test one")
elseif age > 60 and sex ~="Female" then
    print("test two!")
elseif age < 20 then
    io.write("test three\n")
else
    local age = io.read()
    print("Your age is "..age)
end
上面的语句不但展示了if-else语句，也展示了
1）“～=”是不等于，而不是!=
2）io库的分别从stdin和stdout读写的read和write函数
3）字符串的拼接操作符“..”
另外，条件表达式中的与或非为分是：and, or, not关键字。
for 循环#######
从1加到100
sum = 0
for i = 1, 100 do
    sum = sum + i
end
从1到100的奇数和
sum = 0
for i = 1, 100, 2 do
    sum = sum + i
end
从100到1的偶数和
sum = 0
for i = 100, 1, -2 do
    sum = sum + i
end
until循环#######
sum = 2
repeat
   sum = sum ^ 2 --幂操作
   print(sum)
until sum >1000
```
