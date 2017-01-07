#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.8
# Modified    :   2017.1.8
# Version     :   1.0

# Parsing.py
import Queue
import json
from prettytable import PrettyTable
class ParsingProcessor(object):
    def __init__(self, fp, parsing_table, production_list):

        #   1. 构造输入流，在结尾加上$
        self.input_queue = list(fp.read() + '$')
        # 2. 需要有一个栈，这个栈有两个元素，一个是状态，一个是符号
        #  3. 初始化栈，状态为0号，符号为$
        self.token_stack= ['$']
        self.status_stack = [0]
        # 用于记录分析过程
        self.parsing_log = []
        # 传递预测分析表
        self.parsing_table = parsing_table
        # 传递产生式表
        self.production_list = production_list

    def add_log(self,info):
        """增加一条新的分析记录
        Args:
            info: 用于添加在动作项中的注明信息
        """
        self.parsing_log.append([len(self.parsing_log),str(self.status_stack),str(self.token_stack),str(self.input_queue),info])
           
    def parsing(self):
        """语法分析的主程序

        """
        token = self.input_queue[0]
        #   4. 获取读头的元素token，获取当前的状态号码为status
        while(1):
            status = self.status_stack[-1]
            # - 查看parsing_table[status][token]对应的符号，设为 result
            # print self.parsing_table
            # try:
            try:
                result = self.parsing_table[status][token]
            except Exception,e:
                # - 如果result 为空，分析失败
                print "error status: %s ,token: %s"%(status,token)
                print "parsing table for this status is : %s"%self.parsing_table[status]
                return False
            if result[0]=='s':
            # - 如果result 为 移进项，也就是s开头，则获得其移进的项目id，shift_status_id
                shift_status_id = int(result[1:])
            # - 将[shift_status_id,token]压入栈中，读头读取新的元素
                self.add_log("shift to:%s"%shift_status_id)
                item =[shift_status_id,token]
                self.status_stack.append(shift_status_id)
                self.token_stack.append(token)
                self.input_queue.pop(0)
                token = self.input_queue[0]
            elif result[0]=='r': 
                # - 如果result为规约项，也就是r开头
                if result[1:] == '0':
                # - 如果规约项为r0,那么翻译成功
                    self.add_log("accept")
                    return True
                else:
                    regression_id = int(result[1:])
                    pro_str = self.production_list.stringtify_by_id(regression_id)
                    self.add_log("regression production:%s"%pro_str)
                    proitem = self.production_list.get_right_by_index(regression_id)
                    # - 根据规约项产生式的长度，弹出对应的栈，的元素，
                    length = proitem.length
                    self.token_stack = self.token_stack[:-length]
                    self.status_stack = self.status_stack[:-length]
                    # - 设规约项左边的符号为token,
                    new_token = self.production_list.get_left_by_index(regression_id)
                    # - 根据现在的剩下的栈顶status和新的符号token，求parsing_table[status][token]对应的符号，设为result
                    status = self.status_stack[-1]
                    # try:
                    result = self.parsing_table[status][new_token]
                    # except Exception,e:
                    #     return False
                    # - 因为这里的token为非终结符，所以对应的result一定为移进符号，
                    # - 将 [result[1:],token]压入栈中
                    self.status_stack.append(int(result[1:]))
                    self.token_stack.append(new_token)
                    # - 产生式规约成功，输出

    def print_log(self):
        """以表格的形式打印分析过程
        """
        # print self.parsing_log
        print "printing the parsing step..."
        tabletab=['id','status stack','token stack','input','action']
        x = PrettyTable(tabletab)  
        x.align["STATUS"] = "l"# Left align city names
        for item in self.parsing_log:
            x.add_row(item)
        print x
        