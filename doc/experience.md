文件读取：

fp.read([size])                     #size为读取的长度，以byte为单位
fp.readline([size])                 #读一行，如果定义了size，有可能返回的只是一行的一部分
如何判断文件结尾：An empty string is returned when EOF is encountered.

所以 result = fp.read(1)
while(True):
    if result:
        print result
