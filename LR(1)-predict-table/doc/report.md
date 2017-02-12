
## LR(1)
   a)Construct LR(1) parsing table based on the CFG
   b)Design the program using LR(1) paring table 


## 数据结构
- 文法产生式数组 production_list
    - example of item in list:
        ["产生式左边","产生式右边"]
    - index： production 的index 代表的就是产生式的编号，我们将他成为id

- 内部状态转换字典：inner_status_dict:
    - key: status 非终结符，是产生式的左边
    - value: value is a list
        - example of tiem in list:
            [origin_produc, origin_produc]
            代表的是这个终结符可以产生的产生式的标号集合

- predict_parsing_table:
    - LR(1) 预测分析表
    - 第一维度是一个数组，数组的内容是一个字典，数组的下标index代表的是确定化的状态号
    - 字典：
        - key：key代表的是读头header的字符串，也就是边的字符
        - value: 
          - 如果是移进项，'s'+id,代表的就是移进的确定化状态编号
          - 如果是规约项，'r'+id代表的就是规约的产生式编号

- to_extension_queue:
状态间拓展使用的是广度优先遍历，这里构造了一个队列，用来存放新产生的确定化状态的标号，以便接下来进行的状态内部拓展

- definited_status_list:
  - 用于记录已经确定化的状态列表，
  - 这是个list，list的下表的含义是确定化的状态
  - list的每一个item是一个Status对象qued

- Status对象，记录了一个确定化状态的全部信息
  - 有一个list，list的每个元素是LR_proudc_item对象

- LR_produc_item对象是在状态图中的每个产生式的状态，他有三个元素：
  - produc_id: 原始产生式的id
  - dot_location: 点当前的位置，记录的是其右边的字符的下表
  - predic_list: 这是一个集合，记录的是其预测符号

## 预测分析表产生算法逻辑：
1. 化简产生式，将其中带有｜ 或号的分割开，
  - 在我们的实验中，用户的input的数据现在只能是分割后的产生式
  - 第一个产生式为零号产生式
  - 'e'代表epsilon
  - 统一去除了结尾的'\n'，需要在产生式最后写入一个\n[也就是多空一行]
2. 状态初始化：
  - 以0号产生式为基础，进行内部状态拓展
    -[call function] 内部状态拓展
  - 把确定化的0号状态记录入definited_status_list 和 to_extend_list.

3. 从to_qextension_record 获取队列最前面的元素，也就是definited_status_list 的下标,设置为current_status_id，然后获得对应的Status对象

4. 给定的Status对象进行状态拓展：
  - 获取Status的每一个产生式，对产生式LR_produc_item 进行操作：
    - 判断产生式是否有下一个状态，也就是 dot_location 是不是已经到头了；
      - [call function] 内部状态拓展
        - 遍历每一个LR_produc_item
          - 如果到头了，用对应的预测符填写规约项
            - predict_table:
              - key = current_status_id
              - value:
                  遍历 LR_produc_item.predict_list, 把里面的每个元素作为字典的key.
                  把'r'+LR_produc_item.produc_id 作为字典的value
        - 如果后面还有字符，说明可以进行内部状态拓展
            - 通过dot_location 找到dot右边的符号，这个符号就是拓展节点产生式的左边，记为left_char
            - 通过inner_status_dict这个字典，找到left_char的所有产生式，
              - 将新的LR_produc_item加入Status.list中
                - item.produc_id = inner_status_dict[left_char][i]
                - item.dot_location = 0
                - item.predic_list = First(production_list[LR_produc_item.produc_id][1][dot_location+1])
                  - [call function] : First:
  - 对status 的状态进行合并

5. 对给定的status 进行状态间扩展
    - new Status_list
  - 获取这个Status的每一个产生式，也就是每一个LR_produc_item
    - 获得这个产生式的下一个字符[char,char_type]
    - LR_produc_item.doc_location += 1
    - Status_list[char].add(LR_produc_item)
  - 将 new_status_list[char] 一个个加入：
    - to_extent_queue:
    - get definited_status_list 's current_index 
    - predict_parsing_table[char] = 's'+current_index

6. First(production) function 的求解：
  result
  if production[0] in terminal:
    return production[0]
  else:
    for char in production:
      for x in inner_status_dict[char]['status_list']
        first = First(production_list[x][1])
        result.append(first)
      if eps not in first:
        break;

## 分析tokens序列
  1. 构造输入流，在结尾加上$
  2. 需要有一个栈，这个栈有两个元素，一个是状态，一个是符号
  3. 初始化栈，状态为0号，符号为$
  4. 获取读头的元素token，获取当前的状态号码为status
  5. 根据预测分析表进行条件判断：
    - 查看parsing_table[status][token]对应的符号，设为 result
    - 如果result 为空，分析失败
    - 如果result 为 移进项，也就是s开头，则获得其移进的项目id，shift_status_id
      - 将[shift_status_id,token]压入栈中，读头读取新的元素
    - 如果result为规约项，也就是r开头
      - 如果规约项为r0,那么翻译成功
      - 否则
        - 根据规约项产生式的长度，弹出对应的栈，的元素，
        - 设规约项左边的符号为token,
        - 根据现在的剩下的栈顶status和新的符号token，求parsing_table[status][token]对应的符号，设为result
        - 因为这里的token为非终结符，所以对应的result一定为移进符号，
        - 将 [result[1],token]压入栈中
        - 产生式规约成功，输出
## 分析程序的数据结构
- 预测分析表：parsing_table
- 二元栈 stack
- 输入记录列表，用于最后的格式化输出
## 项目结构
