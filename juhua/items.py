# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def return_value(value):
    return value


def parse_num(value):
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
        return r'http' + value


class ProductItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class ProductItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(return_value)
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
        input_processor=MapCompose(parse_num)
    )


class ProductInfoItem(scrapy.Item):
    name = scrapy.Item()
    origin_price = scrapy.Item()
    real_price = scrapy.Item()
    brand = scrapy.Item()
    address = scrapy.Item()
    category = scrapy.Item()
    weight = scrapy.Item()
    quality_guarantee_period = scrapy.Item()
    monthly_sales = scrapy.Item()
    pack_type = scrapy.Item()
    authentication = scrapy.Item()
    resource = scrapy.Item()
