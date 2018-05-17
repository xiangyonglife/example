from selenium  import webdriver

browser = webdriver.Chrome()

browser.get('http://toutiao.com/group/6555824945719411203/')
print(str(browser.page_source))
browser.close()