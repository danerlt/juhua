# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver
from scrapy.loader import ItemLoader
from juhua.items import ProductItem, MyItemLoader


class JingdongSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = [
        r'https://search.jd.com/Search?keyword=%E8%8F%8A%E8%8A%B1%E8%8C%B6&enc=utf-8&'
        r'qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&stock=1&page=1&s=1&click=0']

    def start_requests(self):
        for i in range(1, 120):
            url = r"https://search.jd.com/Search?keyword=%E8%8F%8A%E8%8A%B1%E8%8C%B6&enc=utf-8" \
                  r"&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&stock=1&page={page}".format(page=i)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # 通过ItemLoader加载Item
        products = response.xpath("//li[@class='gl-item']")
        for product in products:
            item_loader = MyItemLoader(item=ProductItem(), selector=product, response=response)
            item_loader.add_css("name", ".p-name > a::attr(title)")
            item_loader.add_css("link", ".p-name > a::attr(href)")
            item_loader.add_css("shop_name", ".p-shop > span > a::attr(title)")
            item_loader.add_css("sales_num", ".p-commit > strong > a::text")
            item_loader.add_css("price", ".p-price > strong > i::text")
            item_loader.add_value("resource", "京东")
            product_item = item_loader.load_item()
            yield product_item
