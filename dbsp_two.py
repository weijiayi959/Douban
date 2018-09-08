import requests
from requests.exceptions import RequestException
from lxml import etree
import pymongo


def get_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
        'Host':'movie.douban.com'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        return None


def parse_page(response):
     retitle=[]
     title = response.get('html')
     votes = response.get('votes')
     response = etree.HTML(title)
     response = response.xpath('//p//text()')
     for ele in response:
         ele=ele.strip()
         retitle.append(ele)
     comment = ''.join(retitle)
     yield{
         'comment': comment,
         'votes': votes
     }


def get_index(url):
     response1 = requests.get(url)
     response1 = etree.HTML(response1.text)
     index = response1.xpath('//div[@class="review-list chart "]/div/@data-cid')
     return index


def write_to_mongo(item):
    client = pymongo.MongoClient('localhost',27017)
    db = client['dbs']
    collection = db['dbsp']
    collection.insert(item)


def main(i):
    url = 'https://movie.douban.com/j/review/{}/full'.format(i)
    response = get_page(url)
    for item in parse_page(response):
        write_to_mongo(item)


if __name__ == "__main__":
    for a in range(5):
        url = 'https://movie.douban.com/review/best/?start={}'.format(a*10)
        for i in get_index(url):
            main(i)
