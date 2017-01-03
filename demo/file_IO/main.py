# main.py

fp = open("hello.txt",'r')
while(1):
    result = fp.read(1)
    if result:
        print result
        print fp.tell()

print 'end'