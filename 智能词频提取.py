#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
基于结巴分词
1.先进行搜索引擎分词，然后统计词频
2.再基于TF-IDF算法进行重点关键词抽取，排除停止词等
3.匹配重点关键词词频，排序后输出

用法
    python3 脚本文件 [参数] 目标文件 

参数
    -k,--topK
        类型：整数，提取前多少的词频
    -m,--mode
        值:s、c，s代表搜索引擎分词，c代表普通分词

示例        
    python3 智能词频提取.py -k 20 -m s 提取结果.txt
'''

import jieba.analyse
import jieba,argparse
from collections import Counter

def cut_for_search(content):
    return jieba.cut_for_search(content)

def cut(content):
    return jieba.cut(content)

def extract_tags(content,topK):
    return jieba.analyse.extract_tags(content,topK=topK)

def get_cipin(content,mode,top):
    if mode == "s":
        tags = cut_for_search(content)
    elif mode == "c":
        tags = cut(content)
    else:
        raise ValueError("参数错误:mode应该为s(搜索引擎模式分词)或c(精确模式分词)")
    core_ci = extract_tags(content,top)
    word_counts = Counter(tags)

    for word in core_ci:
        cipin = word_counts[word]
        print('%s\t%s' %(word,cipin))


parser = argparse.ArgumentParser()

parser.add_argument('file')
parser.add_argument('-k','--topK',type = int,default = 20)
parser.add_argument('-m','--mode',type = str,default="s")

args = parser.parse_args()

FILE = args.file
TOP = args.topK
MODE = args.mode

if __name__ == '__main__':
    content = open(FILE,'r').read()
    get_cipin(content,MODE,TOP)
