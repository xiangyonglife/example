import requests

head ={
    'authority': 'www.toutiao.com',
    'authority':'www.toutiao.com',
    'path':'/a6555775049909928452',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding:':'gzip, deflate, br',
    'cache-control':'max-age=0',
    'scheme':'https',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':'__tasessionId=r3fnl5lu51526469041847',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'

}
rsp = requests.get('https://www.toutiao.com/a6555775049909928452', head)
print(rsp.text)