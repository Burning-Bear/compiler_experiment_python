#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.7.30
# Modified    :   2017.7.30
# Version     :   1.0

from Tkinter import *

class WidgetsDemo(object):

    def __init__(self):
        window = Tk()
        window.title("组建demo")
        #添加一个多选按钮和单选按钮到frame1
        frame1 = Frame(window)
        frame1.pack()  #看下面的解释（包管理器）
        self.v1 = IntVar()
        cbtBold = Checkbutton(frame1, text = "粗体", variable = self.v1, command = self.processCheckbutton)
        self.v2 = IntVar()
        rbRed = Radiobutton(frame1, text = "红色", bg = "red", variable = self.v2, value = 1, command = self.processRaidobutton)
        rbYellow = Radiobutton(frame1, text="黄色", bg="yellow", variable=self.v2, value=2, command=self.processRaidobutton)
        cbtBold.grid(row = 1, column = 1)  #将cbtBold排列在frame1的网格第一行第一列（网格管理器也会在下面有解释）
        rbRed.grid(row=1, column=2)
        rbYellow.grid(row=1, column=3)
        #添加一个label、entry、button和message到frame2
        frame2 = Frame(window)
        frame2.pack()
        label = Label(frame2, text = "请输入名字")
        self.name = StringVar()
        entryName = Entry(frame2, textvariable = self.name)
        btGetName = Button(frame2, text = "获取名字", command = self.processButton)
        message = Message(frame2, text = "组建demo")
        label.grid(row = 1, column = 1)
        entryName.grid(row = 1, column = 2)
        btGetName.grid(row = 1, column = 3)
        message.grid(row = 1, column = 4)
        #添加一个text
        text = Text(window)
        text.pack()
        text.insert(END, "Tip\n最好的学习TKinter方式是读")  #END表示插入到当前文本最后
        text.insert(END, "这是一些很好的学习例子使用他们")
        text.insert(END, "创建你自己的应用吧")
        window.mainloop()

    def processCheckbutton(self):
        print("复选框按钮是" + ("被选中" if self.v1.get() == 1 else "未选中"))    
    def processRaidobutton(self):        
        print("红色是" + ("被选中" if self.v2.get() == 1 else "未选中"))    
    def processButton(self):        
        print("你的名字是：" + self.name.get())

WidgetsDemo()