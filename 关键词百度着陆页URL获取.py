'''
获取关键词百度着陆页URL脚本
从关键词搜索页中提取出排名靠前的土巴兔结果，然后访问并获取到跳转后的URL
'''

import requests,re,sys
from bs4 import BeautifulSoup
from multiprocessing import Process,Lock,cpu_count

def getLandurl(url):
    r = requests.get(url).text
    s = BeautifulSoup(r,'html.parser')
    divs = s.findAll('div',re.compile('result.*c-container.*'))
    for i in divs:
        if 'to8to' in i.find(True,'c-showurl').getText():
            landurl=i.h3.a['href']
            return landurl
            break

def getLocation(landurl):
    r2 = requests.get(landurl,allow_redirects=False)
    return r2.headers['Location']

if __name__ == '__main__':
    
    def writer(url):
        result = open('result.txt','a+')
        try:
            landurl = getLandurl(url)
            location = getLocation(landurl)
        except:
            result.write('%s\n' %k)
        else:
            result.write('%s\t%s\t%s\n' %(k,landurl,location))
        finally:
            result.close()
            
    keywords = open(sys.argv[1],'r').readlines()[:10]

    while len(keywords) != 0:

        cpus = cpu_count()
        lines = keywords[:cpus]
        keywords = keywords[cpus:]
        ps = []

        for k in lines:
            k = k.strip()
            url = 'http://www.baidu.com/s?wd=%s' %k
            p = Process(target=writer,args=(url,))
            ps.append(p)
            p.start()

        for p in ps:
            p.join()