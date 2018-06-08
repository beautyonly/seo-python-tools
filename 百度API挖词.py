#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests,json,csv,sys,os,time,codecs

def convert_to_builtin_type(obj):
    d = {}
    d.update(obj.__dict__)
    return d

class AuthHeader():

    def __init__(self, username=None,password=None,token=None,target=None,accessToken=None): 
        self.username=username
        self.password=password
        self.token=token
        self.target=target
        self.accessToken=accessToken
        self.action='API-SDK'


    def setUsername(self,username):
        self.username=username
    def setPassword(self,password):
        self.password=password
    def setToken(self,token):
        self.token=token
    def setTarget(self,target):
        self.target=target
    def setAccessToken(self,accessToken):
        self.accessToken=accessToken

class JsonEnvelop():
    header=None
    body=None

    def __init__(self,aheader=None,abody=None):
        self.header=aheader
        self.body=abody
    def setHeader(self,header):
        self.header=header
    def setBody(self,body):
        self.body=body

failwords = open('未采集关键词.txt','w')

#记录开始时间，count作用是计数同时作为文件名增量
starttime = time.strftime('%Y/%m/%d %H:%M:%S')
count = 0

#3种请求，header和headers是一样的
header = AuthHeader(username='',password='',token='')
headers = {'content-type': 'application/json;charset=utf-8'}

#三个接口的地址
url1 = 'https://api.baidu.com/json/sms/v4/KRService/getKRFileIdByWords'
url2 = 'https://api.baidu.com/json/sms/v4/KRService/getFileStatus'
url3 = 'https://api.baidu.com/json/sms/v4/KRService/getFilePath'


#逐行读取文件，每100个生成一个列表作为请求数据
text = open('keywords.txt','r',encoding='utf-8').readlines()
while text:
    lines = text[:100]
    text = text[100:]
    seedWords = []
    for i in lines:
        seedWords.append(i.strip())


    #请求文件ID
    request1 = {'seedWords':seedWords,'seedFilter': {'device':0,'competeLow':0,}}
    jsonEnv1 = JsonEnvelop(header,request1)
    jsonStr1=json.dumps(jsonEnv1, default=convert_to_builtin_type, skipkeys=True)

    while True:
        try:
            print('请求文件ID')
            r1 = requests.post(url1,data=jsonStr1,headers=headers)
        except:
            time.sleep(30)
            continue
        else:
            try:
                time.sleep(3)
                fileId = r1.json()['body']['data'][0]['fileId']
            except:
                print('请求文件ID：请求出错，等待30s')
                time.sleep(30)
            else:
                break

    #根据文件ID查询文件生成状态
    request2 = {"fileId":fileId}
    jsonEnv2 = JsonEnvelop(header,request2)
    jsonStr2=json.dumps(jsonEnv2, default=convert_to_builtin_type, skipkeys=True)
    times = 1
    con = 0

    while True:
        time.sleep(5)
        print('请求文件状态')
        r2 = requests.post(url2,data=jsonStr2,headers=headers)
        try:
            time.sleep(7)
            filestatus = r2.json()['body']['data'][0]['isGenerated']
        except:
            print('获取文件状态：请求失败，30s后重试')
            time.sleep(30)
        else:
            if filestatus == 3:
                break
            elif filestatus != 3 and times %3 != 0:
                print('获取文件状态：文件处理中……')
                times = times + 1
            elif times %3 == 0:
                print('获取文件状态：接口阻塞，等待10min，%s' %time.strftime('%H:%M:%S'))
                print('当前文件id %s' %fileId)
                for i in lines:
                    failwords.write(i)
                times = times + 1
                con = 1
                time.sleep(610)
                break

    #如果等了10分钟，则之前的fileId已经因为超时下载不到文件了，可以选择跳过之后的获取部分
    if con == 1:
        continue

    #获取文件路径
    request3 = {"fileId":fileId}
    jsonEnv3 = JsonEnvelop(header,request3)
    jsonStr3=json.dumps(jsonEnv3, default=convert_to_builtin_type, skipkeys=True)

    while True:
        print('请求文件路径')
        r3 = requests.post(url3,data=jsonStr3,headers=headers)
        try:
            time.sleep(3)
            filePath = r3.json()['body']['data'][0]['filePath']
        except:
            print('请求文件路径：请求失败，30s后重试')
            time.sleep(30)
        else:
            break


    #设置文件名
    count = count + 1
    filename = time.strftime('%Y-%m-%d') + '-' + str(count) + '.csv'

    #下载文件
    r = requests.get(filePath)
    with open('%s' %filename,"wb") as file:
        file.write(r.content)
    print('文件%s下载完成' %filename)


#记录结束时间
endtime = time.strftime('%Y/%m/%d %H:%M:%S')
print('耗时：%s  -  %s' %(starttime,endtime))

failwords.close()
