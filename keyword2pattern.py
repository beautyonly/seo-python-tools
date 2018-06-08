#/usr/bin/env python3

import jieba
import sys
import json

def keyword2pattern(keywords_file,pattern_kv_file='pattern_kv.json'):
    keywords = [ x.strip() for x in open(keywords_file,'r').readlines() ]
    pattern_dict = json.loads(open(pattern_kv_file,'r').read())
    wd2pt = {} 

    for k in keywords:
        k_cut = list(jieba.cut(k))
        k_pt = k_cut[:]
        for i in k_cut:
            if i in pattern_dict.keys():
                k_pt[k_pt.index(i)] = '{%s}' %pattern_dict[i]
        wd2pt[k] = ' + '.join(k_pt)

    return wd2pt

if __name__ == "__main__":
    pts = keyword2pattern(sys.argv[1])
    with open('关键词pattern.txt','w') as f:
        for k,v in pts.items():
            f.write('%s\t%s\n' %(k,v))

