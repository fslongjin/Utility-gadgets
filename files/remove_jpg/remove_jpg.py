import os
import sys
from send2trash import send2trash

print("本脚本的目的是，在同名dng文件存在的情况下，删除多余的jpg文件")
path = input("请输入文件夹路径：")

print("正在扫描...", end="")
files = os.listdir(path)

to_remove = []
# 先把后缀名全部统一成小写
for i in range(0, len(files)):
    files[i] = files[i].lower()

for x in files:
    end = x.split(".")[-1]
    front = x.split('.')
    ff = ''
    for xx in front[:-1]:
        ff += xx
    
    if end.lower() == 'dng' :
        if (ff+'.jpg') in files:
            to_remove.append(path + '\\' + ff + '.jpg')

print("ok")
print("共有%d个文件需要删除" % len(to_remove))
ch = input("确定删除？(y/n)")
mode = (str(sys.platform) == 'win32')
if ch.lower() == 'y':
    for x in to_remove:
        if mode:
            send2trash(x)
            print("移动到回收站:\t", x)
        else:
            print("删除:\t", x)
            os.remove(x)
print("删除完成")

