# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def return_value(value):
    return value


def parse_name(value):
    return value.strip()


def parse_price(value):
    return float(value)


def parse_sales_num(value):
    sales_num = 0;
    if u'万' in value:
        match = re.match(r'(\d+.\d+)', value)
        if match:
            sales_num = int(float(match.group(1)) * 10000)
    else:
        match = re.match(r'(\d+)', value)
        if match:
            sales_num = int(match.group(1))
    return sales_num


def parse_link(value):
    if r'https' not in value:
        return r'http:' + value


def parse_resource(value):
    if u'taobao' in value:
        value = '淘宝'
    elif u'tmall' in value:
        value = '天猫'
    elif u'jd' in value:
        value = '京东'
    return value


class MyItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class ProductItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(parse_name),
        output_processor=Join("")
    )
    link = scrapy.Field(
        input_processor=MapCompose(parse_link)
    )
    shop_name = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    sales_num = scrapy.Field(
        input_processor=MapCompose(parse_sales_num)
    )
    price = scrapy.Field(
        input_processor=MapCompose(parse_price)
    )
    resource = scrapy.Field(
        input_processor=MapCompose(parse_resource)
    )


class ProductInfoItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(parse_name)
    )
    origin_price = scrapy.Field(
        input_processor=MapCompose(parse_price)
    )
    real_price = scrapy.Field(
        input_processor=MapCompose(parse_price)
    )
    brand = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    address = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    category = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    weight = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    quality_guarantee_period = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    monthly_sales = scrapy.Field(
        input_processor=MapCompose(int)
    )
    pack_type = scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    resource = scrapy.Field(
        input_processor=MapCompose(parse_resource)
    )