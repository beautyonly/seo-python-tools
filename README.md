学习 Python 中，此为平时写的琐碎代码


### SEO
- [bd抓取记录提取.py](https://github.com/ginsonwang/Python/blob/master/bd%E6%8A%93%E5%8F%96%E8%AE%B0%E5%BD%95%E6%8F%90%E5%8F%96.py) - 从网站日志中提取指定 URL 的百度蜘蛛抓取记录

- [get_keywords_by_query.py](https://github.com/ginsonwang/Python/blob/master/get_keywords_by_query.py) - 通过百度推广 API 查询单个关键词的搜索量及相关关键词

- [keyword2pattern.py](https://github.com/ginsonwang/Python/blob/master/keyword2pattern.py) - 将关键词转为 pattern ，如 '客厅装修' --> {空间}+'装修'，方便 SEO 拓展、布局关键词

- [seo数据采集.py](https://github.com/ginsonwang/Python/blob/master/seo%E6%95%B0%E6%8D%AE%E9%87%87%E9%9B%86.py) - 查询状态码、百度收录、排名工具

- [word_pv_manager.py](https://github.com/ginsonwang/Python/blob/master/word_pv_manager.py) - 从本地数据库查询关键词搜索量，若数据库中未查到，立即请求百度推广 API 获取数据并更新到数据库

- [下拉框关键词采集.py](https://github.com/ginsonwang/Python/blob/master/%E4%B8%8B%E6%8B%89%E6%A1%86%E5%85%B3%E9%94%AE%E8%AF%8D%E9%87%87%E9%9B%86.py) - 采集百度、搜狗、360 搜索下拉框关键词

- [关键词百度排名查询工具.py](https://github.com/ginsonwang/Python/blob/master/%E5%85%B3%E9%94%AE%E8%AF%8D%E7%99%BE%E5%BA%A6%E6%8E%92%E5%90%8D%E6%9F%A5%E8%AF%A2%E5%B7%A5%E5%85%B7.py) - 查询百度关键词排名及着陆页

- [关键词百度着陆页URL获取.py](https://github.com/ginsonwang/Python/blob/master/%E5%85%B3%E9%94%AE%E8%AF%8D%E7%99%BE%E5%BA%A6%E7%9D%80%E9%99%86%E9%A1%B5URL%E8%8E%B7%E5%8F%96.py) - 百度排名 URL 是百度的地址，会自动跳转，该脚本通过访问跳转链接获取着陆页真实 URL。
    - 以前可以直接 head 请求百度搜索结果网址，通过返回头信息的 Locaiton 字段获取跳转后 URL，后来被百度改掉了


### 其他
- [baseX.py](https://github.com/ginsonwang/Python/blob/master/baseX.py) - 10 进制与任意进制转换，最多 62 进制，来源 [stackoverflow](https://stackoverflow.com/questions/1119722/base-62-conversion) 
