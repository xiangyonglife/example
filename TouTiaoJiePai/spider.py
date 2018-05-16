import requests
import json
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import  time



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
        return  browser.page_source
        browser.close()





def parse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    yield {
        'title': title
    }


def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        if url:
           html = get_page_detail(url)
           for item in parse_page_detail(html):
               print(item)





if __name__ == '__main__':
    main()
