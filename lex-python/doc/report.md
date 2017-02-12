1、对PL\0文法中各类单词分类：

  （1）保留字：const、var、procedure、begin、end、if、then、while、do、read、call、write、writeln

  （2）常数：由0-----9这几个数字组成

  （3）标识符：由字母打头的字母和数字的字符串

  （4）运算符：+，-，*，/，:=，>=，<=，#

  （5）分界符：；

  2、将各类单词对应到lex中：

  （1）保留字：

reservedWord [const|var|procedure|begin|end|if|then|while|do|read|call|write|writeln]，由于在lex中不区分大小写，所以将保留字写成：

reservedWord [cC][oO][nN][sS][tT]|[vV][aA][rR]|[pP][rR][oO][cC][eE][dD][uU][rR][eE]|

[bB][eE][gG][iI][nN]|[eE][nN][dD]|[iI][fF]|[tT][hH][eE][nN]|[wW][hH][iI]

[lL][eE]|[dD][oO]|[rR][eE][aA][dD]|[cC][aA][lL][lL]|[wW][rR][iI][tT][eE]

[wW][rR][iI][tT][eE][lL][nN]

  （2）常数：

constant ([0-9])+  /*0---9这几个数字可以重复*/

  （3）标识符：

      identfier [A-Za-z]([A-Za-z][0-9])*

  （4）运算符：

      operator \+|-|\*|\/|:=|>=|<=|#|=  /*在lex中，有特殊意义的运算符要加转义字符\，如+、*及*、/

  （5）分界符：

      delimiter [,\.;]

  3、PL/0的语言的词法分析器要求跳过分隔符（如空格，回车，制表符），对应的lex定义为：

     delim [""\n\t]

whitespace{delim}+

  4、为lex制定一些规则：

     {reservedWord}{count++;printf("\t%d\t(1,‘%s’)\n",count,yytext);}   /*对保留字定规则，输出设置*/

     {operator} {count++;printf("\t%d\t(2,‘%s’)\n",count,yytext); }

     {delimiter}{count++;printf("\t%d\t(3,‘%s’)\n",count,yytext);}

{constant}{count++;printf("\t%d\t(4,‘%s’)\n",count,yytext);}

{identfier}{count++;printf("\t%d\t(5,‘%s’)\n",count,yytext);}

{whitespace} {/* do    nothing*/ }         /*遇到空格，什么都不做*/




----
## 实现思路
- **[方案一，弃用]**
1. 给定正则表达式进行解析
2. 最后对每个正则表达式生成一个DFA二维字典，行为状态，列为字典元素，dic['word']的值为通过这个边的下一个状态是什么，若达到总结点，则翻译成功
3. 如果某个字典翻译失败，尝试下一个字典DFA，一直到尝试完成所有的DFA，如果都不行，则这个字符串无法成功翻译，抛出错误。
4. 不同表达式要兼容，如何兼容？有优先级的概念
5. 不同的正则表达式有嵌套的概念，需要在字典中体现这个嵌套
6. 贪婪匹配原则，一直匹配到不能匹配为止
7. 你需要为每个终结节点给定标号和优先级，用于避免终结点重合

'3.'步骤需要重复重新执行每一个DFA，造成大量的时间浪费，应该想办法更好的归并不同的DFA，以达到更高效的语法翻译

- **[方案二]**
----
 多个DFA构造的算法调整
 - 为每个正则表达式构造NFA，并标记每个正则表达式的终结符，需要标记两个信息：
     - 正则表达式标号
     - 优先级
 - 将多个NFA用或的方式合并；
 - 通过求闭包和子状态扩展两个方案，进行NFA到DFA的转换，过程需要做一个调整的是：
    - 每一个正则表达式给定一个优先级，状态拓展的时候，如果发现有多个终结符号，取优先级最高的那个
 - 构造化简的DFA：
    - 构造弱等价类，但是不能把不同终结点归为同一个弱等价类
 - 根据最后DFA生成查询字典，
    - 这个字典是一个二维字典，第一个维度的key表达的是当前的状态位
    - 字典的第二个维度的key表达的是某一个状态位下的边，而value表达的是经过这个边[key]，到达的新的状态位
    - 贪婪原则：需要匹配到无法继续匹配[某个状态位没有接下来的key]为止
    - 遍历的过程需要记录成功匹配的正则表达式队列
      - 如果匹配多个
        - 优先级不同，按照优先级最高的
        - 优先级相同，按照最先匹配到的

## 项目架构[为之后实现lex做准备]
- main.py
  - 调用match函数
- global_value.py
  - DFA_hash_dictory.
  - reg_map：表达式和优先级，负载信息的对应关系
- match.py
  - 获取下一个读入字符
  - 为每次匹配构造成功匹配栈
  - 循环调用字典，直到某个字符没有对应的后继状态 
    - 循环过程中记录匹配成功的字符串和对应的配对表达式编号
  - 通确定当前应该选用的正则表达式，
  - 输出对应信息

## 可做的改进工作：
  - 字典的改进，可以对优化后的DFA的状态进行重新排布，这样字典的第一个维度就可以简单的使用数组下标表示，而不用使用key，节约存储空间
## 简化说明：
  - 为了表达方便，试验中做的两个化简操作
  - 在DFA中使用了 <=,otherletter, letter 这种不规范的表达‘

## [todo]:
  - i38,i33应该合并，
  - e23 应该有一个自己链接自己的环
  - 空格符应该有自己的环 '=':'e7',需要和 == 归并
##　实验拓展：构造lex——如何自动生成DFA_hash_dictory.
  1. 构造正则表达式解析树
    http://blog.csdn.net/chinamming/article/details/17175073
    符号：
      二元：|,.,(),[],{}
      单元：+，*
    其他定义为字符
    先看到成分，再看到连接符号
  2. 构造解析数，转化成后缀正则表达式
  3. 由后缀正则表达式构造NFA
  4. 由NFA构造DFA[求闭包和子集，合并状态]
  5. 优化DFA
  6. 根据DFA生成状态转换图字典


---

确定要使用的语法：


关键字：
if if
then then
while while
do do

操作符：
operator \+|-|\*|\/|=
relation_op >=|<=|==|!=

空白符：
delim [ \n\t] 
whitespace {delim}+ 

分隔符：
delimiter [,;]
block [{}]
brackets [\(\)]

数字：
digit = [0-9]
constant ({digit})+

标识符：
letter [A-Za-z]
identfier {letter}(letter|{digit})*

类型变量:
type [int|float]

确定可以解析的正则表达式：
[]内部或关系
\转义字符，
  \n
  \t
  \(
  \)
  \{
  \}
{}
1. 块操作符，右边可以使用：*,+,{n,m}三种表达，如果为其他，就理解为

