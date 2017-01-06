#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.6
# Modified    :   2017.1.6
# Version     :   1.0

# Function.py

from Structure import ProItem

# First
def First(self, production):
    predict_list = set()
    if production[0].type == 'T':
        predict_list.add(production[0].char)
    else:
        for char in production:
            for x in self.inner_status_dict[char.char]:
                first = First(self.production_list[x][1])
                if EPSILON not in first:
                    predict_list.update(first)
                    break
                else:
                    first.remove(EPSILON)
                    predict_list.update(first)
    return predict_list