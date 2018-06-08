'''
将所有『关键词+搜索量』转为字典{'关键词':'搜索量'}
然后以关键词为key来查找对应的值，从而得到搜索量
'''

import sys

rjDict = {}

all =open(sys.argv[1],'r',encoding='utf-8').readlines()

for i in all:
    i = i.strip().split(',')
    ci,rj = i[0],i[1]
    rjDict[ci] = rj

keywords = open(sys.argv[2],'r',encoding='utf-8').readlines()
file = open('result.txt','a+',encoding='utf-8')

for k in keywords:
    k = k.strip()
    try:
        k_rj = rjDict[k]
    except:
        file.write('%s\n' %k)
    else:
        file.write('%s,%s\n' %(k,rjDict[k]))

file.close()