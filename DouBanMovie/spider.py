import re
import requests
import  json


def get_one_pages(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<li.*?class="item".*?<em.*?>(.*?)</em>.*?<img.*?src="(.*?)".*?>'
                         + '*?<span.*?>(.*?)</span>.*?<span.*?>(.*?)'
                         + '</span>.*?<span.*?>(.*?)</span>.*?bd.*?<p.*?>(.*?)<br>(.*?)</p>'
                         + '.*?star.*?<span.*?property="v:average">(.*?)</span>.*?<span>'
                         + '(.*?)</span>.*?quote.*?<span.*?>(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    try:
        for item in items:
            yield {
                'top': item[0],
                'movie': item[2],
                'score': item[7],
                'sum': item[8],
                'director': re.split('&nbsp;', item[5].strip()[4:])[0],
                'actor': re.split('&nbsp;', item[5].strip()[4:])[3],
                'time': re.split('&nbsp;', item[6].strip())[0],
                'type': re.split('&nbsp;', item[6].strip())[4],
                'country': re.split('&nbsp;', item[6].strip())[2],
                'image': item[1]

            }
    except Exception as e:
        print(e)



def write_to_file(content):
    with open('movies.text', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()


def main(offset):
    url = 'https://movie.douban.com/top250?start='+str(offset)
    html = get_one_pages(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    for i in range(25):
        main(i*25)




