#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.7
# Modified    :   2017.1.7
# Version     :   1.0

# Global.py



"""
- predict_parsing_table:
    - LR(1) 预测分析表
    - 第一维度是一个数组，数组的内容是一个字典，数组的下标index代表的是确定化的状态号
    - 字典：
        - key：key代表的是读头header的字符串，也就是边的字符
        - value: 
          - 如果是移进项，'s'+id,代表的就是移进的确定化状态编号
          - 如果是规约项，'r'+id代表的就是规约的产生式编号

"""
EPSILON = 'e'
predict_parsing_table = {}
"""

状态间拓展使用的是广度优先遍历，这里构造了一个队列，
用来存放新产生的确定化状态的标号，以便接下来进行的状态内部拓展

"""

to_extension_queue = []
"""
  - 用于记录已经确定化的状态列表，
  - 这是个list，list的下表的含义是确定化的状态
  - list的每一个item是一个Status对象qued
"""
definited_status_list= []
