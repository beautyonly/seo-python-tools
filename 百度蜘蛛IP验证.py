#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
通过IP判断是否真实的百度蜘蛛
如果传入参数为txt文件，则进入批量判断模式
'''


import socket,argparse,re
from bs4 import BeautifulSoup

def if_bd_ip(ip):
    try:
        result = socket.gethostbyaddr(ip)
        if 'crawl.baidu.com' in result[0]:
            return 'Real'
        else:
            r = requests.get('http://ip.t086.com/?ip=%s' %ip)
            s = BeautifulSoup(r.content.decode('gbk'),'lxml')
            if '百度' in s.find('div','bar2 f16').getText():
                return 'Real'
            else:
                return 'Fake'
    except:
        return 'Fake'

def ifip(ip):
    return bool(re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$',ip))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip',help='input ip or ips-file')

    args = parser.parse_args()

    IP = args.ip

    if '.txt' in IP:
        result = open('result.txt','w')
        checked = []
        for i in open(IP,'r').readlines():
            if ifip(i):
                ipd = '.'.join(i.split('.')[:3])
                if ipd not in checked:
                    j = '%s.*\t%s' %(ipd,check(i))
                    print(j)
                    result.write('%s\n' %j)
                else:
                    continue
            else:
                j = '%s\t非法IP' %i
                print(j)
                result.write('%s\n' %j)
            checked.append(ipd)
        result.close()

    else:
        if ifip(IP):
            try:
                print(check(IP))
            except:
                print('查询出错')
        else:
            print('非法IP')
