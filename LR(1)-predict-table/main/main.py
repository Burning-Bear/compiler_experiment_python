#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.7
# Modified    :   2017.1.7
# Version     :   1.0

from Structure import ProductionSet, FaProcessor, LR_produc_item, Status
import logging
logging.basicConfig(level=logging.INFO)
fp = open("production2.txt",'r')
production = ProductionSet(fp)
production.print_production_instance()
production.print_inner_dict()
processor = FaProcessor(production)
init_lr_item = LR_produc_item(0,0,'$')
init_status = Status()
init_status.add(init_lr_item)
# init_lr_item.print_lr_item()
# init_status.print_status()
second_status = processor.closure(init_status)
second_status.print_status()