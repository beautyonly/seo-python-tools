#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
使用方法：
命令行运行 python3 匹配词根.py 词根文件 关键词文件

注意事项：
词根文件每行一个，每次从第一个关键词开始匹配
关键词文件每行一个
'''

import sys

keywords = open(sys.argv[2],'r').readlines()
cigens = open(sys.argv[1],'r').readlines()
rst = open('result.txt','w')

for k in keywords:
    k = k.strip()
    for c in cigens:
        c = c.strip()
        c_in_k_list = []
        if c in k:
            c_in_k_list.append(c)
    rst.write('%s %s\n' %(k,','.join(c_in_k_list)))

rst.close()