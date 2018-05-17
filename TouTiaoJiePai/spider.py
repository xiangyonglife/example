import requests
import json
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from TouTiaoJiePai import config
import pymongo
from hashlib import md5
import os

client = pymongo.MongoClient(config.MANGO_URL)
db = client[config.MANGO_DB]
headline = db[config.MANGO_TABLE]


def get_page_index(offset, keyword):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/'
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException as e:
        print('请求索引页失败')
        return None


def parse_page_index(html):
    result = json.loads(html)
    if result and 'data' in result.keys():
        for item in result.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    browser = webdriver.Chrome()
    browser.get(url)
    return browser.page_source
    browser.close()


def parse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    image_pattern = re.compile('gallery: JSON.parse\((.*?)\)', re.S)
    result = re.search(image_pattern, html)
    if result:
        data_string = result.group(1)
        data = json.loads(json.loads(data_string))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_images(image)

            return {
                'title': title,
                'image': images
            }


def save_to_mongodb(result):
    if result:
        if headline.insert(result):
            print('存储到MONGODB成功', result)
            return True
        print('插入数据库失败', result)
        return False
    print('数据为空')
    return False


def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        if url:
            html = get_page_detail(url)
            result = parse_page_detail(html)
            save_to_mongodb(result)


def download_images(url):
    print('正在下载：'+url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except requests.RequestException as e:
        print('图片下载出错'+e)


def save_images(content):
    fielpath = {0}/{1}/{2}.format(os.getcwd(), md5(content).hexdigest, 'jpg')
    if not os.path.exists(fielpath):
        with open(fielpath, 'wb') as f:
            f.write(content)


if __name__ == '__main__':
    for i in headline.find():
        print(i)
