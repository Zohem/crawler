import scrapy
from bs4 import BeautifulSoup


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
        for p in soup.find_all('p'):
            retp.text.encode('utf-8')