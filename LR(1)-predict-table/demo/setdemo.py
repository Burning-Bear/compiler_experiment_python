#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.7
# Modified    :   2017.1.7
# Version     :   1.0


# setdemo.py
class Char(object):
    def __init__(self,char,char_type):
        self.char = char
        self.type = char_type

a = set()
char = Char('E','T')
a.add(char)
char = Char('E','N')
a.add(char)
the_same =Char('E','N')
a.add(the_same)
print a