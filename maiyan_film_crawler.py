# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 22:47:18 2018

@author: rarestzhou
"""

'''爬取猫眼电影排行榜'''



import requests
import re
import json
from requests.exceptions import RequestException
import time

'''抓取首页:'''
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        return None
    
    
    

'''正则提取：排名、图片、电影名、主演、发布时间、评分等'''
def parse_on_page(html):
    pattern = re.compile('<dd>.*?board.*?>(.*?)</i>.*?data-src="(.*?)".*?'
                        + 'name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?'
                        + 'releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>'
                        + '.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        print (item)
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actors': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'releasetime': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

# parse_on_page(main())


'''写入文件：需要对字典进行序列化 --> json.dumps()'''
def write_into_file(content):
    with open('maoyan_top_movies.txt', 'a', encoding='utf-8') as f:
        # print (type(json.dumps(content))) # <class 'str'>
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


'''分页爬取:每页 10 条数据，每次切换到下一页 offset 就加 10'''
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    
    for item in parse_on_page(html):
        print (item)
        write_into_file(item)
        
# main()
        
if __name__ == '__main__':
    for page_offset in range(10):
        main(offset=page_offset * 10)
        time.sleep(1) # 延时 1 s


