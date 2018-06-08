#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
通过URL批量查询状态码、title数据
'''


import requests,sys,os
from CONFIG import getProxy
from multiprocessing import Process
from bs4 import BeautifulSoup

def manager(url,filename,mode):
    
    if mode == 'ztm':
        try:
            r = requests.head(url,proxies=getProxy(),timeout=5)
        except:
            result = '失败'
        else:
            result = get_ztm(r)
    elif mode == 'title':
        try:
            r = requests.get(url,proxies=getProxy(),timeout=5)
        except:
            resutl = '失败'
        else:
            result = get_title(r)
    else:
        print('参数错误')
    
    with open(filename,'a+') as f:
        f.write('%s\t%s\n' %(url,result))
        print('%s\t%s\n' %(url,result))


    #try:
    #    r = requests.get(url,proxies=getProxy(),timeout=5)
    #except:
    #    print('%s\t失败' %url)
    #else:
    #    if mode == 'ztm':
    #        ztm = get_ztm(r)
    #        with open(filename,'a+') as f:
    #            f.write('%s\t%s\n' %(url,ztm))
    #        print('%s\t%s' %(url,ztm))
    #    elif mode == 'title':
    #        title = get_title(r)
    #        with open(filename,'a+') as f:
    #            f.write('%s\t%s\n' %(url,title))
    #        print('%s\t%s' %(url,title))

def get_title(response):
    try:
        title = BeautifulSoup(response.text,'lxml').find('title').getText()
    except:
        title = ''
    else:
        title = title.split('_')[0]
    finally:
        return title

def get_ztm(response):
    return response.status_code


if __name__ == "__main__":

    urls = open(sys.argv[1],'r').readlines()
    outfile = sys.argv[2]
    mode = sys.argv[3]
    
    while urls:
        team = urls[:os.cpu_count()]
        urls = urls[os.cpu_count():]
        ps = []
        for i in team:
            i = i.strip()
            p = Process(target=manager,args=(i,outfile,mode))
            ps.append(p)
            p.start()
            
        for i in ps:
            p.join()