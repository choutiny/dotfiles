reStructuredText
==============
[RST doc](http://docutils.sourceforge.net/docs/user/rst/quickstart.html)

### command
-----------
.rst
`rst2html`

### grammer
-----------
```
标题(Title)
来看看标题的实例:

code
    - 这里是列表的第一个列表项

    - 这是第二个列表项

    - 这是第三个列表项

      - 这是缩进的第一个列表项
        注意,这里的缩进要和当前列表项的缩进同步.

    - 第一级的第四个列表项

    - 列表项之间要用个空格来分割.

    ===================
    这就是一个标题
    ===================

    ----------------
    这也是一个章节标题
    ----------------

怎么样,看起来不难吧,你只要按这个写法,就能被reStructuredText认识,并被解释为章节标题.reStructuredText可用于作为标题修饰的字符有很多很多:
! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~
只要你想,上面的任意一个都可以用来作为标题的修饰符,当然,reStructuredText也是有推荐的,它推荐下面这些字符:
= - ` : . ' " ~ ^ _ * + #
这些字符是上面一堆字符中稍微看起来不会那么奇怪的一部分,当然,个人建议不要那么花哨,尽量用这两个中的一个:
= -
上面实例的写法也许有点复杂,.rst文件中,你还可以只给出下半部分的字符即可:

code
    这个标题和上面的一样
    ===================
TIPS:作为修饰的字符长度要大于等于文字长度.另外,标题是能够嵌套的.


段落(Paragraphs)
段落一般隶属于某个章节中,是一块左对齐并且没有其他元素体标记的块.在.rst文件中,段落和其他内容的分割是靠空行来完成,如果段落相较于其他的段落有缩进,reStructuredText会解析为引用段落,样式上有些不同.
code
这里是一段reStructuredText的内容,它可以很长很长....最后,末尾留出空行表示是本段落的结束即可.
 
这里是另外一段reStructuredText的内容,这段内容和上一段之间,乃至后面的其他内容之间都要留出空行进行分割.
 
    这个也是段落,当时由于缩进了,会变成引用段落.显示和直接的段落有点不同
 
列表(List)
列表在HTML中被分为两种,一个是有序列表(Enumerated Lists),一种是无序列表(Bullet Lists),在reStructuredText中,我们也能找到这两种列表,还有一种称为定义列表(Definition Lists),这和HTML中的DL一样,在.rst文件中可以支持嵌套列表.
无序列表要求文本块是以下面这些字符开始,并且后面紧跟空格,而后跟列表项的内容,其中列表项比趋势左对齐并且有与列表对应的缩进.
    * + - • ‣ ⁃
还是那句话,用最常用的几个字符就好,不用那么花哨.下面是示例:
code
    - 这里是列表的第一个列表项

    - 这是第二个列表项

    - 这是第三个列表项

      - 这是缩进的第一个列表项
        注意,这里的缩进要和当前列表项的缩进同步.

    - 第一级的第四个列表项

    - 列表项之间要用个空格来分割.
有序列表在格式上和无序列表差不多,但是在使用的前缀修饰符上,使用的不是无序列表那种字符,而是可排序的字符,可以识别的有下面这些:

arabic numerals: 1, 2, 3, ... (no upper limit).
uppercase alphabet characters: A, B, C, ..., Z.
lower-case alphabet characters: a, b, c, ..., z.
uppercase Roman numerals: I, II, III, IV, ..., MMMMCMXCIX (4999).
lowercase Roman numerals: i, ii, iii, iv, ..., mmmmcmxcix (4999).
如果你不想使用这些,在你标明第一个条目的序号字符后,第二个开始你还可以使用"#"号来让reStructuredText自动生成需要的序号(Docutils >= 0.3.8).

code
    1. 第一项
        巴拉巴拉好多内容在这里...

    #. 第二项

        a. 第二项的第一小项

        #. 第二项的第二小项

    #. 第三项

定义列表:每个定义列表项里面包含术语(term),分类器(classifiers,可选), 定义(definition).术语是一行文字或者短语,分类器跟在术语后面,用" : "(空格,冒号,空格)分隔.定义是相对于术语缩进后的一个块.定义中可以包含多个段落或者其他的内容元素.术语和定义之间可以没有空行,但是在定义列表前后必须要有空行的存在.下面是示例:
code
    术语1
        术语1的定义

    术语 2
        术语2的定义,这是第一段

        术语2的定义,第二段

    术语 3 : 分类器
        术语3的定义


    术语 4 : 分类器1 : 分类器2
        术语4的定义
 TIPS:在reStructuredText中,还有两种列表,一种是字段列表(Field Lists),一种是选项列表(Option Lists).由于是rst的语法入门教程,这里不做深入介绍

表格(Table)
reStructuredText提供两种表格:网格表格(Grid Tables), 简单表格(Simple Tables).

网格表中,共使用的符号有:
    - = | +
"-" 用来分隔行, "=" 用来分隔表头和表体行,"|" 用来分隔列,而"+"用来表示行和列相交的节点,如下面的例子:
code
    +------------------------+------------+----------+----------+
    | Header row, column 1   | Header 2   | Header 3 | Header 4 |
    | (header rows optional) |            |          |          |
    +========================+============+==========+==========+
    | body row 1, column 1   | column 2   | column 3 | column 4 |
    +------------------------+------------+----------+----------+
    | body row 2             | Cells may span columns.          |
    +------------------------+------------+---------------------+
    | body row 3             | Cells may  | - Table cells       |
    +------------------------+ span rows. | - contain           |
    | body row 4             |            | - body elements.    |
    +------------------------+------------+---------------------+
 
来自docutils的帮助文档.
 TIPS:表头行是可选的,如果你不需要,就可以不用"="来分割了.

简单表格:这种表格比网格表来说简单许多,一般用于简单的数据展示.其用于修饰的字符也仅两个而已:
    = -
一般用"="就能完成简单表格的绘制,如果有表头,同样需要用"="将它和表体(body)内容分开,否则会被视为无表头数据.
code
    基本形式
    ========

    `下面这种是最简单的表格形式,当然你也可以去掉表头展示.`

    =====  =====  =======
      A      B    A and B
    =====  =====  =======
    False  False  False
    True   False  False
    False  True   False
    True   True   True
    =====  =====  =======

    表内嵌入
    ========

    `下面这种简单表内有列表`

    =====  =====
    col 1  col 2
    =====  =====
    1      Second column of row 1.
    2      Second column of row 2.
           Second line of paragraph.
    3      - Second column of row 3.

           - Second item in bullet
             list (row 3, column 2).
    \      Row 4; column 1 will be empty.
    =====  =====

    表头合并
    ========

    `表头进行分类合并`

    =====  =====  ======
       Inputs     Output
    ------------  ------
      A      B    A or B
    =====  =====  ======
    False  False  False A
    True   False  True
    False  True   True
    True   True   True
    =====  =====  ======
 TIPS:列需要和"="左对齐,不然可能会导致出错;如果碰到第一列为空时,需要使用"\"来转义,不然会被视为是上一行的延续;网格表和简单表中,简单表比较适合展现简单的数据,这些数据本身不需要太复杂的展现形式,而一旦碰到需要和并单元格这类的复杂操作,可能网格表会更加适合.
表格中还有更复杂的表格形式,比如:CSV表格,列表表格.这些复杂的格式就留给有兴趣的朋友深入吧.

块(Blocks)
块在reStructuredText中的表现方式也有好几种,但是最常见的是文字块(Literal Blocks).这种块的表达非常简单,就是在前面内容结束之后,用两个冒号" :: "(空格[Optional],冒号,冒号)来分割,并在之后紧接着插入空行,而后放入块的内容,块内容要相对之前的内容有缩进.
code
    这里是块之前的的内容...::

        这里是块的内容.前面有缩进,空行,和::分隔符.
        此处内容会被一直视为块内容

        空行也不能阻断块内容..

    但是,当内容像这样,不再和块内容一样缩进时,块内容就自动的结束了.

这是块的最简单方式,一般我们编写的代码块就是用这种方式表现(如下), 除此之外,.rst还有引用文字块(Quoted Literal Blocks),行块(Line Blocks),块引用(Block Quotes)等.

code
    下面是我们的测试代码:
    ::
 
        for i in [1,2,3,4,5]:
            print i
        # 代码块测试
 
很简单的代码块测试. 更多的块内容,请参阅官方帮助文档.


样式(Style)
reStructuredText中支持对文本进行样式控制,比如:粗体(Strong),斜体(Italic),等宽字体(Monospace),引用( interpreted text).
code
    .. Strong Emphasis

    This is **Strong Text**. HTML tag is strong.粗体

    .. Italic, Emphasis

    This is *Emphasis* Text.这个HTML使用em, 斜体

    .. Interpreted Text

    This is `Interpreted Text`. 注意,这个HTML一般用<cite>表示

    .. Inline Literals

    This is ``Inline Literals``. HTML tag is <tt>. 等宽字体.
 
来点补充,如果你需要在文档中插入超链接,那么你可以像下面这样:
code
    我这里是一个 链接_.

    .. _链接: http://blog.useasp.net

这种方式要求定义链接,而后引用链接.而且链接要有空格分隔前面的文字.这种方式略嫌麻烦,你可以用更加简化的方式--个人比较推荐:
code
    这里同样是一个 `链接<http://blog.useasp.net>`_,不需要特别设置.

TIPS: 我们会发现,两个处理连接的时候,都需要在链接文字前面要空格与前面进行分割,这个在英文当中比较好处理,因为单个词之间有空格,而在中文中,字之间没有空格,如果加入空格,在显示时会有空格,影响观感,为此,如果在中文中使用,需要考虑好.
```

```
段落 Paragraphs
段落( 参考 )是 reST 文章中最常见的文本块. 段落是由一个或多个空白分隔的文本块. 同Python中的约定,在 reST 中使用缩进来标识, 因此, 所有同级段落,必须左对齐,使用同级缩进.

行内标记 Inline markup
标准的reST 行内标记很简单:

单星号: *文本* 得 强调 (斜体 对中文一般效果不好) ,
双星号: **文本** 得 加重 (加黑),
反引号: ``文本`` 得 代码引用.
If asterisks or backquotes appear in running text and could be confused with inline markup delimiters, they have to be escaped with a backslash.

如果有星号或反引号出现在引用的文本, 就可能会弄乱内联标记分隔符,这时,可以用反斜杠来转义.

Be aware of some restrictions of this markup: 以下是知道这些标记的一些限制:

不可叠用
前后不能用空格: * text* 这样会出错,
必须和周围文字用非单词隔离, 一般使用转义空白来完成: thisis\ *one*\ word
These restrictions may be lifted in future versions of the docutils. docutils未来版本中,可能取消这些限制.

reST also allows for custom "interpreted text roles"', which signify that the enclosed text should be interpreted in a specific way. Sphinx uses this to provide semantic markup and cross-referencing of identifiers, as described in the appropriate section. The general syntax is :rolename:`content`.

reST 也支持自定"文本诠释规则", 这意味着,任意由指定字符封闭的文本都可以用特定的方式来诠释. Sphinx 就用这种形式来提供语义标记和交叉引用, 一般语法形如: :规则名:`内容`

Standard reST provides the following roles: 标准 reST 提供以下规则:

emphasis – *emphasis* 的替代拼写
strong – **strong** 的替代拼写
literal – ``literal`` 的替代拼写
subscript – 下标
superscript – 上标
title-reference – 书籍/期刊/及其他材料的标题
参考: Inline markup Sphinx 追加的规则

列表和引用块 Lists and Quote-like blocks
List markup (ref) is natural: just place an asterisk at the start of a paragraph and indent properly. The same goes for numbered lists; they can also be autonumbered using a # sign:: 列表标记(参考): 只要自然的在段落的开始放置一个星号并正确缩进. 这同样适用于带编号的列表; 也可以使用``#``签署自动编号:

* This is a bulleted list.
* It has two items, the second
  item uses two lines.

1. This is a numbered list.
2. It has two items too.

#. This is a numbered list.
#. It has two items too.
Nested lists are possible, but be aware that they must be separated from the parent list items by blank lines:

嵌套的列表是允许的但必须用空行同父列表分离开:

* this is
* a list

  * with a nested list
  * and some subitems

* and here the parent list continues
定义列表(参考) 如下创建:

term (up to a line of text)
   Definition of the term, which must be indented

   and can even consist of multiple paragraphs

next term
   Description.
Note that the term cannot have more than one line of text. 注意, 条目本身不能多行.

Quoted paragraphs (ref) are created by just indenting them more than the surrounding paragraphs. 创建引用段落 (参考)只需要用缩进和其它段落区分即可.

线块 (ref) 是保留换行符的一种方法:

| These lines are
| broken exactly like in
| the source file.
还有其它特殊文本块形式是支持的:

字段列表 (field lists 参考)
选项列表 (option lists 参考)
引述文本块 (quoted literal blocks 参考)
文本测试块 (doctest blocks 参考)
源代码 Source Code
代码文本块 (参考) 由末尾是特殊标记 :: 的段落引发. 整个代码文本块必须缩进 (同所有的段落一样,使用空白行和周围文本完成分隔):

This is a normal text paragraph. The next paragraph is a code sample::

   It is not processed in any way, except
   that the indentation is removed.

   It can span multiple lines.

This is a normal text paragraph again.
:: 标记是智能处置的:

如果作为一个独立段落出现,则和其它文本完全隔离
如果它紧跟有空格,则将被删除不起作用
如果它在非空白字符之前,则替换为普通的单一冒号
综上,前述示例中的第二段代码引用文本之前的一句会渲染为 "The next paragraph is a code sample:"

That way, the second sentence in the above example's first paragraph would be rendered as "The next paragraph is a code sample:".

表格 Tables
支持两种表格.

网格表 (参考), 你不得不自行"绘制"表格的边框.看起来象这样:

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | ...        | ...      |          |
+------------------------+------------+----------+----------+
简单表 (参考) 容易点,

但是有限制:至少要有一列,而且,第一行不能包含多行文本, 看起来象这样:

=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======
超链接 Hyperlinks
外部链接 External links
Use `Link text <http://example.com/>`_ for inline web links. If the link text should be the web address, you don't need special markup at all, the parser finds links and mail addresses in ordinary text.

用 `Link text <http://example.com/>`_ 来记录行内链接. 如果文字本身就是链接, 那不用作任何标记,解析器可以自动将链接和邮箱地址转换为超链接.

也可以单独定义链接目标用引用(参考),比如:

This is a paragraph that contains `a link`_.

.. _a link: http://example.com/
内部链接 Internal links
Internal linking is done via a special reST role provided by Sphinx, see the section on specific markup, Cross-referencing arbitrary locations.

Sphinx 使用特殊 reST 规则支持内部链接, 详细参考 定义规则

章节 Sections
Section headers (ref) are created by underlining (and optionally overlining) the section title with a punctuation character, at least as long as the text:

章节头部 (参考) 由下线(也可有上线)和包含标点的标题 组合创建, 其中下线要至少等于标准文本的长度:

=================
This is a heading
=================
注意

中文标题的问题

在多数编辑器中,全角/半角中文/标点和E文字符的长度是完全没谱的, 所以,多数情况下,为保持一致性,译者建议统一使用固定长度的上下标线; 比如说78.

Normally, there are no heading levels assigned to certain characters as the structure is determined from the succession of headings. However, for the Python documentation, this convention is used which you may follow: 通常并没有对标题的层级指定明确的标线字符. 不过,对于 Pyhton 文档,可以使用如下约定:

# 有上标线, 用以部分
* 有上标线, 用以章节
=, 用以小节
-, 用以子节
^, 用以子节的子节
", 用以段落
Of course, you are free to use your own marker characters (see the reST documentation), and use a deeper nesting level, but keep in mind that most target formats (HTML, LaTeX) have a limited supported nesting depth.

当然,你可以自由的使用你自定的标识字符(参考 reST 文档), 并使用更加深的嵌套层次, 不过,考虑到兼容多种输出格式(HTML, LaTeX) 最好限制嵌套的深度.

提示

标题层次体验

从行文来说,结构化文本组织的文章,更加关注局部文本的结构清晰, 以整个图书来说,不建议设定太多的标题级别,一般而言**四级**足够了.

直解标记 Explicit Markup
"Explicit markup" (ref) is used in reST for most constructs that need special handling, such as footnotes, specially-highlighted paragraphs, comments, and generic directives.

"直解标记" (Explicit markup, 参考) 用以 reST 中需要特殊处理的各种内容, 如脚注,特殊高亮段落,注释,以及通用指令.

An explicit markup block begins with a line starting with .. followed by whitespace and is terminated by the next paragraph at the same level of indentation. (There needs to be a blank line between explicit markup and normal paragraphs. This may all sound a bit complicated, but it is intuitive enough when you write it.)

直解标记块由``..``开始,紧后跟空格以及跟随的同缩进的文本块. (和正文间要有空白行来明确的加以区分. 可能听起来有点复杂,但当你书写时就能直观的体验到)

指令 Directives
A directive (ref) is a generic block of explicit markup. 指令(ref)就是一个标准的明确标记(Explicit Markup)块. Besides roles, it is one of the extension mechanisms of reST, and Sphinx makes heavy use of it. 除了规则,它是reST 的又一个扩展机制, Sphinx 大量使用了指令.

Docutils 支持以下指令:

警示 Admonitions: attention, caution, danger, error, hint, important, note, tip, warning and the generic admonition. (多数样式目前仅支持 "note" 和 "warning" 好在都有针对的对象ID,很容易使用CSS进行定制 .)

图像 Images:

image (参考后面的 Images_ )
figure (配有标题和图例 的图片)
其它行文元素 Additional body elements:

contents (对诸如 本地文件 的内容表单)
container (配有定制 class 的容器,以便生成HTML 中的 <div> )
rubric (没有到相对段落关系的标题 a heading without relation to the document sectioning)
topic, sidebar (特殊高亮的正文元素 special highlighted body elements)
parsed-literal (支持内嵌标记的文本块)
epigraph (有可选归属行的引用文本块)
highlights, pull-quote (有他们自己class属性的文本块)
compound (复合段落)
特殊表格 Special tables:

table (有标题的表格)
csv-table (从csv数据生成的表格)
list-table (从列表数据生成的表格)
特殊指令 Special directives:

raw (包括原始文本的目标格式标记 include raw target-format markup)
include (从其它文件引入 reST ) – 在Sphinx, 当给定包含文件的绝对路径时,指令会从源代码目录为起点进行相对路径查找.
class (将 class 属性绑定到下一个元素) [1]
HTML 专用 specifics:

meta (生成 HTML 中的 <meta> 标签)
title (覆盖文件标题)
影响标记 Influencing markup:

default-role (设置新默认规则)
role (创建新规则)
由于这些指令都只能作用到单一文件,所以,更好的使用 Sphinx 的方式是设置 default_role.

不要 使用指令 sectnum, header 和 footer.

Sphinx 增加的指令描述收集在: Sphinx Markup Constructs .

Basically, a directive consists of a name, arguments, options and content. (Keep this terminology in mind, it is used in the next chapter describing custom directives.) Looking at this example, 基本上一个指令由名称,参数,选项和内容组成. (请记住这里提及的几个术语, 它们将在之后章节描述自定义指令) 从这个例子来看,:

.. function:: foo(x)
              foo(y, z)
   :module: some.module.name

   Return a line of text input from the user.
function 是指令名, 在头两行里给出了两个参数, 紧接着给出了一个 module 选项 (正如你所见,由冒号标明的 module 之后立即跟上参数) 选项​​必须缩进和指令内容有相同的缩进.

该指令的内容则是由一个空行和同样的缩进来接上.

图片 Images
reST 支持图片指令 (ref), 这样使用:

.. image:: gnu.png
   (options)
在Sphinx 中使用时, 给入的文件名 (此处是 gnu.png) 必须是相对源文件目录的路径, 如果给的是绝对路径形式,也意味着对源文件顶层目录进行相对查找. 比如说, 文件 sketch/spam.rst 可以用路径 ../images/spam.png 或 /images/spam.png. 来引用图片 images/spam.png

Sphinx will automatically copy image files over to a subdirectory of the output directory on building (e.g. the _static directory for HTML output.) Sphinx 会自动将图片复制到构筑输出目录中的相关子目录 (e.g. HTML输出时的 _static 目录.)

Interpretation of image size options (width and height) is as follows: if the size has no unit or the unit is pixels, the given size will only be respected for output channels that support pixels (i.e. not in LaTeX output). Other units (like pt for points) will be used for HTML and LaTeX output.

图片尺寸的解释选项 (width 和 height)有如下规约: 如果大小没给任何单位或单位是像素, 输出通道优先使用像素(换言之,非LaTeX输出). 其他单位(如 pt 或是 点) 将被用于HTML和LaTeX输出.

Sphinx extends the standard docutils behavior by allowing an asterisk for the extension Sphinx 扩展了标准 docutils 行为,支持如下的星号指代:

.. image:: gnu.*
Sphinx then searches for all images matching the provided pattern and determines their type. Each builder then chooses the best image out of these candidates. For instance, if the file name gnu.* was given and two files gnu.pdf and gnu.png existed in the source tree, the LaTeX builder would choose the former, while the HTML builder would prefer the latter. Sphinx 会搜索所有匹配所提供模式的图片, 并确定它们的类型. 每个构筑器再从中选择最佳的图片. 例如, 如果给定文件名是 gnu.* , 源代码树中有两个文件 gnu.pdf 和 gnu.png , LaTeX 构筑器会选择前者, HTML 构筑器更倾向于后者.

Changed in version 0.4: 增加了文件名的星号后缀支持.

Changed in version 0.6: 开始支持绝对路径的图片

脚注 Footnotes
and add the footnote body at the bottom of the document after a "Footnotes" rubric heading, like so:: 脚注 (参考), 使用 [#name]_ 来标记位置, 并在文章底部 "Footnotes" 专栏之后追加脚注内容,如下使用:

Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

.. rubric:: Footnotes

.. [#f1] Text of the first footnote.
.. [#f2] Text of the second footnote.
You can also explicitly number the footnotes ([1]_) or use auto-numbered footnotes without names ([#]_). 可以使用确切编号的脚注 (如: [1]_) 或是自动编号(用 [#]_).

引证 Citations
标准 reST 支持引证 (参考) , with the additional feature that they are "global", i.e. all citations can be referenced from all files. Use them like so:: 有额外的功能是 "global", 换言之,引证能从所有文件来引用. 这样使用:

Lorem ipsum [Ref]_ dolor sit amet.

.. [Ref] Book or article reference, URL or whatever.
Citation usage is similar to footnote usage, but with a label that is not numeric or begins with #. 引证 的使用基本和脚注相同, 不过使用的标签不是数字或是以 # 开始.

替换 Substitutions
reST 支持 "替换" (参考), 以 |name| 形式来定义替换的文本或是标记对象. 如脚注,可以在直解标记文本块中声明,形如:

.. |name| replace:: replacement *text*
或是:

.. |caution| image:: warning.png
             :alt: Warning!
详参 reST 替换参考 .

If you want to use some substitutions for all documents, put them into rst_prolog or put them into a separate file and include it into all documents you want to use them in, using the include directive. (Be sure to give the include file a file name extension differing from that of other source files, to avoid Sphinx finding it as a standalone document.)

如果你对所有文件使用一组替换, 把它们置入 rst_prolog 或放入一个单独的文件, 并在所有相关文件中使用 incluse 指令引入, (请将此定义文件,使用和内容文件不同的后缀,否则,Sphinx 将视其为独立文章来尝试解析)

Sphinx defines some default substitutions, see Substitutions. Sphinx 本身有些默认替换,参考 Substitutions .

注释 Comments
所有直解标记文本块都不算有效的标记构成 Every explicit markup block which isn't a valid markup construct (like the footnotes above) is regarded as a comment (ref). For example:

没有有效标记(如脚注)的直解标记文本块就是注释(参考) 例如:

.. This is a comment.
可以用缩进文本来进行多行注释:

..
   This whole indented block
   is a comment.

   Still in the comment.
源文本编码 Source encoding
Since the easiest way to include special characters like em dashes or copyright signs in reST is to directly write them as Unicode characters, one has to specify an encoding. Sphinx assumes source files to be encoded in UTF-8 by default; you can change this with the source_encoding config value.

由于最简单的方式,是在 reST 中将包括特殊字符(如长划线或版权标记)都直接写成Unicode字符. Sphinx 默认假设源文件是 utf-8 编码. 你可以用配置项 source_encoding 来指定别的编码.

嗯嗯嗯 Gotchas
There are some problems one commonly runs into while authoring reST documents: 通常运用 reST 进行撰写时会遇见几个问题:

对在线标记的分隔: 如前所述,内联标记必须用非单词字符和周围的文字进行区隔, 要解决这个问题你必须使用反斜杠转义空格,详见 参考 .
在线标记不能嵌套: 但是形如 *see :func:`foo`* 是没问题的.
Footnotes

[1]	当默认域包含 class 指令时,该指令将被掩蔽, 因此 Sphinx 转而使用 rst-class.
1. 缩进分段
```
