# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver
from scrapy.loader import ItemLoader
import pymysql
from juhua.items import ProductInfoItem, MyItemLoader


class JingdongProductInfoSpider(scrapy.Spider):
    name = 'jd_product_info'
    allowed_domains = ['item.jd.com']

    start_urls = ['http://item.jd.com/11806381868.html']
    # def start_requests(self):
        # self.connect = pymysql.Connect(host='127.0.0.1',
        #                                port=3306,
        #                                user='root',
        #                                passwd='123456',
        #                                db='juhua',
        #                                charset='utf8')
        # sql = r"SELECT link from  product where name not in (SELECT name from product_info) and resource like '京东'"
        # self.cursor = self.connect.cursor()
        # self.cursor.execute(sql)
        # results = self.cursor.fetchall()
        # for row in results:
        #     yield Request(url=row[0], callback=self.parse)

    def parse(self, response):
        # 通过ItemLoader加载Item
        item_loader = ProductItemLoader(item=ProductInfoItem(),  response=response)
        item_loader.add_css("name", ".sku-name::text")
        item_loader.add_css("origin_price", ".p-price > span:nth-child(2)::text")
        item_loader.add_css("real_price", ".p-price > span:nth-child(2)::text")
        item_loader.add_css("brand", "#parameter-brand > li  a::text")

        attr_lists = response.css("parameter2 p-parameter-list")

        item_loader.add_value("address", "")
        item_loader.add_value("category", "")
        item_loader.add_value("quality_guarantee_period", "")
        item_loader.add_value("pack_type", "")

        item_loader.add_value("resource", "京东")

        product_item = item_loader.load_item()
        yield product_item
