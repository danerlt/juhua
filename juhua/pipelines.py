# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import log
from scrapy.exceptions import DropItem

SETTINGS = get_project_settings()


class MySQLPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        # Instantiate DB
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host=SETTINGS['DB_HOST'],
                                            user=SETTINGS['DB_USER'],
                                            passwd=SETTINGS['DB_PASSWD'],
                                            port=SETTINGS['DB_PORT'],
                                            db=SETTINGS['DB_DB'],
                                            charset='utf8',
                                            use_unicode=True,
                                            cursorclass=MySQLdb.cursors.DictCursor
                                            )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item
        pass

    def _insert_record(self, tx, item):
        pass

    def _handle_error(self, e):
        log.err(e)


class ProductPipeline(MySQLPipeline):
    def process_item(self, item, spider):
        attr_names = ['name', 'link', 'shop_name', 'sales_num', 'price', 'resource']
        for attr in attr_names:
            if attr not in item:
                raise DropItem("%s没有%s属性" % (item, attr))
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):
        select_sql = u"SELECT id from product where name like '%s'"
        tx.execute(select_sql % (item["name"],))
        result = tx.fetchone()
        if result is None:
            sql = u'INSERT INTO product(`name`,`link`,`shop_name`,`sales_num`,`price`,`resource`)' \
                  u'VALUES ("%s", "%s", "%s", "%d", "%f", "%s")'
            tx.execute(sql % (item["name"], item["link"], item["shop_name"], item["sales_num"],
                              item["price"], item["resource"]
                              )
                       )


class ProductInfoPipeline(MySQLPipeline):
    def process_item(self, item, spider):
        attr_names = ['name', 'origin_price', 'real_price', 'brand', 'address', 'category',
                      'weight', 'quality_guarantee_period', 'pack_type', 'monthly_sales', 'resource']
        for attr in attr_names:
            if attr not in item:
                raise DropItem("%s没有%s属性" % (item, attr))
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):
        select_sql = u"SELECT id from product_info where name like '%s'"
        tx.execute(select_sql % (item["name"],))
        result = tx.fetchone()
        if result is None:
            sql = u'INSERT INTO product_info(`name`,`origin_price`,`real_price`,`brand`,`address`,`category`,' \
                  u'`weight`,`quality_guarantee_period`,`pack_type`,`monthly_sales`,`resource`) ' \
                  u'VALUES ("%s", "%f", "%f", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s")'
            tx.execute(sql % (item["name"], item["origin_price"], item["real_price"], item["brand"], item["address"],
                              item["category"], item["weight"], item["quality_guarantee_period"], item["pack_type"],
                              item["monthly_sales"], item["resource"]
                              )
                       )
            pass
