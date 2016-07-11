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

lua -i

```

## run
----------
```
shell#lua5.3
Lua 5.3.1  Copyright (C) 1994-2015 Lua.org, PUC-Rio
>print("hello world")       #Lua脚本的语句的分号是可选的,这个和GO语言很类似.

or 
shell#lua32 hello.lua

or chmod +x hello.lua
#lua ./hello.lua
or add "#!/usr/local/bin/lua"
#./hello.lua
```

## syntax
----------
1. comments --行注释, --[[ 块注释 --]]
2. add `#!/usr/local/bin/lua` in lua
3. 变量 
``` 
全局变量:所有的变量默是全局除非显式地声明为局部.
局部变量:当类型被指定为局部的一个变量,它的范围是有限的在自己的范围内使用.
表字段:这是一种特殊类型的变量,可以除了nil,包括功能不放任何东西.

Lua的数字只有double型,64bits,你不必担心Lua处理浮点数会慢(除非大于100,000,000,000,000),或是会有精度问题,你可以以如下的方式表示数字,0x开头的16进制和C是很像的.
num = 1024
num = 3.0
num = 3.1416
num = 314.16e-2
num = 0.31416E1
num = 0xff
num = 0x56
字符串你可以用单引号,也可以用双引号,还支持C类型的转义,比如: '\a' (响铃), '\b' (退格), '\f' (表单), '\n' (换行), '\r' (回车), '\t' (横向制表), '\v' (纵向制表), '\\' (反斜杠), '\"' (双引号), 以及 '\" (单引号)
下面的四种方式定义了完全相同的字符串(其中的两个中括号可以用于定义有换行的字符串)
a = 'alo\n123"'
a = "alo\n123\""
a = '\97lo\10\04923"'
a = [[alo
123"]]
C语言中的NULL在Lua中是nil,比如你访问一个没有声明过的变量,就是nil,比如下面的v的值就是nil
v = UndefinedVariable
布尔类型只有nil和false是 false,数字0啊,''空字符串('\0')都是true!
另外,需要注意的是:lua中的变量如果没有特殊说明,全是全局变量,那怕是语句块或是函数里.变量前加local关键字的是局部变量.
theGlobalVar = 50
local theLocalVar = "local variable"

local d, f = 5, 10  --declaration of d and f as local variables.
d, f = 5, 10;       --declaration of d and f as global variables.
d, f = 10           --[[declaration of d and f as global variables. Here value of f is nil --]]
```
4. 数据类型
```
Lua是动态类型语言,所以变量没有类型,仅值有类型.值可以被存储在变量中,作为参数传递,并作为结果返回
值类型      描述
nil         用于区分具有一些数据或没有(nil)数据的值.
boolean     包括true和false值.一般用于条件检查.
number      表示真实(双精度浮点数)的数字.
string      表示字符数组.
function    表示是用C或Lua语言的方法.
userdata    表示任意C数据.
thread      独立的执行线程,它是用来实现协程.
table       代表普通数组,符号表,集合,记录,图,树等,并实现关联数组.它可以容纳任何值(除了nil).

```

5. 控制流程
```
控制语句(Lua没有++或是+=这样的操作)
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
上面的语句不但展示了if-else语句,也展示了
1)"~="是不等于,而不是!=
2)io库的分别从stdin和stdout读写的read和write函数
3)字符串的拼接操作符".."
另外,条件表达式中的与或非为分是:and, or, not关键字.
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

5. 函数
```
Lua的函数和Javascript的很像
递归
function fib(n)
  if n < 2 then return 1 end
  return fib(n - 2) + fib(n - 1)
end
闭包,同样,Javascript附体!
示例一
function newCounter()
    local i = 0
    return function()     -- anonymous function
       i = i + 1
        return i
    end
end
c1 = newCounter()
print(c1())  --> 1
print(c1())  --> 2
示例二
function myPower(x)
    return function(y) return y^x end
end
power2 = myPower(2)
power3 = myPower(3)
print(power2(4)) --4的2次方
print(power3(5)) --5的3次方
函数的返回值
和Go语言一样,可以一条语句上赋多个值,如:
name, age, bGay = "haoel", 37, false, "haoel@hotmail.com"
上面的代码中,因为只有3个变量,所以第四个值被丢弃.
函数也可以返回多个值:
function getUserInfo(id)
    print(id)
    return "haoel", 37, "haoel@hotmail.com", "http://coolshell.cn"
end
name, age, email, website, bGay = getUserInfo()
注意:上面的示例中,因为没有传id,所以函数中的id输出为nil,因为没有返回bGay,所以bGay也是nil.
局部函数
函数前面加上local就是局部函数,其实,Lua中的函数和Javascript中的一个德行.
比如:下面的两个函数是一样的:
function foo(x) return x^2 end
foo = function(x) return x^2 end
```
