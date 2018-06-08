#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
通过搜索结果地址获取着陆页真实URL
'''

import requests,sys
from bs4 import BeautifulSoup
from CONFIG import getProxy

def get_location_by_url(bdurl):
    try:
        landurl = requests.head(bdurl,proxies=getProxy(),allow_redirects=False).headers['Location']
    except KeyError:
        r = requests.get(bdurl)
        s = BeautifulSoup(r.text,'lxml')
        landurl = s.find('script').getText().split('(')[-1].split(')')[0].split('"')[1]
        return landurl
    else:
        return landurl

if __name__ == '__main__':
    for bdurl in open(sys.argv[1],'r'):
        try:
            url = get_location_by_url(bdurl.strip())
        except:
            with open('失败.txt','a+') as ff:
                ff.write('%s' %bdurl)
        else:
            print(url)
            with open(sys.argv[2],'a+') as f:
                f.write('%s\t%s\n' %(bdurl.strip(),url))