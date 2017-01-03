#!usr/bin/env python
#coding=utf-8
# main.py
import json
from Match import MatchHandler
import logging
logging.basicConfig(level=logging.INFO)
fp = open("text.txt",'r')
match = MatchHandler(fp)
result_queue =  match.match_driver()
for item in result_queue:
    print item