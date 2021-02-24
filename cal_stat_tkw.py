#运行：python *py
#自动获取文件夹下所有.stat文件，自动输出统计结果--stat_cal.xls文件。
import os
import re
import pandas as pd

ls = os.popen('ls *.stat').readlines()
names=[]
read=[]
ratio=[]
data = pd.DataFrame()

for i in ls:
    name = i
    file = open(i[:-1],'r')
    cmd = 'sed ' +  '-n ' + '5p ' + i[:-1]
    readsline = os.popen(cmd).readline()
    ratioline = file.read()
    pattern = re.compile('mapped(.*?)N/A')
    ratios = pattern.findall(ratioline)[0]
    reads = readsline.split()
    names.append(i[:-1])
    read.append(reads[0])
    ratio.append(ratios[2:-2])

data['name'] = names
data['read'] = read
data['ratio'] = ratio

data.to_excel('stat_cal.xls',index = False)
