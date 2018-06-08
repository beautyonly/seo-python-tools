#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
通用的文本匹配脚本

传入需匹配的文本及配置项（分隔符，匹配因子所在列）
传入映射关系及配置项（分隔符，匹配模式）

映射关系数量越大匹配速度越慢;匹配模式不为0时速度慢
'''

#import argparse
import sys
#from multiprocessing import Process,Lock

def mode_ctrl(a,b,mode):
    '''
    文本匹配模式控制
    0：相等
    1：完全匹配包含，如'客厅' in '客厅装修'
    2：完全包含，如'客厅装修' in '装修客厅图片'
    '''
    if mode == 0:
        return a == b
    elif mode == 1:
        return a in b
    elif mode == 2:
        return set(a) - set(b) == set()
    else:
        return False

def match(map_dict,text,keyword_column,separator,mode):
    keyword = text.split(key_file_separate)[keyword_column-1]
    if mode == 0:
        try:
            re = map_dict[keyword]
        except:
            re = 'null'
            re_with_data = '%s%s%s\n'%(re,separator,text)
            f.write(re_with_data)
            print(re_with_data.strip())
        else:
            re_with_data = '%s%s%s\n'%(re,separator,text)
            f.write(re_with_data)
            print(re_with_data.strip())
    else:
        matched_flag = 0
        for key in list(map_dict.keys()):
            if mode_ctrl(key,keyword,mode):
                re = map_dict[key]
                re_with_data = '%s%s%s\n'%(re,separator,text)
                print(re_with_data.strip())
                f.write(re_with_data)
                matched_flag = 1
                break
            else:
                matched_flag = 2
        if matched_flag == 2:
            re = 'null'
            re_with_data = '%s%s%s\n'%(re,separator,text)
            f.write(re_with_data)
            print(re_with_data.strip())


if __name__ == '__main__': 

    #配置项
    map_separate = ','   #映射关系文件的分隔符
    key_file_separate  = ',' #匹配文件的分隔符
    key_column = 2  #匹配因子在文件中的列数
    match_mode = 1  #匹配模式

    #lock = Lock()
    
    text_file = sys.argv[1]
    map_file = sys.argv[2]
    f = open('文本匹配结果.txt','w')
    
    #构建映射字典
    map_dict = {}
    for i in open(map_file,'r').readlines():
        i = i.strip().split(map_separate)
        map_dict[i[0]] = i[1]

    text = [ x.strip() for x in open(text_file,'r').readlines() ]
    
    for i in text:
        match(map_dict,i,key_column,key_file_separate,match_mode)
    
    #while text:
    #    team = text[:3]
    #    text = text[3:]
    #
    #    ps = []
    #
    #    for text in team:
    #        p = Process(target=match,
    #                    args=(map_dict,text,key_column,key_file_separate,match_mode))
    #        ps.append(p)
    #        p.start()
    #
    #    for p in ps:
    #        p.join()

    f.close()
    print('匹配结果输出完毕')