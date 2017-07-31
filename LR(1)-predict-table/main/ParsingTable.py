#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.6
# Modified    :   2017.1.14
# Version     :   1.0  


# ParsingTable.py

"""
    - Status 对象，记录了一个确定化状态的全部信息
      - 有一个list，list的每个元素是LR_proudc_item对象

    - LR_produc_item对象是在状态图中的每个产生式的状态，他有三个元素：
      - produc_id: 原始产生式的id
      - dot_location: 点当前的位置，记录的是其右边的字符的下表
      - predic_list: 这是一个列表，记录的是其预测符号
"""
import json
import pdb
import logging
import Queue
from Global import EPSILON
from prettytable import PrettyTable
from Production import ProItem

import Tkinter    

class LR_produc_item(object):
    """
        用于描述一个LR(1)分析过程中每个产生式的状态，它包含了dot和预测符信息

        - LR_produc_item对象是在状态图中的每个产生式的状态，他有三个元素：
          - produc_id: 原始产生式的id
          - dot_location: 点当前的位置，记录的是其右边的字符的下表
          - predic_list: 这是一个列表，记录的是其预测符号
    """
    def __init__(self,id, dot_location, predict_list):
        # 产生式的id
        self.produc_id = id
        # 点当前的位置，记录的是其右边的字符的下表
        self.dot_location =dot_location
        # 这是一个集合，记录的是其预测符号
        self.predict_list = set(predict_list)

    def the_same_lr(self,item):
        """判断两个LR产生式项是否相同，不比较预测符情况
        
        Args:
            item 用于比较的产生式
        """
        if self.produc_id == item.produc_id and self.dot_location == item.dot_location:
            return True
        else:
            return False

    def the_same_lr_full(self,item):
        """判断两个LR产生式项是否相同，需要比较预测符情况
        
        Args:
            item 用于比较的产生式
        """
        if self.produc_id == item.produc_id and self.dot_location == item.dot_location and self.predict_list-item.predict_list == set([]):
            return True
        else:
            return False

    def update_predict(self,predict_list):
        """对该产生式的预测符号进行追加，因为是集合的结构，可以自动进行去重

        """
        self.predict_list.update(predict_list)

    def print_lr_item(self):
        logging.info("id is %s, dot_location is %s, predic_list is %s"%(self.produc_id,self.dot_location, self.predict_list))

class Status(object):
    """
    - Status对象，记录了一个状态的全部信息
          - 有一个list，list的每个元素是LR_proudc_item对象 
          - length 字段用来记录现在Status一共有的产生式的个数
    """
    def __init__(self):
        self.list = []
        self.length=0
    
    def has_same_status(self,status):
        """判断两个状态是否完全相同

        Args:
            status: 用于比较的状态
        """
        for index, item in enumerate(status.get_status_list()):
            # 此时相同产生式，但是预测符不同的，已经合并了，
            #　所以你不用考虑预测符不同的相同产生式的情况
            same_index = self.has_same_lr_item(item,full=True)
            if same_index == -1:
                return False
        return True
    def has_same_lr_item(self, produc_item,full=False):
        """比较待匹配的产生式是否能在Status中找到，

        Args:
            produc_item:  一个LR_produc_item 对象
            full: true 意味着需要匹配预测符号，false不需要保证预测符一样

        Returns:
            如果相同，返回所在的下表
            否则，返回-1
        """
        for index, item in enumerate(self.list):
            if full:            
                if item.the_same_lr_full(produc_item):   
                    return index
            else:
                if item.the_same_lr(produc_item):   
                    return index
        return -1       

    def add(self, produc_item):
        """加入新的产生式进该状态节点，这个函数已经考虑了重复产生式的预测符合并的情况

        Args：
            produc_item:用于合并进来的产生式


        """
        # 如果该项和已有状态中的产生式一样，dot也要一样，直接合并
        index = self.has_same_lr_item(produc_item)
        if index == -1:
            # 这是一个新的产生式，直接append
            self.list.append(produc_item)
            self.length = self.length + 1
        else:
            self.list[index].update_predict(produc_item.predict_list)
            return    


    def get_status_list(self):
        return self.list

    def print_status(self):
        for index, x in enumerate(self.list):
            logging.info("--status number :%s"%index)
            x.print_lr_item()


class ParsingTableProcessor(object):
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
          # - 用于记录已经确定化的状态列表，
          # - 这是个list，list的下表的含义是确定化的状态
          # - list的每一个item是一个Status对象qued
        self.definited_status_list = []
        self.production_list = production
        # 用来记录下一个状态的标号的id
        self.status_next_id = 0

    def get_next_status_id(self):
        """获得下一个状态的标号的id

        """
        result = self.status_next_id
        self.status_next_id = self.status_next_id + 1
        return result

    def First(self, produc_item):
        """求first算法

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

    def regression(self, Status, status_id):
        """将状态中需要规约的产生式填入predict parsing table
        
        Args：
            Status：待检查的状态
            status_id: 这个产生式的id[todo: id应该作为status本身的一个对象，而不是作为参数传递进来]
        """
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
                    # print "starting regression"
                    for predict_char in item.predict_list:
                        self.add_to_parsing_table('r' + str(pro_id), status_id, predict_char)

    def closure(self, Status):
        """内部状态拓展，构造闭包的算法

        Args:
            Status：用来子状态拓展的状态
        """
        stat_list = Status.get_status_list()
        old_length = 0
        new_length = Status.length
        # 循环直到状态内找不到新的产生式为止,也就是两次循环的Status的产生式的个数相等
        # pdb.set_trace()
        while(old_length != new_length):
            old_length = new_length
            for item in stat_list:
                # item 是一个lr_produc产生式
                pro_id = item.produc_id
                # pro_item 是一个产生式ProItem对象
                pro_item = self.production_list.get_right_by_index(pro_id)
                if item.dot_location != pro_item.length:
                    # 产生式的dot没有到末尾，可以进行拓展
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
                                # 求first
                                predict_list = self.First(new_pro_item)
                                if EPSILON in predict_list:
                                    # 当predict_list有epsilon的时候，再把原来的预测符加上来
                                    predict_list.extend(item.predict_list)
                            lr_produc_item = LR_produc_item(production_id, 0, predict_list)
                            Status.add(lr_produc_item)
            new_length = Status.length
            # Status.print_status()
        return Status
    
    def get_parsing(self, origin_id, token):
        """获得分析表的具体信息
        [这个函数的结构设计的不是特别好！]
        """
        if self.predict_parsing_table[origin_id].has_key(token):
            return self.predict_parsing_table[origin_id][token]
        else:
            return 'empty'
    def init_status(self):
        """初始化第一个产生式
        """
        init_lr_item = LR_produc_item(0,0,'$')
        init_status = Status()
        init_status.add(init_lr_item)
        # init_lr_item.print_lr_item()
        # init_status.print_status()
        status_id = self.get_next_status_id()
        definited_status = self.closure(init_status)
        self.add_to_definited_status(definited_status)
        return definited_status


    def goto(self, status):
        """用来进行状态间拓展

        Args:
            status 是状态集合
            X 是用于goto的边
        """
        status_dict = {}
        for lr_item in status.get_status_list():
            # item 是一个lr_produc产生式
            pro_id = lr_item.produc_id
            # pro_item 是一个产生式ProItem对象
            pro_item = self.production_list.get_right_by_index(pro_id)
            if lr_item.dot_location < pro_item.length:
                # 这个产生式还没到达末尾，可以进行拓展
                # 获得移进的token符号
                edge = pro_item.get_token_by_index(lr_item.dot_location).char
                # 构造新的lr项
                new_lr_item = LR_produc_item(pro_id, lr_item.dot_location+1, lr_item.predict_list)
                if status_dict.has_key(edge):
                    # 这个状态已经存在，将新的产生式加入进来
                    status_dict[edge].add(new_lr_item)
                else:
                    # 这个状态还未出现
                    status_dict[edge] = Status()
                    status_dict[edge].add(new_lr_item)
        return status_dict

    def add_to_definited_status(self, status):
        """将状态加入确定化的状态字典
        """
        self.definited_status_list.append(status)

    def add_to_parsing_table(self, symbol, origin_id, token):
        """将数据填入预测分析表

        Args：
            symbol：需要填入的符号信息，有r+id和s+id两种情况
            origin_id:状态id
            token:token字符信息

        """
        if self.predict_parsing_table.has_key(origin_id):
            self.predict_parsing_table[origin_id][token] = symbol
        else:
            self.predict_parsing_table[origin_id] = {
                token:symbol
            }

    def same_status(self, Status):
        """判断两个状态是否是相同的状态

        Returns：
            -1 如果不是相同的状态
            index 如果是相同的状态，返回状态的id标号
        """
        for index,value in enumerate(self.definited_status_list):
            if Status.has_same_status(value):
                return index
        return -1

    def print_parsing_table(self,text=None):
        
        
        tabletab = ['STATUS']
        for key in self.production_list.get_action_set():
            tabletab.append("A:"+key)
        for key in self.production_list.get_goto_set():
            tabletab.append("G:"+key)

        x = PrettyTable(tabletab)  
        x.align["STATUS"] = "l"# Left align city names

        x.padding_width = 1# One space between column edges and contents (default)
        for index, status in self.predict_parsing_table.items():
            row = [index]
            for key in self.production_list.get_action_set():
                row.append(self.get_parsing(index,key))
            for key in self.production_list.get_goto_set():
                row.append(self.get_parsing(index,key))
            x.add_row(row)
        if text == None:
            logging.info("printing the predict parsing table...\n %s"%x)
        else:
            print "in printing!"
            text.insert(Tkinter.END,x)

    def print_status_list(self):
        logging.info("printing the definited status list...\n")
        for index, status in enumerate(self.definited_status_list):
            logging.info("--------------------------------")
            logging.info('|'+("status I%s:"%index).ljust(30)+'|')
            for lr_item in status.get_status_list():
                produc_id = lr_item.produc_id
                dot_location = lr_item.dot_location
                predict_list = lr_item.predict_list
                left_char = self.production_list.get_left_by_index(produc_id) 
                right_token_list = self.production_list.get_right_by_index(produc_id)
                right_char = ''
                for index, token in enumerate(right_token_list.get_list()):
                    if index == dot_location:
                        right_char = right_char+'.'
                    right_char = right_char + token.char
                logging.info('|'+(left_char+"->"+right_char+","+str(predict_list)).center(30)+"|")
            logging.info("--------------------------------")
            logging.info("  ")