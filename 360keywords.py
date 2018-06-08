#encoding:UTF-8
'''
Created on 2015-6-6
功能：采集360下拉推荐关键词
@author: X240
'''
import urllib.request
import re

keyword = input("请输入查询的关键词:\n")

#keywords = ['第壹投','p2p理财']
keyword = urllib.request.quote(keyword)

url = "http://sug.so.360.cn/suggest?callback=suggest_so&encodein=utf-8&encodeout=utf-8&format=json&fields=word,obdata&word="
url = url+keyword

urlsg = "http://w.sugg.sogou.com/sugg/ajaj_json.jsp?key="+keyword+"&type=web&ori=yes&pr=web&abtestid=1&ipn="

'''
opener = urllib.request.build_opener()
opener.addheaders = ['Host','sug.so.360.cn']
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0')]
opener.addheaders = ['Accept','*/*']
opener.addheaders = ['Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3']
opener.addheaders = ['Accept-Encoding','gzip, deflate']
opener.addheaders = ['Referer','http://www.haosou.com/']
'''

res = urllib.request.urlopen(url)
keylist = res.read()
keylist = keylist.decode('UTF-8')

rl = r'"word":"(.*?)","obdata'
rl = re.compile(rl)
word = re.findall(rl, keylist)

fileHandle = open ( 'keywords.txt', 'w' )  

#print("360推荐关键词：")
fileHandle.write("360推荐关键词：\n")
for ky in word:
    fileHandle.write(ky+"\n")
    #print(ky)
    
#搜狗    
ressg = urllib.request.urlopen(urlsg)
keylistsg = ressg.read()
keylistsg = keylistsg.decode('GBK')

rlsg = r'"(\D.*?)"'
rlsg = re.compile(rlsg)
wordsg = re.findall(rlsg, keylistsg)

#print("\n\n搜狗推荐关键词：")
fileHandle.write("\n\n搜狗推荐关键词：")
for ky2 in wordsg:
    if len(ky2) >= 4:
        fileHandle.write("\n"+ky2)
        #print(ky2)
 
fileHandle.close()
print("采集完毕，请查看keywords.txt文件。。。")
