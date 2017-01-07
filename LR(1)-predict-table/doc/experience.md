
## 比较两个数组是否相同
你实现的重点就是要比较两个列表的是否相同。
建议你可以先排序在比较
a.sort()
b.sort()
a==b就会返回True。

如：
>>> a = [(1,1),(2,2),(3,3),(4,4)]
>>> b = [(4,4),(1,1),(2,2),(3,3)]
>>> a==b
False
>>> a.sort()
>>> b.sort()
>>> a
[(1, 1), (2, 2), (3, 3), (4, 4)]
>>> b
[(1, 1), (2, 2), (3, 3), (4, 4)]
>>> a==b
True

## QUEUE队列
- 创建一个“队列”对象
    - import Queue
    - myqueue = Queue.Queue(maxsize = 10)
    - Queue.Queue类即是一个队列的同步实现。队列长度可为无限或者有限。可通过Queue的构造函数的可选参数maxsize来设定队列长度。如果maxsize小于1就表示队列长度无限。

- 将一个值放入队列中
    - myqueue.put(10)
    - 调用队列对象的put()方法在队尾插入一个项目。put()有两个参数，第一个item为必需的，为插入项目的值；第二个block为可选参数，默认为1。如果队列当前为空且block为1，put()方法就使调用线程暂停,直到空出一个数据单元。如果block为0，put方法将引发Full异常。

- 将一个值从队列中取出
    - myqueue.get()
    - 调用队列对象的get()方法从队头删除并返回一个项目。可选参数为block，默认为True。如果队列为空且block为True，get()就使调用线程暂停，直至有项目可用。如果队列为空且block为False，队列将引发Empty异常。

- python queue模块有三种队列:
    1. python queue模块的FIFO队列先进先出。
        - class Queue.Queue(maxsize) FIFO 
    2. LIFO类似于堆。即先进后出。
        - class Queue.LifoQueue(maxsize) LIFO 
    3. 还有一种是优先级队列级别越低越先出来。 
        - class Queue.PriorityQueue(maxsize) 优先级队列
- 介绍一下此包中的常用方法:
Queue.qsize() 返回队列的大小 
Queue.empty() 如果队列为空，返回True,反之False 
Queue.full() 如果队列满了，返回True,反之False
Queue.full 与 maxsize 大小对应 
Queue.get([block[, timeout]])获取队列，timeout等待时间 
Queue.get_nowait() 相当Queue.get(False)
非阻塞 Queue.put(item) 写入队列，timeout等待时间 
Queue.put_nowait(item) 相当Queue.put(item, False)
Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
Queue.join() 实际上意味着等到队列为空，再执行别的操作

## 调试
- 设置断点
    import pdb
    pdb.set_trace()
- (Pdb) h
    说明下这几个关键 命令>断点设置
   (Pdb)b  10 #断点设置在本py的第10行
   或(Pdb)b  ots.py:20 #断点设置到 ots.py第20行
   删除断点（Pdb）b #查看断点编号
            (Pdb)cl 2 #删除第2个断点
   
- 运行
    (Pdb)n #单步运行
    (Pdb)s #细点运行 也就是会下到，方法
    (Pdb)c #跳到下个断点
- 查看
    (Pdb)p param #查看当前 变量值
    (Pdb)l #查看运行到某处代码
    (Pdb)a #查看全部栈内变量>如果是在 命令行里的调试为：

## set的操作
- 构造
    - a = set('spam') 
    - a = set(['h','a','m']) 
- 操作
    t.add('x')            # 添加一项    
    s.update([10,37,42])  # 在s中添加多项

    使用remove()可以删除一项：  
    t.remove('H')  
      
    len(s)  
    set 的长度  
      
    x in s  
    测试 x 是否是 s 的成员  
      
    x not in s  
    测试 x 是否不是 s 的成员  
      
    s.issubset(t)  
    s <= t  
    测试是否 s 中的每一个元素都在 t 中  
      
    s.issuperset(t)  
    s >= t  
    测试是否 t 中的每一个元素都在 s 中      
- 集合操作
    a = t | s          # t 和 s的并集  
      
    b = t & s          # t 和 s的交集  
      
    c = t – s          # 求差集（项在t中，但不在s中）  
      
    d = t ^ s          # 对称差集（项在t或s中，但不会同时出现在二者中）  

## 格式化输出表格

>>> from prettytable import PrettyTable
>>> x = PrettyTable(["name", "age", "sex", "money"])
>>> x.align["name"] = "l"  # 以name字段左对齐
>>> x.padding_width = 1   # 填充宽度
>>> x.add_row(["wang",20, "man", 1000])
>>> x.add_row(["alex",21, "man", 2000])
>>> x.add_row(["peiqi",22, "man", 3000])
>>> print(x)