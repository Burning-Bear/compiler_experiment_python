#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.7
# Modified    :   2017.1.7 
# Version     :   1.0  


# Structure.py

"""
    - Status对象，记录了一个确定化状态的全部信息
      - 有一个list，list的每个元素是LR_proudc_item对象

    - LR_produc_item对象是在状态图中的每个产生式的状态，他有三个元素：
      - produc_id: 原始产生式的id
      - dot_location: 点当前的位置，记录的是其右边的字符的下表
      - predic_list: 这是一个列表，记录的是其预测符号
"""
import json
import pdb
import logging
from Global import EPSILON
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
        pro_line = fp.readline()
        type_line =fp.readline()
        while pro_line != '':
            # print 'pro :%s type is :%s'%(pro_line, type_line)
            left = ProItem()
            right =ProItem()
            left.add_string(pro_line[0],type_line[0])
            right.add_string(pro_line[3:-1],type_line[3:-1])
            self.production_list.append([left, right])
            index = len(self.production_list) - 1
            if self.inner_status_dict.has_key(left.get_char_by_index(0)):
                # 将产生式的序号加入innser_status_dict中
                self.inner_status_dict[left.get_char_by_index(0)].append(index)
            else:
                self.inner_status_dict[left.get_char_by_index(0)] = [index]
            pro_line = fp.readline()
            type_line = fp.readline()

    def get_right_by_index(self,index):
        return self.production_list[index][1]

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

class LR_produc_item(object):
    """
        - LR_produc_item对象是在状态图中的每个产生式的状态，他有三个元素：
          - produc_id: 原始产生式的id
          - dot_location: 点当前的位置，记录的是其右边的字符的下表
          - predic_list: 这是一个列表，记录的是其预测符号
    """
    def __init__(self,id, dot_location, predict_list):
        self.produc_id = id
        self.dot_location =dot_location
        self.predict_list = set(predict_list)

    def the_same_lr(self,item):
        if self.produc_id == item.produc_id and self.dot_location == item.dot_location:
            return True
        else:
            return False

    def update_predict(self,predict_list):
        self.predict_list.update(predict_list)

    def print_lr_item(self):
        logging.info("id is %s, dot_location is %s, predic_list is %s"%(self.produc_id,self.dot_location, self.predict_list))

class Status(object):
    """
    - Status对象，记录了一个确定化状态的全部信息
          - 有一个list，list的每个元素是LR_proudc_item对象 
    """
    def __init__(self):
        self.list = []
        self.length=0

    def add(self, produc_item):
        # 如果该项和已有状态中的产生式一样，dot也要一样，直接合并
        for index, item in enumerate(self.list):
            if item.the_same_lr(produc_item):
                self.list[index].update_predict(produc_item.predict_list)
                return
        # 这是一个新的产生式，直接append
        self.list.append(produc_item)
        self.length = self.length + 1

    def get_status_list(self):
        return self.list

    def print_status(self):
        for index, x in enumerate(self.list):
            logging.info("--status number :%s"%index)
            x.print_lr_item()

class FaProcessor(object):
    def __init__(self, production):
        # - predict_parsing_table:
        #     - LR(1) 预测分析表
        #     - 第一维度是一个数组，数组的内容是一个字典，数组的下标index代表的是确定化的状态号
        #     - 字典：
        #         - key：key代表的是读头header的字符串，也就是边的字符
        #         - value: 
        #           - 如果是移进项，'s'+id,代表的就是移进的确定化状态编号
        #           - 如果是规约项，'r'+id代表的就是规约的产生式编号        
        self.predict_parsing_table = {}

        # 状态间拓展使用的是广度优先遍历，这里构造了一个队列，
        # 用来存放新产生的确定化状态的标号，以便接下来进行的状态内部拓展
        self.to_extension_queue = []
          # - 用于记录已经确定化的状态列表，
          # - 这是个list，list的下表的含义是确定化的状态
          # - list的每一个item是一个Status对象qued
        self.definited_status_list = []
        self.production_list = production

    def First(self, produc_item):
        """
        Args:
            produc_item: ProItem,输入的是一个产生式的token_list
        
        Returns:
            predict_list: 预测符序列
        """
        predict_list = set()
        first_token = produc_item.get_token_by_index(0)
        if first_token.type == 'T':
            predict_list.add(first_token.char)
        else:
            for token in produc_item.token_list:
                # 遍历产生式的每一个token
                first = set()
                for produc_id in self.production_list.get_by_char(token.char):
                    # 查看当前的token能够产生的所有产生式，produc_id 为产生式的下标,对产生式求first
                    first.update(self.First(self.production_list.get_right_by_index(produc_id)))
                # 遍历完成当前token的所有产生式
                # 查看token 的first能否产生SPSILON，如果可以产生，需要把EPSILON去掉，接着求下一个token的first
                # 如果不能产生SPSILON，说明遍历已经结束，将得到的SPSILON加入predict_list
                if EPSILON not in first:
                    predict_list.update(first)
                    break
                else:
                    first.remove(EPSILON)
                    predict_list.update(first)
        return predict_list

    def closure(self, Status):
        stat_list = Status.get_status_list()
        old_length = 0
        new_length = Status.length
        # 循环直到找不到新的产生式为止
        # pdb.set_trace()
        while(old_length != new_length):
            old_length = new_length
            for item in stat_list:
                # item 是一个lr_produc产生式
                pro_id = item.produc_id
                # pro_item 是一个产生式ProItem对象
                pro_item = self.production_list.get_right_by_index(pro_id)
                if item.dot_location == pro_item.length:
                    # LR1 产生式的dot已经到末尾了，需要进行规约操作
                    for predict_char in item.predict_list:
                        self.predict_parsing_table[pro_id] = 'r' + predict_char
                else:
                    next_token = pro_item.token_list[item.dot_location]
                    if next_token.type == 'N':
                        # 如果下一个token是非终结符，那么可以进行内部的状态位拓展
                        pro_id_list = self.production_list.get_by_char(next_token.char)
                        # 获取某个终结符的所有产生式的id
                        for production_id in pro_id_list: 
                            # 获得用于求first的表达式βa
                            predict_list = set()
                            # 计算新的产生式的预测符号
                            if pro_item.length == item.dot_location + 1:
                                # β == EPSILON， 直接将alpha作为预测符
                                predict_list = item.predict_list
                            else:
                                new_pro_item = ProItem()
                                new_pro_item.add(pro_item.token_list[item.dot_location+1:])
                                # 将预测福序列转化为[char, char_type]的表达形式
                                # char_list = [Token(x,'T') for x in item.predict_list]
                                # new_pro_item.add(char_list)
                                new_pro_item.print_item()
                                predict_list = self.First(new_pro_item)
                                if EPSILON in predict_list:
                                    # 当predict_list有epsilon的时候，再把原来的预测符加上来
                                    predict_list.extend(item.predict_list)
                            lr_produc_item = LR_produc_item(production_id, 0, predict_list)
                            Status.add(lr_produc_item)
            new_length = Status.length
            # Status.print_status()
        return Status

    def init(self):
        pass
    def goto(Status, X):
        """
            Status 是状态集合
            X 是用于goto的边
        """
        pass