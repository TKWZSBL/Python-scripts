# coding: utf-8

#根据bedtools coverage的结果文件，统计reads覆盖cds大于X%的表达的gene,自动输出xxx_cds_coverage.txt文件
#运行脚本: python script.py SRR029190.depth.txt 
#edit by tankaiwen 2021.06.09

import sys

#读取输入文件
depth_file=sys.argv[1]

name = depth_file.split('.')
geneID_coverage_dict = {}
geneID_cds_dict = {}
geneID_gene_length_dict = {}

with open(depth_file,'r') as depth:
    for i in depth:
        
        line_depth = i.strip().split('\t')
        geneID=line_depth[3]
        cds_length=float(line_depth[5])
        gene_length=float(line_depth[6])
        
        if int(line_depth[4]) >= 5:

            #每个基因有表达的cds长度
            if geneID in geneID_cds_dict:
                geneID_cds_dict[geneID] = int(geneID_cds_dict[geneID]) + cds_length
            else:
                geneID_cds_dict.setdefault(geneID,cds_length)
            #每个基因总cds长度统计
            if geneID in geneID_gene_length_dict:
                geneID_gene_length_dict[geneID] = int(geneID_gene_length_dict[geneID]) + gene_length
            else:
                geneID_gene_length_dict.setdefault(geneID,gene_length)
        else:
            if geneID in geneID_cds_dict:
                continue
            else:
                geneID_cds_dict.setdefault(geneID,0)
            if geneID in geneID_gene_length_dict:
                #geneID_gene_length_dict.get(line_depth[3]).append(line_depth[6])
                geneID_gene_length_dict[geneID] = int(geneID_gene_length_dict[geneID]) + gene_length
            else:
                geneID_gene_length_dict.setdefault(geneID,gene_length)

#开始计算
geneID_coverage_dict = {k : v/geneID_gene_length_dict[k] for k, v in geneID_cds_dict.items() if k in geneID_gene_length_dict}
#将结果写进文件
#给定输出文件名字
output = open(name[0]+'_cds_coverage.txt','w')
for i,j in geneID_coverage_dict.items() :
    print(i,j,file=output,sep='\t')
output.close()

