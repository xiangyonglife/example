from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
from pyquery import PyQuery as Pq
from selenium.common import exceptions
from TaoBaoProduct import config
import pymongo

client = pymongo.MongoClient(config.MANGO_URL)
db = client[config.MANGO_DB]

browser = webdriver.PhantomJS(service_args=config.SERVICE_ARGEs)
wait_ = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)


def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com/')
        input_ = wait_.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait_.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > '
                                                                          'div.search-button > button')))
        input_.send_keys(config.KEYWORD)
        submit.click()
        total = wait_.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > "
                                                                             "div > div > div.total")))
        get_products()
        return total.text
    except exceptions.TimeoutException:
        search()


def next_page(page_number):
    print('正在翻页')
    try:
        input_ = wait_.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait_.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div >'
                                                                          ' div.form > span.btn.J_Submit')))
        input_.clear()
        input_.send_keys(page_number)
        submit.click()
        wait_.until(ec.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div >'
                                                                       ' ul > li.item.active > span'),
                                                     str(page_number)))
        get_products()
    except exceptions.TimeoutException:
        next_page(page_number)


def get_products():
    try:
        wait_.until(ec.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
        html = browser.page_source
        doc = Pq(html)
        items = doc('#mainsrp-itemlist .items .item').items()
        for item in items:
            product = {
                'title': item.find('.title').text(),
                'price': item.find('.price').text(),
                'pay': item.find('.deal-cnt').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text(),
                'image': item.find('.pic .img').attr('src'),

            }
            save_to_mongodb(product)
            print(product)
    except exceptions.TimeoutException:
        return get_products()


def save_to_mongodb(result):
    try:
        if db[config.MANGO_TABLE].insert(result):
            print('存储mongodb成功', result)
    except Exception:
        print('存储mongodb失败', result)


def main():
    try:
        total = search()
        patter = re.compile('\d+', re.S)
        total = int(re.search(patter, total).group())
        for i in range(2, total+1):
            next_page(i)
        browser.close()
    except Exception:
        print('出错啦')
    finally:
        browser.close()


if __name__ == '__main__':
     main()
    #for i in db[config.MANGO_TABLE].find():
        #print(i)



