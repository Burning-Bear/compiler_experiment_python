文件读取：

fp.read([size])                     #size为读取的长度，以byte为单位
fp.readline([size])                 #读一行，如果定义了size，有可能返回的只是一行的一部分
如何判断文件结尾：An empty string is returned when EOF is encountered.

所以 result = fp.read(1)
while(True):
    if result:
        print result

字典的遍历方法：


>>> for k in d.keys():
...   if d[k] == 0:
...     del(d[k])

for (d,x) in dict.items():
     print "key:"+d+",value:"+str(x)

关于 nano的编辑器使用

文件编辑中常用快捷键：ctrl+X 离开nano软件，若有修改过的文件会提示是否保存；

ctrl+O 保存文件；   ctrl+W 查询字符串；

ctrl +C 说明目前光标所在处的行数和列数等信息；

ctrl+ _ 可以直接输入行号，让光标快速移到该行；

