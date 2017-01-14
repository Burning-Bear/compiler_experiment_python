#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.6
# Modified    :   2017.1.7
# Version     :   1.0

from ParsingTable import ParsingTableProcessor
from Production import ProductionSet
from Parsing import ParsingProcessor
import logging
import Queue

logging.basicConfig(level=logging.INFO,                   
                     filename='output.log',
                     filemode='w')

def parsing_table_driver(processor):
    """LR(1)预测分析表构造处理器的驱动，调用它可以构造成分析表

    Args:
        processor: 输入是分析表处理器：
    
    Returns:
        processor，构造完成之后的构造器ParsingTableProcessor
    """
    definited_status = processor.init_status()
    # 状态间拓展使用的是广度优先遍历，这里构造了一个队列，
    # 用来存放新产生的确定化状态的标号，以便接下来进行的状态内部拓展
    to_extent_queue = Queue.Queue(maxsize=-1)
    to_extent_queue.put([0, definited_status])
    # 当没有待拓展队列之后，循环结束
    while not to_extent_queue.empty():
        item = to_extent_queue.get()
        definited_status_id = item[0]
        definited_status = item[1]
        # 进行状态间拓展
        status_dict = processor.goto(definited_status)
        for key,value in status_dict.items():
            # 状态内扩展
            definited_status = processor.closure(value)    
            # 确定一个状态，加入字典
            old_status_id = processor.same_status(definited_status)
            # print "----print definited status [id]:%s,    [edge]: %s------,is old?:%s"%(definited_status_id,key,old_status_id)
            # definited_status.print_status()
            if old_status_id == -1:
                new_status_id = processor.get_next_status_id()
                processor.add_to_definited_status(definited_status)     
                # 确定状态为新状态后，进行状态内的可规约符号进行规约
                processor.regression(definited_status, new_status_id)
                # 将确定化的状态加入待拓展队列
                to_extent_queue.put([new_status_id , definited_status])
                # 进行状态间拓展
                processor.add_to_parsing_table('s'+str(new_status_id), definited_status_id, key)
            else:
                processor.add_to_parsing_table('s'+str(old_status_id), definited_status_id, key)
    return processor


production_fp = open("production.txt",'r')
# 构造产生式
production = ProductionSet(production_fp)
# 生成分析表构造器
processor = ParsingTableProcessor(production)
# 构造分析表
processor = parsing_table_driver(processor)
# 打印
processor.print_parsing_table()
processor.print_status_list()
# 语法分析
token_fp = open("input.txt",'r')
# 构造语法分析器
parsing = ParsingProcessor(token_fp,processor.predict_parsing_table,processor.production_list)
parsing.parsing()
# 打印分析结构
parsing.print_log()