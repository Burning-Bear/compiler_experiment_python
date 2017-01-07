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
logging.basicConfig(level=logging.INFO)

def parsing_table_driver(processor):
    """LR(1)预测分析表构造处理器的驱动，调用它可以构造成分析表
    Args:
        processor: 输入是分析表处理器：
    """
    definited_status = processor.init_status()
    to_extent_queue = Queue.Queue(maxsize=-1)
    to_extent_queue.put([0, definited_status])
    # print "----print definited status------,"
    # definited_status.print_status()
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
                # print "shift status id is %s"%new_status_id
                processor.regression(definited_status, new_status_id)
                # 将确定化的状态加入待拓展队列
                to_extent_queue.put([new_status_id , definited_status])
                processor.add_to_parsing_table('s'+str(new_status_id), definited_status_id, key)
            else:
                processor.add_to_parsing_table('s'+str(old_status_id), definited_status_id, key)
    return processor


fp = open("production.txt",'r')
production = ProductionSet(fp)
# production.print_production_instance()
# production.print_inner_dict()
processor = ParsingTableProcessor(production)
# second_status.print_status()
processor = parsing_table_driver(processor)

processor.print_parsing_table()
processor.print_status_list()
fp = open("input.txt",'r')
parsing = ParsingProcessor(fp,processor.predict_parsing_table,processor.production_list)
parsing.parsing()

parsing.print_log()