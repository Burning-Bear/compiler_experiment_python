# 需要安装的包：
- 要求安装prettytable库，用于格式化输出表格
- Python2.7

# part1. lex词法分析器[未完成]
## 项目文件结构
- FA-based\main.py
  - 调用match函数
- FA-based\global_value.py
  - DFA_hash_dictory 字典，定义了表达DFA的字典
  - reg_map：表达式和优先级，附带信息的对应关系
- FA-based\match.py
  - 获取下一个读入字符
  - 为每次匹配构造成功匹配栈
  - 循环调用字典，直到某个字符没有对应的后继状态 
    - 循环过程中记录匹配成功的字符串和对应的配对表达式编号
  - 通确定当前应该选用的正则表达式，
  - 输出对应信息

## 输入输出示例：
- 输入示例：
在\FA-based\Main.py
的fp = open("text.txt",'r') 可以指定输入文件的路径
```
int main()
{ 
    int a=10;  
    float b,c;      
    c=b+a;
    if (a>=0){
      a = a + 1    
    while b != 0 do
      b = b + c
    }
}
```
- 输出示例：
```
+--------+-------------+---------------------+
| status | origin_char |      infomation     |
+--------+-------------+---------------------+
|  e33   |     int     |         type        |
|  e14   |             |      whitespace     |
|  e24   |     main    |      identfier      |
|  e19   |      (      |       brackets      |
|  e19   |      )      |       brackets      |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e21   |      {      |        block        |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e33   |     int     |         type        |
|  e14   |             |      whitespace     |
|  e24   |      a      |      identfier      |
|   e7   |      =      |       operator      |
|  e23   |      10     |        digits       |
|  e17   |      ;      |      delimiter      |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e24   |    float    |      identfier      |
|  e14   |             |      whitespace     |
|  e24   |      b      |      identfier      |
|  e17   |      ,      |      delimiter      |
|  e24   |      c      |      identfier      |
|  e17   |      ;      |      delimiter      |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e24   |      c      |      identfier      |
|   e7   |      =      |       operator      |
|  e24   |      b      |      identfier      |
|   e7   |      +      |       operator      |
|  e24   |      a      |      identfier      |
|  e17   |      ;      |      delimiter      |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e27   |      if     |      if keyword     |
|  e14   |             |      whitespace     |
|  e19   |      (      |       brackets      |
|  e24   |      a      |      identfier      |
|  e42   |      >=     | relational operator |
|  e23   |      0      |        digits       |
|  e19   |      )      |       brackets      |
|  e21   |      {      |        block        |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e24   |      a      |      identfier      |
|  e14   |             |      whitespace     |
|   e7   |      =      |       operator      |
|  e14   |             |      whitespace     |
|  e24   |      a      |      identfier      |
|  e14   |             |      whitespace     |
|   e7   |      +      |       operator      |
|  e14   |             |      whitespace     |
|  e23   |      1      |        digits       |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e41   |    while    |    while keyword    |
|  e14   |             |      whitespace     |
|  e24   |      b      |      identfier      |
|  e14   |             |      whitespace     |
|  e42   |      !=     | relational operator |
|  e14   |             |      whitespace     |
|  e23   |      0      |        digits       |
|  e14   |             |      whitespace     |
|  e32   |      do     |      do keyword     |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e24   |      b      |      identfier      |
|  e14   |             |      whitespace     |
|   e7   |      =      |       operator      |
|  e14   |             |      whitespace     |
|  e24   |      b      |      identfier      |
|  e14   |             |      whitespace     |
|   e7   |      +      |       operator      |
|  e14   |             |      whitespace     |
|  e24   |      c      |      identfier      |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e21   |      }      |        block        |
|  e14   |             |      whitespace     |
|        |             |                     |
|  e21   |      }      |        block        |
+--------+-------------+---------------------+
```

# part2. LR(1)语法分析器

## 主要工作：
- 根据输入的产生是字符串构造对应的数据结构存储
- 根据输入的token序列构造对应的数据结构存储
- 通过内部状态拓展和状态间拓展，生成对应的状态集 
- 根据状态集构造预测分析表
- 根据预测分析表分析tokens序列，构造程序

## 文件结构：
- \main\Global.py 存储项目中的全局变量，目前只存储了EPSILON = 'e'，这个变量
- \main\Production.py用于将用户定义的产生式信息转化为字符串存储下来
	- Class Token 用于描述文法符号，也就是一个token，包括了token的终结符与否和字符信息
	- Class ProItem 用于描述单个产生式，依赖于Token
	- Class ProductionSet 用于描述用户定义的所有文法产生式的集合
- \main\ParsingTable.py 用于存储构造预测分析表相关的数据结构，包括带dot和预测符的产生式，状态集合：
	- Class LR_produc_item：用于描述一个LR(1)分析过程中每个产生式的状态，它包含了产生式和产生式当前的dot和预测符信息
	- Class Status：记录了一个确定化的状态集合的信息，依赖于LR_produc_item

## 主要算法：
1. **构造分析表**：
	- 首先，main函数中，编写了构造分析表的驱动子函数：
		- 初始化第一个状态processor.init_status()
		- 用于存储待状态拓展的队列：to_extent_queue
		- 状态内拓展，同时将移进项填入分析表：definited_status = processor.closure(value)
		- 状态间拓展：processor.goto(definited_status)
		- 对拓展完毕的状态进行规约，将可规约项填入分析表：processor.regression(definited_status, new_status_id)
		- 重复循环知道无法找到新的队列
	- 状态内扩展：通过main中的processor.closure(status)完成，过程如下：
		- 遍历该状态的所有产生式
		- 判断产生式的状态，如果dot还没到达末尾，并且下一个符号不是终结符，才能进行状态拓展 
		- 内部状态拓展：通过First(βα)计算每个新的产生式和预测符，以下是求first的逻辑：
			- 遍历token作为产生式左边时所能产生的所有产生式
			- 获取这些产生式的first()，如果一个token是非终结符，则将递归调用他的first,将结果加入集合set中
			- 查看这个token对应的first的集合是否存在spsilon，如果存在，继续往下一个token从第一步开始重复循环
			- 否则结束，返回predict_list
	- 状态间拓展：processor.goto(status)
		- 遍历状态中的所有LR产生式
		- 获取产生式的dot的位置，只有还没结尾的产生式，才能进行拓展
		- 将新产生的产生式通过status_dict字典存储，edge是现在的产生式和新的产生式的链接边：status_dict[edge] = Status()，这样的结构是为了方便程序返回后进行状态间拓展的预测分析表的构造
	- 填写规约项：processor.regression(definited_status, new_status_id)
		- 规约程序遍历当前的状态的所有产生式
		- 查看产生式的dot位置
		- 如果产生式的dot已经达到末尾，则对预测分析表填入规约项: self.add_to_parsing_table('r' + str(pro_id), status_id, predict_char)
		
2. **根据预测分析表进行语法分析**：
	预测分析表的语法分析程序在/main/Parsing.py中，使用ParsingProcessor的类来完成，下面是其主要代码：
	- **需要说明的数据结构**：
		- 构造输入流，在结尾加上$：self.input_queue = list(fp.read() + '$')
		- 分析过有两个栈，一个是状态栈，一个是符号栈，初始化栈，状态为0号，符号为$
            self.token_stack= ['$']
            self.status_stack = [0]
		- 用于记录分析过程的list：self.parsing_log = []
		- 传递预测分析表：self.parsing_table = parsing_table
		- 传递产生式表：self.production_list = production_list
	- **主要逻辑过程**：
        - 读取token序列
        - 根据预测分析表查看是否有对应的移进/规约项，如果不存在，则语法分析失败
        - 如果结果是移进项，则将状态压入栈，从预测流读取新的元素
        - 如果是规约项
        - 如果规约项是R0，也就是accept，则翻译结束
        - 如果规约项不是r0，则进行弹栈，移进操作

## 输入输出：
- **输入**
	- 在\main\main.py中
production_fp = open("production.txt",'r') 可以指定输入的语法产生式序列
token_fp = open("input.txt",'r')可以指定输入的token序列
	- 目前项目结构不完善，对于input，有以下的要求:
		- 输入文件有两个，一个是产生式序列，一个是token序列
			- 对于产生式序列：
				- 每个产生式有两行，第一个是产生式信息，第二个需要注明每个产生式的符号是终结符还是非终结符，用T代表终结符，N代表非终结符，如：
				E->E+T
				N->NTN
			- 在我们的实验中，用户的输入的产生式的数据现在只能是分割后的产生式，也就是说，产生式右边文件不要出现|的符号
			- 第一个产生式为零号产生式，也就是说，第一个产生式应该是以下的形式:
			    S->E
			    N->N
			- 用'e'代表epsilon
			- 由于代码结构原因，目前默认每行最后一个元素是’\n’，所以，暂时需要在产生式输入文件的最后一行多一个空行”\n”
			- 对于token序列：需要注明的是，我们的输入仅仅是和产生式对应的token序列，而不是真正的程序源代码
		- 正确的输入示例
```
S->E
N->N
E->E+T
N->NTN
E->T
N->N
T->T*F
N->NTN
T->F
N->N
F->(E)
N->TNT
F->i
N->T
[\n]（注意，这里要多空一行）
```
- **输出**
	- 通过\main\main.py中的
logging.basicConfig(level=logging.INFO,  filename='output.log',  filemode='w')
可以对输出进行重定向，我将输出重定向到了’output.log’中，以下是输出结果
	- 输入示例对应的输出示例：
	- 预测分析表
```
INFO:root:printing the predict parsing table...
 +--------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
| STATUS |  A:$  |  A:)  |  A:(  |  A:+  |  A:*  |  A:i  |  G:E  |  G:T  |  G:F  |
+--------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
| 0      | empty | empty |   s2  | empty | empty |   s1  |   s3  |   s4  |   s5  |
| 1      |   r6  | empty | empty |   r6  |   r6  | empty | empty | empty | empty |
| 2      | empty | empty |   s7  | empty | empty |   s6  |   s8  |   s9  |  s10  |
| 3      |   r0  | empty | empty |  s11  | empty | empty | empty | empty | empty |
| 4      |   r2  | empty | empty |   r2  |  s12  | empty | empty | empty | empty |
| 5      |   r4  | empty | empty |   r4  |   r4  | empty | empty | empty | empty |
| 6      | empty |   r6  | empty |   r6  |   r6  | empty | empty | empty | empty |
| 7      | empty | empty |   s7  | empty | empty |   s6  |  s13  |   s9  |  s10  |
| 8      | empty |  s14  | empty |  s15  | empty | empty | empty | empty | empty |
| 9      | empty |   r2  | empty |   r2  |  s16  | empty | empty | empty | empty |
| 10     | empty |   r4  | empty |   r4  |   r4  | empty | empty | empty | empty |
| 11     | empty | empty |   s2  | empty | empty |   s1  | empty |  s17  |   s5  |
| 12     | empty | empty |   s2  | empty | empty |   s1  | empty | empty |  s18  |
| 13     | empty |  s19  | empty |  s15  | empty | empty | empty | empty | empty |
| 14     |   r5  | empty | empty |   r5  |   r5  | empty | empty | empty | empty |
| 15     | empty | empty |   s7  | empty | empty |   s6  | empty |  s20  |  s10  |
| 16     | empty | empty |   s7  | empty | empty |   s6  | empty | empty |  s21  |
| 17     |   r1  | empty | empty |   r1  |  s12  | empty | empty | empty | empty |
| 18     |   r3  | empty | empty |   r3  |   r3  | empty | empty | empty | empty |
| 19     | empty |   r5  | empty |   r5  |   r5  | empty | empty | empty | empty |
| 20     | empty |   r1  | empty |   r1  |  s16  | empty | empty | empty | empty |
| 21     | empty |   r3  | empty |   r3  |   r3  | empty | empty | empty | empty |
+--------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
```
	- 确定化状态集
```
INFO:root:printing the definited status list...
INFO:root:--------------------------------
INFO:root:|status I0:                    |
INFO:root:|       S->.E,set(['$'])       |
INFO:root:|   E->.E+T,set(['+', '$'])    |
INFO:root:|    E->.T,set(['+', '$'])     |
INFO:root:| T->.T*F,set(['+', '*', '$']) |
INFO:root:|  T->.F,set(['+', '*', '$'])  |
INFO:root:| F->.(E),set(['$', '+', '*']) |
INFO:root:|  F->.i,set(['$', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I1:                    |
INFO:root:|  F->i,set(['+', '*', '$'])   |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I2:                    |
INFO:root:| F->(.E),set(['+', '*', '$']) |
INFO:root:|   E->.E+T,set([')', '+'])    |
INFO:root:|    E->.T,set([')', '+'])     |
INFO:root:| T->.T*F,set([')', '+', '*']) |
INFO:root:|  T->.F,set([')', '+', '*'])  |
INFO:root:| F->.(E),set([')', '+', '*']) |
INFO:root:|  F->.i,set([')', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I3:                    |
INFO:root:|       S->E,set(['$'])        |
INFO:root:|   E->E.+T,set(['+', '$'])    |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I4:                    |
INFO:root:|     E->T,set(['+', '$'])     |
INFO:root:| T->T.*F,set(['+', '*', '$']) |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I5:                    |
INFO:root:|  T->F,set(['+', '*', '$'])   |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I6:                    |
INFO:root:|  F->i,set([')', '+', '*'])   |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I7:                    |
INFO:root:| F->(.E),set([')', '+', '*']) |
INFO:root:|   E->.E+T,set([')', '+'])    |
INFO:root:|    E->.T,set([')', '+'])     |
INFO:root:| T->.T*F,set([')', '+', '*']) |
INFO:root:|  T->.F,set([')', '+', '*'])  |
INFO:root:| F->.(E),set([')', '+', '*']) |
INFO:root:|  F->.i,set([')', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I8:                    |
INFO:root:| F->(E.),set(['+', '*', '$']) |
INFO:root:|   E->E.+T,set([')', '+'])    |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I9:                    |
INFO:root:|     E->T,set([')', '+'])     |
INFO:root:| T->T.*F,set([')', '+', '*']) |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I10:                   |
INFO:root:|  T->F,set([')', '+', '*'])   |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I11:                   |
INFO:root:|   E->E+.T,set(['+', '$'])    |
INFO:root:| T->.T*F,set(['+', '*', '$']) |
INFO:root:|  T->.F,set(['+', '*', '$'])  |
INFO:root:| F->.(E),set(['$', '+', '*']) |
INFO:root:|  F->.i,set(['$', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I12:                   |
INFO:root:| T->T*.F,set(['+', '*', '$']) |
INFO:root:| F->.(E),set(['$', '+', '*']) |
INFO:root:|  F->.i,set(['$', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I13:                   |
INFO:root:| F->(E.),set([')', '+', '*']) |
INFO:root:|   E->E.+T,set([')', '+'])    |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I14:                   |
INFO:root:| F->(E),set(['+', '*', '$'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I15:                   |
INFO:root:|   E->E+.T,set([')', '+'])    |
INFO:root:| T->.T*F,set([')', '+', '*']) |
INFO:root:|  T->.F,set([')', '+', '*'])  |
INFO:root:| F->.(E),set([')', '+', '*']) |
INFO:root:|  F->.i,set([')', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I16:                   |
INFO:root:| T->T*.F,set([')', '+', '*']) |
INFO:root:| F->.(E),set([')', '+', '*']) |
INFO:root:|  F->.i,set([')', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I17:                   |
INFO:root:|    E->E+T,set(['+', '$'])    |
INFO:root:| T->T.*F,set(['+', '*', '$']) |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I18:                   |
INFO:root:| T->T*F,set(['+', '*', '$'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I19:                   |
INFO:root:| F->(E),set([')', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I20:                   |
INFO:root:|    E->E+T,set([')', '+'])    |
INFO:root:| T->T.*F,set([')', '+', '*']) |
INFO:root:--------------------------------
INFO:root:  
INFO:root:--------------------------------
INFO:root:|status I21:                   |
INFO:root:| T->T*F,set([')', '+', '*'])  |
INFO:root:--------------------------------
INFO:root:  
```
	- 分析过程
```
INFO:root:printing the parsing step...
+----+----------------+----------------------+--------------------------------+------------------------------+
| id |  status stack  |     token stack      |             input              |            action            |
+----+----------------+----------------------+--------------------------------+------------------------------+
| 0  |      [0]       |        ['$']         | ['i', '*', 'i', '+', 'i', '$'] |          shift to:1          |
| 1  |     [0, 1]     |      ['$', 'i']      |   ['*', 'i', '+', 'i', '$']    |  regression production:F->i  |
| 2  |     [0, 5]     |      ['$', 'F']      |   ['*', 'i', '+', 'i', '$']    |  regression production:T->F  |
| 3  |     [0, 4]     |      ['$', 'T']      |   ['*', 'i', '+', 'i', '$']    |         shift to:12          |
| 4  |   [0, 4, 12]   |   ['$', 'T', '*']    |      ['i', '+', 'i', '$']      |          shift to:1          |
| 5  | [0, 4, 12, 1]  | ['$', 'T', '*', 'i'] |        ['+', 'i', '$']         |  regression production:F->i  |
| 6  | [0, 4, 12, 18] | ['$', 'T', '*', 'F'] |        ['+', 'i', '$']         | regression production:T->T*F |
| 7  |     [0, 4]     |      ['$', 'T']      |        ['+', 'i', '$']         |  regression production:E->T  |
| 8  |     [0, 3]     |      ['$', 'E']      |        ['+', 'i', '$']         |         shift to:11          |
| 9  |   [0, 3, 11]   |   ['$', 'E', '+']    |           ['i', '$']           |          shift to:1          |
| 10 | [0, 3, 11, 1]  | ['$', 'E', '+', 'i'] |             ['$']              |  regression production:F->i  |
| 11 | [0, 3, 11, 5]  | ['$', 'E', '+', 'F'] |             ['$']              |  regression production:T->F  |
| 12 | [0, 3, 11, 17] | ['$', 'E', '+', 'T'] |             ['$']              | regression production:E->E+T |
| 13 |     [0, 3]     |      ['$', 'E']      |             ['$']              |            accept            |
+----+----------------+----------------------+--------------------------------+------------------------------+
```
