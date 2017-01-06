
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
- predict_table:
    - LR(1) 预测分析表
    - 第一维度是一个数组，数组的内容是一个字典，数组的下标index代表的是确定化的状态号
    - 字典：
        - key：key代表的是读头header的字符串，也就是边的字符
        - value: 
          - 如果是移进项，'s'+id,代表的就是移进的确定化状态编号
          - 如果是规约项，'r'+id代表的就是规约的产生式编号
- to_extension_queue:状态间拓展使用的是广度优先遍历，这里构造了一个队列，用来存放新产生的确定化状态的标号，以便接下来进行的状态内部拓展
- 
- definited_status_list:
  - 用于记录已经确定化的状态列表，
  - 这是个list，list的下表的含义是确定化的状态
  - list的每一个item是一个Status对象qued

- Status对象，记录了一个确定化状态的全部信息
  - 有一个list，list的每个元素是LR_proudc_item对象

- LR_produc_item对象是在状态图中的每个产生式的状态，他有三个元素：
  - produc_id: 原始产生式的id
  - dot_location: 点当前的位置，记录的是其右边的字符的下表
  - predic_list: 这是一个列表，记录的是其预测符号

## 算法逻辑：
1. 化简产生式，将其中带有｜ 或号的分割开，
  -　在这次遍历的过程中建立production_list, 和 inner_status_dict 两个数据
  - 构造0号产生式 S' -> S
2. 状态初始化：
  - 以0号产生式为基础，进行内部状态拓展
    -[call function] 内部状态拓展
  - 把确定化的0号状态记录入definited_status_list 和 to_extend_list.
3. 从to_qextension_record 获取队列最前面的元素，也就是definited_status_list 的下标,设置为current_status_id，然后获得对应的Status对象
4. 给定的Status对象进行状态拓展：
  1. 获取Status的每一个产生式，对产生式LR_produc_item 进行操作：
    - 判断产生式是否有下一个状态，也就是 dot_location 是不是已经到头了；
      - [call function] 如果到头了，用对应的预测符填写规约项
        - predict_table:
          - key = current_status_id
          - value:
              遍历 LR_produc_item.predict_list,把里面的每个元素作为字典的key，
              把'r'+LR_produc_item.produc_id 作为字典的value
      - 如果后面还有字符，说明可以进行内部状态拓展
        - [call function] 内部状态拓展
          - 遍历每一个LR_produc_item
            - 通过dot_location 找到dot右边的符号，这个符号就是拓展节点产生式的左边，记为left_char
            - 通过inner_status_dict这个字典，找到left_char的所有产生式，
              - 将新的LR_produc_item加入Status.list中
                - item.produc_id = inner_status_dict[left_char][i]
                - item.dot_location = 0
                - item.predic_list = First(production_list[LR_produc_item.produc_id][1][dot_location+1])
                  - [call function] : First:
5. First(production) function 的求解：
  result
  if production[0] in terminal:
    return production[0]
  else:
    
    for char in production:
      for x in inner_status_dict[char]['status_list']
      result.append(First(production_list[x][1]))
      if not inner_status_dict[char]['has_spison']:
        break;