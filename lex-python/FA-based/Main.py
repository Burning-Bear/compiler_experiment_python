#!usr/bin/env python
#coding=utf-8
# main.py
import json
import logging

from prettytable import PrettyTable

from Match import MatchHandler

def format_print(result_queue):
    """以表格的形式打印结果
    """
    # print self.parsing_log
    tabletab=['status','origin_char','infomation']
    x = PrettyTable(tabletab)  
    x.align["STATUS"] = "l"# Left align 
    for item in result_queue:
    	list_item = [item["status"],item['text'],item['info']]
        x.add_row(list_item)
    print x

logging.basicConfig(level=logging.INFO,                   
 					filename='output.log',
                    filemode='w')
fp = open("text.txt",'r')
match = MatchHandler(fp)
result_queue =  match.match_driver()
format_print(result_queue)