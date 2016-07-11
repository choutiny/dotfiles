apache
========

###List index
----------------
```
DocumentRoor "/home/www"
<Directory "/home/www/">
    Options All indexes FollowSymLinks
    Order allow,deny
    Allow from all
</Directory>
```

### .htaccess
----------------
```
[F] Forbidden(禁止): 命令服务器返回 403 Forbidden错误给用户浏览器
[L] Last rule(最后一条规则): 告诉服务器在本条规则执行完后停止重写URL
[N] Next(下一条规则): 告诉服务器继续重写,指导所有重写指令都执行过
[G] Gone(丢失): 命令服务器返回410 GONE(no longer exists)错误消息
[P] Proxy(代理): 告诉服务器通过mod_proxy模块处理用户请求
[C] Chain(捆绑): 告诉服务器将当前的规则和前面的规则进行捆绑
[R] Redirect(重定向): 命令服务器发出重定向消息,以便用户浏览器发出rewritten/modified(重写/修改)URL的请求
[NC] No Case(不区分大小写): 对客户端请求的URL不区分大小写
[PT] Pass Through(放行): 让mod_rewrite模块将重写的URL传回给Apache做进一步处理
[OR] Or(逻辑或): 用逻辑"或"将两个表达式连接在一起,如果结果为"真",则会应用后继的相关规则
[NE] No Escape(禁用转义): 命令服务器在输出时禁用转义字符
[NS] No Subrequest(禁用子请求): 如果存在内部子请求,则跳过当前命令
[QSA] Append Query String(追加查询字符串): 命令服务器在URL末尾追加查询字符串
[S=x] Skip(跳过): 如果满足某指定的条件,则跳过后面第x调规则
[E=variable:value] Environmental Variable(环境变量): 命令服务器将值value赋给变量variable
[T=MIME-type] Mime Type(MIME类型): 声明目标资源所属的MIME类型
[] 匹配一个字符集合,例如[xyz]可以匹配x, y或者z
[]+ 例如[xyz]+会以任何顺序,次数匹配x,y,z的出现
[^] 字符^表示字符集的补集.[^xyz]将匹配没有x,y或者z的字符串
[a-z] 连字符(-)表示匹配从字母a到字母z的所有字符串
a{n} 指定字母a出现的次数为n次,满足该条件时匹配.例如x{3}仅与xxx匹配
a{n,} 指定字母a出现的次数至少为n次,例如x{3,}可以与xxx或者xxxx等匹配
a{n,m} 指定a出现的次数至少为n到m次.
() 用于将正则表达式分组,满足第一组正则表达式的字符串会被存储在变量$1中,以此类推.如果括号中的不是正则表达式,例如(perishable)?press 将能够匹配有或者没有perishable前缀的press
^ 位于行首.注意:和中括号中的[^]意义不同.
$ 位于行末
? 例如 monzas? 会匹配 monza 或者 monzas,而 mon(za)? 会匹配 mon 或者 monza.又如 x? 会匹配"空字符" 或者 一个x
! 逻辑非.例如"!string" 将会匹配除了"string"以外的所有字符串
. 表示任意字符串
- 命令Apache"不要"重写URL,例如"xxx.domain.com.* – [F]"
+ 匹配至少一个任意字符,例如G+匹配以G开头,并且后面至少有一个字符的字符串
* 匹配零个或多个字符,例如".*"匹配任意字符串
| 逻辑"或",与[OR]不同的是,它只匹配字符串,例如(x|y)匹配x或者y
\ 转义字符.可以转义左括号( 尖字符^ 美元符号$ 感叹号! 点. 星号* 管道符号| 右括号) 等
\. 转义为点字符(点字符在正则表达式中可以匹配任意字符)
/* 零个或多个正斜杠
.* 零个或多个任意字符(即,匹配任意字符串,包括空字符)
^$ 匹配"空字符","空行"
^.*$ 匹配任意字符串(仅限一行)
[^/.] 匹配既非"正斜杠"也不是"点"的任意字符
[^/.]+ 匹配第一个字符既非"正斜杠"也不是"点",后继字符可以是"正斜杠"或者"点"的字符串
http:// 匹配"http://"
^domain.* 匹配以"domain"开始的字符串
^domain\.com$ 仅匹配"domain.com"
-d 测试字符串是否是已存在的目录
-f 测试字符串是否是已存在的文件
-s 测试字符串所指文件是否有"非零"值

HTTP协议重定向编码

301 – Moved Permanently
302 – Moved Temporarily
403 – Forbidden
404 – Not Found
410 – Gone
```
