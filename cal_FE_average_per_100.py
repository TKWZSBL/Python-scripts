###给定FE.sorted.bdg与bin.bed相交后的文件，计算平均每个碱基的FE值（即每一个窗口的平均值，一个窗口的加起来除以100）
###脚本运行：python cal_FE_average_per_100.py BBen_FE.bed
#文件格式：BBen_FE.bed
#bin文件染色体号   起始位置    终止位置    FE文件染色体号    起始位置    终止位置   位置丰度（FE值）    bin大小
# 1       0       100     1       0       15574   0.00000 100
# 1       100     200     1       0       15574   0.00000 100
# 1       200     300     1       0       15574   0.00000 100
#edit by Kaiwen Tan 2020.09.11
#注意，该脚本仅针对特定课题，其他课题可能出现漏掉某些行的可能（比如基因）
import sys

input_FE = sys.argv[1]
name = input_FE.split('.')
dict1 = {}
dict2 = {}
dict3 = {}
with open(sys.argv[1],'r') as bedfile:
    for line in bedfile:
        info = line.rstrip().split('\t')
        name = info[0]+'\t'+info[1]+'\t'+info[2]#即染色体号 起始位置 终止位置 三个信息
        number = (int(info[2])-int(info[1]))#number是该区域的长度，终止位置-起始位置
        FE = float(info[6])*int(info[7])#该区域FE值 = 每个碱基的FE * 碱基数
        
        if name in dict1:
            dict1[name] = dict1[name] + FE #如果字典中已经有了name，则将值进行累加
        else:
            dict1[name] = FE
            
        if name in dict2:
            pass
        else:
            dict2[name] = number #如果字典中已经有了name，则将值进行累加

#将两个字典进行值的相除，得到每个区间的平均FE值
dict3 = {k : v/dict2[k] for k, v in dict1.items() if k in dict2}

#将结果写进文件
average = open(name[0]+'.txt','w')
for i,j in  dict3.items() :
    print(i,j,file=average)
average.close()
