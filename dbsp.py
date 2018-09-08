import requests
from requests.exceptions import RequestException
from selenium import webdriver
from lxml import etree
import re
import pymongo

def get_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
        'Host':'movie.douban.com'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(response):
    response1 = re.sub('<p\sclass="spoiler-tip">.*?</p>|&nbsp', '', response)
    response = etree.HTML(response)
    title = response.xpath('//div[contains(@class, "main")]/a[contains(@class, "subject-img")]/img/@title')
    name = response.xpath('//header[@class="main-hd"]/a[2]/text()')
    time = response.xpath('//header[@class="main-hd"]/span[2]/text()')
    h2 = response.xpath('//div[@class="main-bd"]/h2/a/text()')
    pattern = re.compile('<div\sclass="short-content">(.*?)\(', re.S)
    content = re.findall(pattern, response1)
    userful = response.xpath('//a[@href="javascript:;"]/span[contains(@id,"r-useful_count")]/text()')
    unuserful = response.xpath('//a[@href="javascript:;"]/span[contains(@id,"r-useless_count")]/text()')
    reply = response.xpath('//a[@class="reply"]/text()')
    for item in range(len(title)):
        yield{
            'title':title[item],
            'name':name[item],
            'time':time[item],
            'h2':h2[item],
            'content':content[item].replace(';', '').strip(),
            'userful':userful[item].strip(),
            'unuserful':unuserful[item].strip(),
            'reply':reply[item].strip()
        }


def write_to_mongo(item):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['dbsp']
    collection = db['dbsp'].insert(item)

def main(i):
    url = 'https://movie.douban.com/review/best/?start={}'.format(i*10)
    response = get_page(url)
    for item in parse_page(response):
        write_to_mongo(item)

if __name__ == "__main__":
    for i in range(5)
        main(i)
