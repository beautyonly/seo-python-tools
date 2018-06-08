#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
seo数据采集脚本

用法
    python3 seo数据采集.py [参数] [输出文件]

参数
    ztm，查询状态码
    sl，查询收录
    pm，查询排名

示例
    python3 seo数据采集.py ztm 查询结果.txt
'''


import requests,json,time
from bs4 import BeautifulSoup
from CONFIG import makeHeaders,getProxy

def get_indexed(url):
    url = 'http://%s' %url if 'http' not in url else url
    search_url = 'http://www.baidu.com/s?wd=%s&tn=json' %url
    r = requests.get(search_url,headers=makeHeaders(),proxies=getProxy(),timeout=10)
    js_text = json.loads(r.text)
    if js_text['feed']['entry'][0] == {}:
        return '未收录'
    else:
        landurl = js_text['feed']['entry'][0]['url']
        if url == landurl:
            return '已收录'
        else:
            return '未收录'

def get_ztm(url,proxy):
    return requests.head(url,proxies=proxy).status_code

def to8to_rank_filter(tag):
    if tag.name != 'div' or not tag.has_attr('class'):
        return False
    elif 'resultc-container' not in ''.join(tag.attrs['class']):
        return False
    elif not tag.find('a','c-showurl',string=re.compile('to8to.com')):
        return False
    else:
        return True

def get_location(landurl):
    r2 = requests.get(landurl,allow_redirects=False)
    return r2.headers['Location']

def get_rank_data(tag,keyword):
    rank = tag.attrs['id']
    rankurl = tag.find('a','c-showurl').attrs['href']
    landurl = get_location(rankurl)
    return [keyword,rank,landurl]

def get_ranks(keyword,url):
    r = requests.get('http://www.baidu.com/s?wd=%s' 
        %keyword,headers=makeHeaders(),proxies=getProxy())
    s = BeautifulSoup(r.text,'lxml')
    to8to_ranks = s.findAll(to8to_rank_filter)
    rank_datas = []
    if len(to8to_ranks) != 0:
        for div in to8to_ranks:
            rank_datas.append(get_rank_data(div,keyword))
    else:
        rank_datas.append([keyword,0,''])
    return rank_datas
        


def run(keyword=None,url=None,mode=None,proxy=None):
    if mode == 'ztm':
        return '%s\t%s' %(url,get_ztm(url,proxy))
    if mode == 'sl':
        return '%s\t%s' %(url,get_indexed(url,proxy))
    elif mode == 'pm':
        rank_datas = get_ranks(keyword,url,proxy)
        for i in rank_datas:
            print('%s\t%s\t%s' %(i[0],i[1],i[2]))


if __name__ == '__main__':
    in_mode = sys.argv[1]
   
    for line in open(sys.argv[2],'r'):
        in_keyword,in_url = line.strip().split(',')
 
        #查状态码or收录
        if in_mode in ['ztm','sl']:
            run(url=in_url,mode='ztm') if in_mode == 'ztm' else run(url=in_url,mode='sl')
        #查排名
        elif in_mode == 'pm':
            run(keyword=in_keyword,url=in_url,mode='pm')
        
        #查状态码、收录、排名
        elif in_mode == 'all':
            run(keyword=in_keyword,url=in_url,mode='all')


        
        
