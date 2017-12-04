# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    start_urls = [r'https://search.jd.com/Search?keyword=%E8%8F%8A%E8%8A%B1%E8%8C%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&stock=1&page=1&s=1&click=0']
    # start_urls = ['https://taobao.com/']

    # def start_requests(self):
    #     key = '菊花'
    #     for i in range(0, 100):
    #         url = "https://s.taobao.com/search?q=" + str(key) + "&commend=all&search_type=item&s=" + str(44 * i)
    #         yield Request(url=url, callback=self.parse)

    def parse(self, response):
        body = response.body.decode("utf-8", "ignore")
        print(body)
