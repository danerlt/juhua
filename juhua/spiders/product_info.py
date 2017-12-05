# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from selenium import webdriver
from scrapy.loader import ItemLoader
import pymysql
from juhua.items import ProductInfoItem, MyItemLoader


class ProductInfoSpider(scrapy.Spider):
    name = 'product_info'
    allowed_domains = ['detail.tmall.com', 'item.taobao.com', 'item.jd.com']

    start_urls = ['http://detail.tmall.com/item.htm?id=41828566996&ns=1&abbucket=0']

    def parse(self, response):
        self.connect = pymysql.Connect(host='127.0.0.1',
                                       port=3306,
                                       user='root',
                                       passwd='123456',
                                       db='juhua',
                                       charset='utf8')
        sql = r"SELECT link,price FROM  product WHERE name NOT IN (SELECT name FROM product_info) "
        self.cursor = self.connect.cursor()
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            url = row[0]
            price = row[1]
            if 'taobao' in url:
                yield Request(url=url, meta={'price': price}, callback=self.parse_taobao)
            elif 'tmall' in url:
                yield Request(url=url, meta={'price': price}, callback=self.parse_tmall)
            elif 'jd' in url:
                yield Request(url=url, meta={'price': price}, callback=self.parse_jd)

    def parse_taobao(self, response):
        # 提取属性
        attr_lists = response.css(".attributes-list > li::text").extract()
        my_dict = {}.fromkeys(('品牌', '省份', '城市', '茶种类', '净含量', '保质期', '包装种类'), "NULL")
        if attr_lists:
            for item in attr_lists:
                i = item.strip().split(':')
                key = i[0].strip()
                value = i[1].strip()
                my_dict[key] = value
        brand = my_dict.get('品牌')  # 品牌
        province = my_dict.get('省份')  # 省份
        city = my_dict.get('城市')  # 城市
        category = my_dict.get('茶种类')  # 菊花茶种类
        weight = my_dict.get('净含量')  # 净含量
        quality_guarantee_period = my_dict.get('保质期')  # 保质期
        pack_type = my_dict.get('包装种类')  # 包装种类

        # 通过ItemLoader加载Item
        item_loader = MyItemLoader(item=ProductInfoItem(), response=response)
        item_loader.add_css('name', ".tb-main-title::text")
        item_loader.add_css('origin_price', "#J_StrPrice > .tb-rmb-num::text")
        item_loader.add_value('real_price', response.meta['price'])
        item_loader.add_value('brand', brand)
        item_loader.add_value("address", str(province) + str(city))
        item_loader.add_value("category", category)
        item_loader.add_value("weight", weight)
        item_loader.add_value("quality_guarantee_period", quality_guarantee_period)
        item_loader.add_value("monthly_sales", 0)  # 销量为0,表示查看不了销量
        item_loader.add_value("pack_type", pack_type)
        item_loader.add_value("resource", response.url)

        product_item = item_loader.load_item()
        yield product_item

    def parse_tmall(self, response):
        # 提取属性
        attr_lists = response.css("#J_AttrUL > li::text").extract()
        my_dict = {}.fromkeys(('品牌', '省份', '城市', '茶种类', '净含量', '保质期', '包装种类'), None)
        if attr_lists:
            for item in attr_lists:
                i = re.split('[：|:]', item.strip())
                key = i[0].strip()
                value = i[1].strip()
                my_dict[key] = value
        brand = my_dict.get('品牌')  # 品牌
        province = my_dict.get('省份')  # 省份
        city = my_dict.get('城市')  # 城市
        category = my_dict.get('茶种类')  # 菊花茶种类
        weight = my_dict.get('净含量')  # 净含量
        quality_guarantee_period = my_dict.get('保质期')  # 保质期
        pack_type = my_dict.get('包装种类')  # 包装种类
        origin_price = 0.0 # 天猫原价是动态加载的，只能在脚本里去使用正则匹配
        match = re.search('"reservePrice":.*?(\d+.\d+)', response.text)
        if match:
            origin_price = float(match.group(1).strip())
        # 通过ItemLoader加载Item
        item_loader = MyItemLoader(item=ProductInfoItem(), response=response)
        item_loader.add_css('name', ".tb-detail-hd > h1::text")
        item_loader.add_value('origin_price', origin_price)
        item_loader.add_value('real_price', response.meta['price'])
        item_loader.add_value('brand', brand)
        item_loader.add_value("address", str(province) + str(city))
        item_loader.add_value("category", category)
        item_loader.add_value("weight", weight)
        item_loader.add_value("quality_guarantee_period", quality_guarantee_period)
        item_loader.add_css("monthly_sales", ".tm-count::text")
        item_loader.add_value("pack_type", pack_type)
        item_loader.add_value("resource", response.url)

        product_item = item_loader.load_item()
        yield product_item

    def parse_jd(self, response):
        # 提取属性
        attr_lists = response.xpath("//ul[@class='parameter2 p-parameter-list']/li/text()").extract()
        my_dict = {}.fromkeys(('商品产地', '分类', '包装', '品牌', '净含量', '保质期'), "NULL")
        if attr_lists:
            for item in attr_lists:
                i = re.split('：', item.strip())
                key = i[0].strip()
                value = i[1].strip()
                my_dict[key] = value
        address = my_dict.get('商品产地')  # 省份
        category = my_dict.get('分类')  # 菊花茶种类
        pack_type = my_dict.get('包装')  # 包装种类
        # 规格与包装中的参数
        param_names = response.css(".Ptable-item > dl > dt::text").extract()
        param_values = response.css(".Ptable-item > dl > dd::text").extract()
        for i in range(len(param_names)):
            my_dict[param_names[i]] = param_values[i]
        brand = my_dict.get('品牌')  # 品牌
        weight = my_dict.get('净含量')  # 净含量
        quality_guarantee_period = my_dict.get('保质期')  # 保质期

        # 通过ItemLoader加载Item
        item_loader = MyItemLoader(item=ProductInfoItem(), response=response)
        item_loader.add_css('name', ".sku-name::text")
        item_loader.add_value('origin_price', response.meta['price']) # 京东上面没有原价，只有一个京东价
        item_loader.add_value('real_price', response.meta['price'])
        item_loader.add_value('brand', brand)
        item_loader.add_value("address", address)
        item_loader.add_value("category", category)
        item_loader.add_value("weight", weight)
        item_loader.add_value("quality_guarantee_period", quality_guarantee_period)
        item_loader.add_value("monthly_sales", 0)  # 销量为0,表示查看不了销量
        item_loader.add_value("pack_type", pack_type)
        item_loader.add_value("resource", response.url)

        product_item = item_loader.load_item()
        yield product_item
