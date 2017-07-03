import scrapy
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient


mongo = MongoClient()

class PageModel:

    client = None
    database_name = 'zohem_data_core'
    collection_name = 'pipe_crawl_data'
    collection = None

    def __init__(self,pageData,client=None):

        self.url = pageData['url']
        self.h1 = pageData['h1']
        self.h2 = pageData['h2']
        self.h3 = pageData['h3']
        self.h4 = pageData['h4']
        self.para = pageData['para']
        self.url = pageData['url']
        self.title = pageData['title']

        if client is None:
            self.client = MongoClient() # todo: configure for database arguments
        else:
            self.client = client
        self.collection = self.client[self.database_name][self.collection_name]

    def getDict(self):
        return {
            'url': self.url,
            'title': self.title,
            'h1': self.h1,
            'h2': self.h2,
            'h3': self.h3,
            'h4': self.h4,
            'para': self.para
        }

    def saveModel(self):
        dict = self.getDict()
        dict['timestamp'] = int(time.time()*1000)

        self.collection.insert(dict)

class TestSpider(scrapy.Spider):

    name = "test"
    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/English_Wikipedia'
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):

        soup = BeautifulSoup(response.body.decode('utf-8'),'lxml')

        retrive_para = []
        retrive_h1 = []
        retrive_h2 = []
        retrive_h3 = []
        retrive_h4 = []
        title = None

        body = soup.find('body')
        url = response.url

        try:
            title = soup.find('title').text
        except:
            title = None

        for p in body.find_all('p'):
            if len(p.text) > 0:
                retrive_para += [p.text]

        for h1 in body.find_all('h1'):
            retrive_h1 += [h1.text]

        for h2 in body.find_all('h2'):
            retrive_h2 += [h2.text]

        for h3 in body.find_all('h3'):
            retrive_h3 += [h3.text]

        for h4 in body.find_all('h4'):
            retrive_h4 += [h4.text]

        pageModel = PageModel({
            'url': url,
            'title': title,
            'h1': retrive_h1,
            'h2': retrive_h2,
            'h3': retrive_h3,
            'h4': retrive_h4,
            'para': retrive_para
        })

        pageModel.saveModel()
        print('continue to next page ')