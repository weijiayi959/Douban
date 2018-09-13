import json
from lxml import etree
import requests
from requests.exceptions import RequestException
import time
from multiprocessing import Pool


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    rehtml = etree.HTML(html)
    Url = rehtml.xpath('//div[@class="post"]/a/@href')   
    Photo = rehtml.xpath('//div[@class="post"]/a/img/@src')
    Title = rehtml.xpath('//div[@class="title"]/a/text()')
    Score = rehtml.xpath('//div[@class="rating"]/span[@class="rating_nums"]/text()')
    People = rehtml.xpath('//div[@class="rating"]/span[3]/text()')
    Author = rehtml.xpath('//div[@class="abstract"]//text()')
    for item in range(len(Url)):
        yield {
            'Url': Url[item],
            'Photo': Photo[item],
            'Title': Title[item].strip(),
            'Score': Score[item],
            'People': People[item][1:-1],
            'Author': Author[item].strip()[3:],
            'Polisher': Author[item+1].strip()[4:],
            'Year': Author[item+2].strip()[4:]
        }


def write_to_page(item):
    with open('douban3-2.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False)+'\n')


def main(i):
    url = 'https://www.douban.com/doulist/45004834/?start={}&sort=time&sub_type=4'.format(i*25)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_page(item)


if __name__ == '__main__':
    start = time.clock()
    pool = Pool()
    pool.map(main, [i for i in range(4)])
    pool.close()
    pool.join()
    end = time.clock()
    print('TIME', end-start)






