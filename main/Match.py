#!usr/bin/env python
#coding=utf-8
# match.py
from Global import DFA_hash_dic, node_reg_mapping, key_mapping_regex
import logging
import re

class MatchHandler(object):
    def __init__(self,fp):
        self._current_status='0'
        self._succ_list = []
        # fp come from open("file path",'r')
        self._fp = fp
        self._end_file = False

    def _mapping_key(self, single_char):
        key = None
        if DFA_hash_dic[self._current_status].has_key(single_char):
            key = single_char
        else:
            for (temp_key, value) in key_mapping_regex.items():
                # find if this single char satisfied with some kind of regex expression.
                if re.match(value,single_char):
                    key = temp_key
                    break
            # find a key, then judge if this is a key in dictory
            if key and not DFA_hash_dic[self._current_status].has_key(key):
                key = None
        return key
            
    def _match_one_char(self, single_char):
        logging.info("match one char :%s"%single_char)
        key = self._mapping_key(single_char)
        logging.info("key is :%s"%key)
        if not key:
            return None
        else:
            next_status = DFA_hash_dic[self._current_status][key]
            return next_status
                    # get a end node, record in succ_list.

    def _append_succ_list(self, status, str):
        """Store success information, include status and regex string, into succ_list.

        Args:
            status: 'exx'
            str:'float'

        Returns:
            None
        """
        prefix = status[0]
        if prefix == 'e':
            # next status is a end node, record in succ_list.
            info = {'status':status,'text':str}
            self._succ_list.append(info)

    def _update_status(self, next_status):
        self._current_status = next_status

    def _get_next_char(self):
        """Get next char of fp.
        when EOF is encountered, return None.

        Args:
            None

        Returns:
            next char or None
        """
        # fp come from open("file path",'r')
        result = self._fp.read(1)
        if result:
            return result
        else:
            self._end_file = True
            return None
    def reset_file_pointer(self):
        self._fp.seek(self._fp.tell() - 1)

    def _list_mapping(self):
        if self._succ_list == []:
            return None
        else:
            # find the min level regex as the match string.
            min_level = 99
            min_index = -1
            for index, item in enumerate(self._succ_list):
                status = item['status']
                level = node_reg_mapping[status]
                if level < min_level:
                    min_level = level
                    min_index = index
            min_status = self._succ_list[min_index]['status']
            result = {
                'status':min_status,
                'text':self._succ_list[min_index]['text'],
                'info':node_reg_mapping[min_status]['info']
            }
            return result

    def _reset(self):
        self._current_status='0'
        self._succ_list = []

    def _match_one_reg(self):
        """
          - 获取下一个读入字符
          - 为每次匹配构造成功匹配栈
          - 循环调用字典，直到某个字符没有对应的后继状态 
            - 循环过程中记录匹配成功的字符串和对应的配对表达式编号
          - 通确定当前应该选用的正则表达式，
          - 输出对应信息
        """
        next_char = self._get_next_char()
        current_text = next_char
        while(1):
            if self._end_file:
                # get the end of file
                break
            next_status = self._match_one_char(next_char)
            logging.info("next status is %s"%next_status)
            if next_status == None:
                # failed or finfish, depend on succ_list is empty or not.
                # reset read pointer
                self.reset_file_pointer()
                break
            else:
                self._append_succ_list(next_status, current_text)
                self._update_status(next_status)
            next_char = self._get_next_char()
            if next_char == None:
                break
            current_text = current_text+next_char
        # match finish, now mapping.
        result = self._list_mapping()
        self._reset()
        if not result:
            # return the fail match string
            return False,current_text
        else:
            return True,result

    def match_driver(self):
        result_queue = []
        while(True):
            if self._end_file:
                return result_queue
            success, result = self._match_one_reg()
            logging.info("success:%s, result: %s"%(success,result))
            if not success:
                result_queue.append("match error with: text\"%s\""%result)
                return result_queue
            else:
                result_queue.append(result)

