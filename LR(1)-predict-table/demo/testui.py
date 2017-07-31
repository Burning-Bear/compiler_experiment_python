#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.7.30
# Modified    :   2017.7.30
# Version     :   1.0

# testUI.py

import Tkinter           # 导入 Tkinter 库
import Tkconstants, tkFileDialog
class MainFrame(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root)
        self.root = root
        Tkinter.Label(root,text="编译原理教学辅助实验室系统",font =("Times", "24", "bold italic")).pack()
        self.control_frame = Tkinter.Frame(root)
        self.control_frame.pack()
        self.show_frame = Tkinter.Frame(root)
        self.show_frame.pack()

        self.control_product_frame = Tkinter.Frame(self.control_frame)
        self.control_product_frame.grid(row=0,column=0,padx=10,pady=2)
        self.control_test_frame = Tkinter.Frame(self.control_frame)
        self.control_test_frame.grid(row=0,column=1,padx=10,pady=2)


        self.product_file_label = Tkinter.Label(
            self.control_product_frame, 
            text="not select file yet",
            width = 60)
        self.product_file_select_button = Tkinter.Button(
            self.control_product_frame, 
            text="上传产生式文件",
            command=self.update_product_text)
        self.product_file_label.grid(row=0,column=0,sticky=Tkinter.W)
        self.product_file_select_button.grid(row=0,column=1, sticky=Tkinter.E)
        self.product_edit_text = Tkinter.Text(self.control_product_frame)
        self.product_edit_text.grid(row=1,columnspan=2)
        self.product_edit_text.insert(Tkinter.END,'not content yet')


        self.test_file_label = Tkinter.Label(
            self.control_test_frame, 
            text="not select file yet",
            width = 60)
        self.test_file_select_button = Tkinter.Button(
            self.control_test_frame, 
            text="上传测试文件",
            command=self.update_test_text)
        self.test_file_label.grid(row=0,column=0,sticky=Tkinter.W)
        self.test_file_select_button.grid(row=0,column=1, sticky=Tkinter.E)
        self.test_edit_text = Tkinter.Text(self.control_test_frame)
        self.test_edit_text.grid(row=1,columnspan=2)
        self.test_edit_text.insert(Tkinter.END,'not content yet')


        table_button = Tkinter.Button(
            self.control_product_frame, 
            text="构造预测分析表",
            command=self.parsing_table)
        construct_button = Tkinter.Button(
            self.control_product_frame, 
            text="构造lr(1)产生式",
            command=self.update_product_text)
        table_button.grid(row=2,column=0,padx=14,sticky=Tkinter.W)
        construct_button.grid(row=2,column=1,padx=14)
        parsing_button = Tkinter.Button(
            self.control_test_frame, 
            text="对token进行语法分析",
            command=self.control_test_frame)
        parsing_button.grid(row=2,columnspan=2)
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
        product_filename = tkFileDialog.askopenfilename(**self.file_opt)
        if product_filename:
            self.product_file_label.config(text='...'+product_filename[-50:])
            self.product_edit_text.delete(0.0, Tkinter.END)
            with open(product_filename) as f:
                for line in f.readlines():
                    self.product_edit_text.insert(Tkinter.END,line)

    def update_test_text(self):
        test_filename = tkFileDialog.askopenfilename(**self.file_opt)
        if test_filename:
            self.test_file_label.config(text='...'+test_filename[-50:])
            self.test_edit_text.delete(0.0, Tkinter.END)
            with open(test_filename) as f:
                for line in f.readlines():
                    self.test_edit_text.insert(Tkinter.END,line)

    def parsing_table(self):
        top = Tkinter.Toplevel(self.root)
        text = Tkinter.Text(top)
        text.pack()
                           # 创建两个列表
        # li     = ['C','python','php','html','SQL','java']
        # movie  = ['CSS','jQuery','Bootstrap']
        # listb  = Listbox(root)          #  创建两个列表组件
        # listb2 = Listbox(root)
        # for item in li:                 # 第一个小部件插入数据
        #     listb.insert(0,item)

        # for item in movie:              # 第二个小部件插入数据
        #     listb2.insert(0,item)

        # listb.pack()                    # 将小部件放置到主窗口中
        # listb2.pack()

        # import tkFileDialog

        # filename = tkFileDialog.askopenfilename(filetypes=[("bmp格式".decode('gbk'),"bmp")])

        # Button(self, text='askopenfilename', command=self.askopenfilename).pack(**button_opt)

if __name__ == '__main__':
    root = Tkinter.Tk()
    root.geometry('1024x768')
    root.title("编译原理教学辅助实验室系统")
    MainFrame(root)
    root.mainloop()