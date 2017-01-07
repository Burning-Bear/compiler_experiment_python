#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.7
# Modified    :   2017.1.7
# Version     :   1.0


# Production.py
class Token(object):
    """用于描述文法符号，也就是一个token
    """
    def __init__(self,char,char_type):
        self.char = char
        self.type = char_type

    def print_char(self):
        logging.info("-----char is %s, type is %s"%(self.char,self.type))

class ProItem(object):
    """ 
    用于描述单个产生式

    定义每一个产生式符号序列为一个对象,这个对象包括两个成员：
        token_list: 是一个符号序列的数组，每一个item包括两个元素：1. 字符；2. 字符的类型
        length ：产生式符号序列的类型

    """
    def __init__(self):
        self.token_list = []
        self.length = 0

    def add_string(self, string='', char_type=''):
        self.length = len(string)
        for (i,j) in zip(string, char_type):
            self.token_list.append(Token(i,j))   

    def add(self, extend_list):
        """为产生式序列增加新的元素
        Args:
            extend_list
        """
        self.token_list.extend(extend_list)
        self.length = self.length + len(extend_list)

    def get_token_by_index(self,index):
        return self.token_list[index]

    def print_item(self):
        for index,x in enumerate(self.token_list):
            logging.info("----ProItem number is %s"%index)
            x.print_char()     

    def get_char_by_index(self,index):
        return self.token_list[index].char

    def get_list(self):
        return self.token_list

class ProductionSet(object):
    """原来语法产生式的集合
    """
    def __init__(self,fp):
        # - 文法产生式数组 production_list
        #     - example of item in list:
        #         ["产生式左边"的ProItem,"产生式右边"的ProItem]
        #     - index： production 的index 代表的就是产生式的编号，我们将他成为id
        self.production_list = []
        # - 内部状态转换字典：inner_status_dict:
        #     - key: status 非终结符，是产生式的左边
        #     - value: value is a list
        #         - example of tiem in list:
        #             [origin_produc, origin_produc]
        #             代表的是这个终结符可以产生的产生式的标号集合
        self.inner_status_dict = {}
        self.action_set = set(["$"])
        self.goto_set = set()
        pro_line = fp.readline()
        type_line =fp.readline()
        while pro_line != '':
            # print 'pro :%s type is :%s'%(pro_line, type_line)
            left = ProItem()
            right =ProItem()
            left.add_string(pro_line[0],type_line[0])
            right.add_string(pro_line[3:-1],type_line[3:-1])
            self.production_list.append([left, right])
            self.add_token_list(right)
            index = len(self.production_list) - 1
            if self.inner_status_dict.has_key(left.get_char_by_index(0)):
                # 将产生式的序号加入innser_status_dict中
                self.inner_status_dict[left.get_char_by_index(0)].append(index)
            else:
                self.inner_status_dict[left.get_char_by_index(0)] = [index]
            pro_line = fp.readline()
            type_line = fp.readline()

    def add_token_list(self, proItem):
        """将一个token加入token_list， token_list 存储了产生式的所有token的集合
        
        Args:
            proItem:产生式右部
        """
        for token in proItem.get_list():
            if token.type == 'N':
                self.goto_set.add(token.char)
            else:
                self.action_set.add(token.char)

    def get_right_by_index(self,index):
        return self.production_list[index][1]

    def get_left_by_index(self,index):
        return self.production_list[index][0].get_token_by_index(0).char

    def get_by_char(self, char):
        return self.inner_status_dict[char]
        return [self.production_list[x] for x in production_id_list]

    def print_production_instance(self):
        for index,x in enumerate(self.production_list):
            logging.info("--number of production is %s"%index)
            logging.info("---print left")
            x[0].print_item()
            logging.info("---print right")
            x[1].print_item()
            logging.info("-------")

    def print_inner_dict(self):
        logging.info(json.dumps(self.inner_status_dict,indent=2))

    def get_goto_set(self):
        return self.goto_set

    def get_action_set(self):
        return self.action_set

    def stringtify_by_id(self,produc_id):
        """将第produc_id 条产生式格式化输出

        Args:
            produc_id:产生式id
        """
        left_char = self.get_left_by_index(produc_id) 
        right_token_list = self.get_right_by_index(produc_id)
        right_char = ''
        for index, token in enumerate(right_token_list.get_list()):
            right_char = right_char + token.char
        return left_char+"->"+right_char