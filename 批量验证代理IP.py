#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
将IP作为代理访问www.baidu.com，如果返回状态码为200则代理IP有效
'''

import requests,sys
import threading
from CONFIG import makeHeaders

def testProxies(ip):
    proxies = {'http':ip}
    try:
        r = requests.head('http://www.baidu.com',proxies=proxies,timeout=10,headers=makeHeaders())
    except:
        print('%s\t不可用' %proxies['http'])
    else:
        if r.status_code == 200:
            print('%s\t可用' %proxies['http'])
            lock.acquire()
            with open('代理IP验证结果.txt','a+') as f:
                f.write('%s\n' %ip)
            lock.release()
        else:
            print('%s\t不可用' %proxies['http'])


if __name__=="__main__":

    lock = threading.Lock()
    
    ips = open(sys.argv[1],'r').readlines()
    
    while ips:
    
        t = ips[:10]
        ips = ips[10:]
        ps = []
        
        for ip in t:
            p = threading.Thread(target=testProxies,args=(ip.strip(),))
            ps.append(p)
            p.start()
            
        for p in ps:
            p.join()
