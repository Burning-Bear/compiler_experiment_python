#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.7.30
# Modified    :   2017.8.4
# Version     :   1.0

# testUI.py

import Tkinter           # 导入 Tkinter 库
import Tkconstants, tkFileDialog
from main import parsing_table_driver
from ParsingTable import ParsingTableProcessor
from Production import ProductionSet
from Parsing import ParsingProcessor
import logging
import Queue

logging.basicConfig(level=logging.INFO)

class MainFrame(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)
        self.root = root
        # Tkinter.Label(root,text="LR(1)语法分析辅助实验系统",font =("Times", "24", "bold")).pack()
        self.control_frame = Tkinter.Frame(root)
        self.control_frame.pack()
        self.show_frame = Tkinter.Frame(root)
        self.show_frame.pack()
        self.processor = None

        self.control_product_frame = Tkinter.Frame(self.control_frame)
        self.control_product_frame.grid(row=0,column=0,padx=15,pady=2)
        self.control_test_frame = Tkinter.Frame(self.control_frame)
        self.control_test_frame.grid(row=0,column=1,padx=15,pady=2)

        Tkinter.Label(self.control_product_frame,
            text="语法分析器构造栏",
            font=("微软雅黑","14")).grid(row=0,columnspan=3)

        self.product_file_label = Tkinter.Label(
            self.control_product_frame, 
            text="尚未选择文件",
            width = 20)
        self.product_file_select_button = Tkinter.Button(
            self.control_product_frame, 
            text="上传产生式文件",
            command=self.update_product_text)
        self.product_file_label.grid(row=1,column=0,sticky="w")
        self.product_file_select_button.grid(row=1,column=1, sticky=Tkinter.E)
        self.product_edit_text = Tkinter.Text(self.control_product_frame,width=40)
        self.product_edit_text.grid(row=2,columnspan=2)
        self.product_edit_text.insert(Tkinter.END,'无内容')


        Tkinter.Label(self.control_test_frame,
            text="tokens检测栏",
            font=("微软雅黑","14")).grid(row=0,columnspan=3)

        self.test_file_label = Tkinter.Label(
            self.control_test_frame, 
            text="尚未选择文件",
            width = 20)
        self.test_file_select_button = Tkinter.Button(
            self.control_test_frame, 
            text="上传测试文件",
            command=self.update_test_text)     
        self.test_file_label.grid(row=1,column=0,sticky="w")
        self.test_file_select_button.grid(row=1,column=1, sticky=Tkinter.E)
        self.test_edit_text = Tkinter.Text(self.control_test_frame,width=40)
        self.test_edit_text.grid(row=2,columnspan=2)
        self.test_edit_text.insert(Tkinter.END,'无内容')


        table_button = Tkinter.Button(
            self.control_product_frame, 
            text="构造预测分析表",
            command=self.parsing_table)
        construct_button = Tkinter.Button(
            self.control_product_frame, 
            text="生成确定化状态列表",
            command=self.lr_item)
        table_button.grid(row=3,column=0,padx=14,sticky=Tkinter.W)
        construct_button.grid(row=3,column=1,padx=14)
        parsing_button = Tkinter.Button(
            self.control_test_frame, 
            text="对tokens进行语法分析",
            command=self.token_analyze)
        parsing_button.grid(row=3,columnspan=2)
        # .grid(row=1)
        # .pack(side=Tkinter.RIGHT)
        
        

        # Tkinter.Label(
        #     self.control_test_frame, 
        #     text="not select file yet").pack(side=Tkinter.RIGHT)

        # self.product_filename= "not select yet"
        

        
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = '上传文件'

    def update_product_text(self):
        self.product_filename = tkFileDialog.askopenfilename(**self.file_opt)
        if self.product_filename:
            self.product_file_label.config(text='...'+self.product_filename[-20:])
            self.product_edit_text.delete(0.0, Tkinter.END)
            with open(self.product_filename) as f:
                for line in f.readlines():
                    self.product_edit_text.insert(Tkinter.END,line)

    def update_test_text(self):
        self.test_filename = tkFileDialog.askopenfilename(**self.file_opt)
        if self.test_filename:
            self.test_file_label.config(text='...'+self.test_filename[-20:])
            self.test_edit_text.delete(0.0, Tkinter.END)
            with open(self.test_filename) as f:
                for line in f.readlines():
                    self.test_edit_text.insert(Tkinter.END,line)

    def parsing_table(self):
        top = Tkinter.Toplevel(self.root)
        text = Tkinter.Text(top)
        text.pack(fill=Tkinter.BOTH, expand=1)
        production_fp = open(self.product_filename,'r')
        # 构造产生式
        try:
            production = ProductionSet(production_fp)
            # 生成分析表构造器
            self.processor = ParsingTableProcessor(production)
            # 构造分析表
            self.processor = parsing_table_driver(self.processor)
            # 打印
            self.processor.print_parsing_table(text=text)
        except Exception as e:
            text.insert(Tkinter.END,"您输入的语法有误，分析表构造失败")


    def lr_item(self):
        top = Tkinter.Toplevel(self.root)
        text = Tkinter.Text(top)
        text.pack(fill=Tkinter.BOTH, expand=1)
        if self.processor == None:
            text.insert(Tkinter.END,"请先构造预测分析表")
            return
        self.processor.print_status_list(text=text)


    def token_analyze(self):
        top = Tkinter.Toplevel(self.root)
        text = Tkinter.Text(top)
        text.pack(fill=Tkinter.BOTH, expand=1)
        token_fp = open(self.test_filename,'r')
        # 构造语法分析器
        if self.processor == None:
            text.insert(Tkinter.END,"请先构造预测分析表")
            return
        parsing = ParsingProcessor(token_fp,self.processor.predict_parsing_table,self.processor.production_list)
        parsing.parsing()
        # 打印分析结构
        parsing.print_log(text)

if __name__ == '__main__':
    root = Tkinter.Tk()
    root.geometry('800x450')
    root.title("LR(1)语法分析辅助实验系统")
    MainFrame(root)
    root.mainloop()