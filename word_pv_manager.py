#/usr/bin/env python3

from get_keywords_by_query import *
import mysql.connector
import sys
import time

#连接数据库
conn = mysql.connector.connect(user='root',password='',database='spider_result') #spider_result
cursor = conn.cursor()

def get_db_pv(query):
    cursor.execute('select pv from seo_keywords where keyword = %s',[query])
    sql_re = cursor.fetchall()
    if sql_re == [] or sql_re[0][0] == None:
        return None
    else:
        return sql_re[0][0]

def update_db(query):
    cursor.execute('SELECT COUNT(*) FROM `seo_keywords` WHERE id > 0')
    count = cursor.fetchall()[0][0]

    try:
        api_re = get_keywords(query)
    except:
        print('API 请求失败，等待重试')
        time.sleep(10)
    else:
        for d in api_re:
            cursor.execute(
                'INSERT INTO seo_keywords(keyword,pv) values(%s,%s) ON DUPLICATE KEY UPDATE pv = %s;',[d['word'],d['pv'],d['pv']])
        conn.commit()
        time.sleep(3)
        cursor.execute('SELECT COUNT(*) FROM `seo_keywords` WHERE id > 0')
        end_count = cursor.fetchall()[0][0]
        print('已更新 %s 个关键词日均；带日均关键词总数 %s' %(end_count - count,end_count))

if __name__ == "__main__":

    #处理传入参数
    try:
        sys.argv[1]
    except:
        print('---缺少必要的参数：请传入关键词文件')
    else:
        query_file = sys.argv[1]
    
    try:
        sys.argv[2]
    except:
        mode = 'search'
        print('---未传入程序运行模式，默认模式为 search')
    else:
        mode = sys.argv[2]

    querys = [ x.strip() for x in open(query_file,'r') ][5296:]

    #运行
    if mode == 'search':
        for query in querys:
            query_pv = get_db_pv(query)
            print(query_pv)
    elif mode == 'update':
        for query in querys:
            update_db(query)
    else:
        print('---程序运行模式输入错误：\n---\t search 查询关键词 pv\n---\tupdate 更新关键词库')
    
    conn.close()
