#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import json
from operator import itemgetter

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

def get_keywords(seedword):
    api = "https://api.baidu.com/json/sms/v4/KRService/getKRByQuery"
    header = AuthHeader(
                username='',
                password='',
                token='')
    body = {
        "queryType":1,
        "query":seedword,
        "seedFilter":{
            "device":0,
            "competerLow":0
             }
        }

    jsonEnv = JsonEnvelop(header,body)
    data = json.dumps(jsonEnv,default=convert_to_builtin_type, skipkeys=True)
    response = requests.post(api,data=data,
                             headers={'Content-Type':'application/json'})
    keywords = []
    for x in response.json()['body']['data']:
        if x['word'] != seedword:
            keywords.append({'word':x['word'],'pv':x['pv']})
        else:
            keywords.insert(0,{'word':seedword,'pv':x['pv']})

    return keywords

if __name__ == "__main__":
    seedword = sys.argv[1]
    keywords = get_keywords(seedword)
    print(seedword + ' : ' + str(keywords[0]['pv']))
    print('----------------------------------------------------------------')
    rows_by_pv = sorted(keywords[1:],key=itemgetter('pv'),reverse=True)
    for kd in rows_by_pv:
        print(kd['word'] + ' : ' + str(kd['pv']))
