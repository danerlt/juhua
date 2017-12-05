# -*- coding: utf-8 -*-

import scrapy
import re
from juhua.items import ProductItem, MyItemLoader
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver


class TaobaoSpider(scrapy.Spider):
    name = "taobao"
    allowed_domains = ["taobao.com"]
    start_urls = ['https://taobao.com/']

    def __init__(self):
        self.brower = webdriver.Chrome()
        super(TaobaoSpider, self).__init__()
        dispatcher.connect(self.spider_close, signals.spider_closed)

    def spider_close(self, spider):
        self.brower.quit()

    def start_requests(self):
        key = "菊花茶"
        for i in range(1, 100):  # 定义爬虫页数
            url = "https://s.taobao.com/search?q=" + str(key) + "&commend=all&search_type=item&s=" + str(44 * i)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # 通过ItemLoader加载Item
        products = response.xpath("//div[@class='ctx-box J_MouseEneterLeave J_IconMoreNew']")
        for product in products:
            item_loader = MyItemLoader(item=ProductItem(), selector=product, response=response)
            item_loader.add_xpath("name", "string(div[@class='row row-2 title']/a)")
            # name = product.xpath("string(//div[@class='row row-2 title']/a)").extract()
            item_loader.add_css("link", ".title > a::attr(href)")
            item_loader.add_css("shop_name", ".shopname > span:nth-child(2)::text")
            item_loader.add_css("sales_num", ".deal-cnt::text", re="(\d+)")
            item_loader.add_css("price", ".price > strong::text")
            item_loader.add_css("resource", ".title > a::attr(href)")
            product_item = item_loader.load_item()
            # product_item["name"] = name
            yield product_item