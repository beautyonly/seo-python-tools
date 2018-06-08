#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
采集百度、360、搜狗下拉框关键词脚本
'''

import json,requests,re,sys,time

def get_sugs(word):
    sugs = []
    for SE in ['baidu','360','sogou']:
        sugs += baidu_sugs(word)
        sugs += sogou_sugs(word)
        sugs += so_sugs(word)
    return set(sugs)

def baidu_sugs(word):
    try:
        r = requests.get('http://suggestion.baidu.com/su?wd=%s&sugmode=3&json=1' %word,timeout=5)
        r_js = json.loads(re.sub("\\\\\\\'",' ',re.sub(r'window.baidu.sug\((.*)\);',r'\1',r.text)))
    except Exception as e:
        print(e)
        with open('采集失败关键词.txt','a+') as f:
            f.write(word+'\tbaidu\n')
        return []
    else:
        return r_js['s']

def sogou_sugs(word):
    try:
        r = requests.get('https://www.sogou.com/suggnew/ajajjson?key=%s&type=web' %word,timeout=5)
        r_js = json.loads(re.sub(r'window.sogou.sug\((.*),-1\);',r'\1',r.text))
    except Exception as e:
        print(e)
        with open('采集失败关键词.txt','a+') as f:
            f.write(word+'\tsogou\n')
        return []
    else:
        return r_js[1]

def so_sugs(word):
    try:
        r = requests.get('https://sug.so.360.cn/suggest?callback=suggest_so&encodein=utf-8&encodeout=utf-8&format=json&fields=word&word=%s' %word,timeout=5)
        r_js = json.loads(re.sub(r'suggest_so\((.*)\);',r'\1',r.text))
    except Exception as e:
        print(e)
        with open('采集失败关键词.txt','a+') as f:
            f.write(word+'\t360\n')
        return []
    else:
        return [ x['word'] for x in r_js['result'] ]
       
        
if __name__ == '__main__':

    for seed_word in open(sys.argv[1],'r').readlines():
        seed_word = seed_word.strip()
    
        #对种子词进行拓展，结尾加字母获得更多推荐词
        seed_word_expand = [seed_word] + [ seed_word + x for x in 'abcdefghijklmnopqrstuvwxyz' ]
        for seed in seed_word_expand:
            for line in get_sugs(seed):
                with open('下拉框关键词.txt','a+') as f:
                    f.write('%s\t%s\n' %(seed_word,line))
            #time.sleep(0.5)