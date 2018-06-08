#!/usr/bin/env python3

import datetime
import os
import re
import time
import socket
import requests
from ftplib import FTP
from bs4 import BeautifulSoup
from pandas import DataFrame

def get_yesterday():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def download_log(date=get_yesterday()):
    log_file = 'baidusearch-%s.tar.gz' %date
    if os.path.isfile(log_file):
        print('''>>> 日志文件已存在，解压''')
        os.system('tar -xzvf %s to8to_baidu.log' %log_file)
    else:    
        ftp = FTP()
        ftp.connect('192.168.3.4',port=11211)
        ftp.login('ftpuser_baidu','''ftpuser_baidu@@)!%''')
        
        print('''>>> 下载日志文件"%s"''' %log_file)
        ftp.retrbinary('RETR ' + log_file,open(log_file,'wb').write)

        print('''>>> 解压日志文件''')
        os.system('tar -xzvf %s to8to_baidu.log' %log_file)    

def verify_ip(ip):
    try:
        result = socket.gethostbyaddr(ip)
    except:
        r = requests.get('http://ip.t086.com/?ip=%s' %ip)
        s = BeautifulSoup(r.content.decode('gbk'),'lxml')
        if '百度' in s.find('div','bar2 f16').getText():
            return True
        else:
            return False
    else:
        if 'crawl.baidu.com' in result[0]:
            return True
        else:
            return False

def list_to_file(list,filename):
    for i in list:
        with open(filename,'a+') as f:
            f.write('%s\n' %i)

def date_tran(log_date):
    time_map = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    date = re.sub(r'\[([0-9]+)/([a-zA-z]+)/([0-9]+):([0-9:]+)',r'\3/\2/\1 \4',log_date)
    l = date.split('/')
    l[1] = str(time_map[l[1]])
    return '/'.join(l)

def log_parser(log_str):
    domain,_,_,_,date,_,method,url,_,statu,size,time,referer,*ua = log_str.split(' ')
    ips = ''.join(ua).split('"')[3]
    if ips.count(',') > 1:
        ip = ips.split(',')[0]
    else:
        ip = ips
    ua = ''.join(ua).split('"')[1]
    date = date_tran(date)
    return {'domain':domain,'ip':ip,'date':date,'method':method,'url':url,'statu':statu,'size':int(size),'time':time,'referer':referer,'ua':ua}

def make_data(log_file):
    log_text = open(log_file,'r').readlines()
    data = []
    for i in log_text:
        data.append(log_parser(i))
    return data
    
    
if __name__ == '__main__':

    #下载日志
    download_log()
    
    #构建 DataFrame
    data = make_data('to8to_baidu.log')
    log_frame = DataFrame(data)

    #检查IP
    ips = list(log_frame['ip'])
    fake_ips = []
    for ip in ips:
        if not verify_ip(ip):
            fake_ips.append(ip)
    list_to_file(fake_ips,'fake_ips.txt')
    
    #检查状态码
    log_frame.groupby('statu')['url'].count()
    
    
    