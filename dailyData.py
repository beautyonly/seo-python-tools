import requests,datetime,csv,time
from bs4 import BeautifulSoup 

#定义生成URL的函数
def makeURL(start,end,plat='gb',srctype='SEO'): #默认参数设置为前一天
    URL = 'http://data.to8to.com/Business/ViewReport/pid/1311?cid=7903&Date_turning=&date_type=0&order_name=stat_Date&order_value=desc&chart_type=3&date_start=%s&date_end=%s&sel_1=plat_type*_*%s&sel_2=channelname*_*gb&sel_3=channelname2*_*summary&sel_4=srctype*_*%s' %(start,end,plat,srctype)
    return URL

def text(tag):
    return tag.get_text()

#前期准备
cookies = dict(cookies_are='')  #暂时手动填
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
lastweek = (datetime.date.today() - datetime.timedelta(days=8)).strftime('%Y%m%d')
channels = ['效果图','学装修','新闻中心','装修攻略','问答','城市站']
header = ['频道',lastweek,yesterday,'差值','比值']
datas = []

try:
    r1 = requests.get(makeURL(lastweek,lastweek),cookies=cookies)
    time.sleep(2)
    r2 = requests.get(makeURL(yesterday,yesterday),cookies=cookies)
except:
    print('请求失败')
else:
    try:
        s1 = BeautifulSoup(r1.text,'lxml')
        for i in s1.findAll('tr','table_body'):
            line = i.findAll('td')
            channel = '%s%s' %(text(line[1]),texxt(line[2]))
            uv = int(text(line[5]))
            if channel[2:] in channels:
                tmp = [channel,uv]
                datas.append(tuple(tmp))
            else:
                continue

        s2 = BeautifulSoup(r2.text,'lxml')
        num = 0
        for i in s2.findAll('tr','table_body'):
            line = i.findAll('td')
            channel = '%s%s' %(text(line[1]),texxt(line[2]))
            uv = int(text(line[5]))
            if channel[2:] in channels:
                ct = datas[num]
                datas[num] = datas[num] + (uv,uv-ct[1],(uv-ct[1])/uv)
                num = num + 1
            else:
                continue
    except:
        print('返回数据有误')

with open('dailyData.csv', 'w', encoding='utf-8-sig') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(header)
    f_csv.writerows(datas)
