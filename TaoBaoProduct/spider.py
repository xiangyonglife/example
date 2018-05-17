from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
from pyquery import PyQuery as Pq
from selenium.common import exceptions



browser = webdriver.Chrome()
wait_ = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.taobao.com/')
        input_ = wait_.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait_.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > '
                                                                          'div.search-button > button')))
        input_.send_keys('美食')
        submit.click()
        total = wait_.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > "
                                                                             "div > div > div.total")))
        get_products()
        return total.text
    except exceptions.TimeoutException:
        search()


def next_page(page_number):
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
            print(product)
    except exceptions.TimeoutException:
        return get_products()


def main():
    total = search()
    patter = re.compile('\d+', re.S)
    total = int(re.search(patter, total).group())
    for i in range(2, total+1):
        next_page(i)


if __name__ == '__main__':
    main()



