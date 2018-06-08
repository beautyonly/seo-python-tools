#encoding:utf-8 
'''
Created on 2016年7月4日

@author: beauty
'''
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import random

startTime = time.clock()

#读取keywords
f = open('keywords.txt','r')
kw_list = f.readlines()
f.close()

domain = 'baidu.com'
sumPage = 5
baseURL = 'http://www.baidu.com/s?wd='

#保存结果
resultList = []

header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def get_html(baseUrl,word,pn):
    url = baseUrl+urllib.request.quote(word)+'&pn='+str((pn-1)*10)
    req = urllib.request.Request(url, headers = header)
    oper = urllib.request.urlopen(req)
    html = oper.read()
    html = html.decode()
    return html

def filterHTML(html):
    html = html.replace('<b>', '')
    html = html.replace('</b>', '')
    html = html.replace('<em>', '')
    html = html.replace('</em>', '')
    return html

def find_domain(html,domain):
    if type(html) !='bs4.BeautifulSoup':
        html = BeautifulSoup(html)
    #过滤script和style
    cont = 0
    while cont < len(html.find_all('script')):
        html.script.extract() 
    while cont < len(html.find_all('style')):
        html.style.extract()
    
    item = html.find_all('span',text=re.compile(domain))
    return item

def get_rank(item):
    for result in item:
        rank = get_sort(result)
        title = get_title(result)[0]
        rankUrl = get_title(result)[1]
        description = get_description(result)
        get_pageurl(result)
        item = (word,rank,title,description,rankUrl)
        resultList.append(item)
    return

def get_sort(res):
    sort = res.find_previous('div',id=re.compile("^\d{1,2}")).get('id')
    return sort

def get_title(res):
    if res.find_previous('h3') != None:
        title = res.find_previous('h3').get_text()
        if res.find_previous('h3').a != None:
            link = res.find_previous('h3').a.get('href')
        else:
            link = -1
        rankUrl =  get_pageurl(link)
    elif res.find_previous('h4') != None:
        title = res.find_previous('h4').get_text()
        if res.find_previous('h4').a != None:
            link = res.find_previous('h4').a.get('href')
        else:
            link = -1
        rankUrl =  get_pageurl(link)
    else:
        title ='无法获取标题'
        rankUrl ='无法获取链接'
    return title,rankUrl

def get_description(res):
    if res.find_previous('div',class_='c-abstract') !=None:
        description = res.find_previous('div',class_='c-abstract').get_text(strip=True)
    elif res.find_previous('div',class_='c-span18') !=None:
        if res.find_previous('div',class_='c-span18').p !=None:
            description = res.find_previous('div',class_='c-span18').p.get_text(strip=True)
        else:
            description = res.find_previous('div',class_='c-span18').get_text(strip=True)
    elif res.find_previous('div',class_='ecl-weigou-list') != None:
        description = res.find_previous('div',class_='ecl-weigou-list').get_text(strip=True)#百度微购
    elif res.find_previous('div',class_='c-offset') != None:
        description = res.find_previous('div',class_='c-offset').get_text(strip=True)#百度新闻
    elif res.find_previous('div',class_='op-koubei2-main') != None:
        description = res.find_previous('div',class_='op-koubei2-main').get_text(strip=True)#百度口碑
    elif res.find_previous('div',class_='op_shares_simple') != None:
        description = res.find_previous('div',class_='op_shares_simple').get_text(strip=True)#新浪财经
    elif res.find_previous('div',class_='c-span24') != None:
        description = res.find_previous('div',class_='c-span24').get_text(strip=True)#百科
    elif res.find_previous('div',class_='c-border') != None:   #百度的许多产品有框
        if res.find_previous('div',class_='op_jingyan_list1') != None:
            description = res.find_previous('div',class_='op_jingyan_list1').get_text(strip=True)#百度经验
            if res.find_previous('div',class_='op_jingyan_list2') != None:
                description = description + res.find_previous('div',class_='op_jingyan_list2').get_text(strip=True)#百度经验
        elif res.find_previous('div',class_='op-taginfo-cont') != None:
            description = res.find_previous('div',class_='op-taginfo-cont').get_text(strip=True) #礼物说等
        else:
            description = res.find_previous('div',class_='c-border').get_text(strip=True)#先输出框的内容，可能会有的js代码没有过滤
    elif res.find_previous('p',class_='f13') != None:
        description = res.find_previous('p',class_='f13').get_text(strip=True)#天猫屏蔽提示，可能不准
    else:
        description = '无法提取描述'   
    return description

def get_pageurl(link):
    if -1 == link:
        pageurl ='无链接'
    else:
        pageurl ='URL'
    return pageurl

for word in kw_list:
    for pn in range(1,sumPage+1):
        #print('打开页面',int(time.clock()))  速度慢，用于测试
        print(word.strip(),' 第',pn,'页')
        html = get_html(baseURL,word,pn)
        #print('页面分析',int(time.clock())) 速度慢，用于测试
        html = filterHTML(html)
        if domain in html:
            item = find_domain(html,domain)
            rank = get_rank(item)

for item in resultList:
    print(item[0].strip(),'\t',item[1],'\t',item[2],'\t',item[3],'\t',item[4],'\n')
print("查询了 ",len(kw_list),'个关键词，前',sumPage,'页的结果，累计分析了',len(kw_list)*sumPage,'个页面')
print('运行耗时：',int(time.clock() - startTime),'秒')
