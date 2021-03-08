#根据原本的基因位置，筛选出blast结果中最优且位置正确的结果,自动输出 blast_out.fil.txt 文件
#运行脚本: python script.py gene.fil.bed(基因对应染色体的list) blast_out.txt(blast结果文件)
#edit by tankaiwen 2021.01.29


import sys
gene_dict_file = sys.argv[1]
blast_out = sys.argv[2]


old_gene_dict = {}
with open(gene_dict_file,'r') as gene_bed:
    for i in gene_bed:
        line = i.strip().split("\t")
        old_gene_dict.setdefault(line[0],line[1])


file1 = open('blast_out.fil.txt','w')
with open(blast_out,'r') as blast:
    geneID = ''
    a = 0
    for i2 in blast:
        line2 = i2.strip().split("\t")
        if line2[0].startswith("#"):#如果开头是#则跳过该行
            continue
        else:      
            if str(line2[0])!=str(geneID):#如果不是#行，先判断是否已经读过该gene的blast结果,不等于表示是第一次读到该gene
                a += 1
                if a == 1:
                    best_blast = i2.strip()#预存第一个为最优比对
                #print(line2)
                if line2[1] == old_gene_dict[line2[0]]:#提取old gene字典中的信息,判断如果符合位置，则输出结果到文件
                    #加一步判断，如果比对上的长度小于2k，则还是使用最优比对结果，不再管染色体比对错误的问题
                    if int(line2[3]) < 2000:
                        print(best_blast,file=file1)
                        geneID = line2[0]
                    else:    
                        print(i2.strip(),file=file1)
                        geneID = line2[0]
                elif str(old_gene_dict[line2[0]]).startswith("scaffold"):
                #如果不符合，即比对出现了问题，则再进行判断,如果scaffold开头则直接拿最好的比对结果
                #注：针对不同的基因组，这个scaffold可能不同，有的是contig或其他，自己修改
                    print(i2.strip(),file=file1)
                    geneID = line2[0]
                elif line2[1] != old_gene_dict[line2[0]]:
                    print(best_blast,file=file1)
                    geneID = line2[0]
            else:#如果不是#行，且读过了该gene,进行过判断，则跳过
                geneID = line2[0]
                a = 0


file1.close()   
