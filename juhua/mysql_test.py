import pymysql

from juhua.items import ProductItem
from decimal import Decimal


class MySQLTest(object):
    def __init__(self):
        self.connect = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='juhua',
            charset='utf8'
        )
        # 获取游标
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def test_insert_product(self):
        # item = ProductItem()
        item = {}
        item['name'] = 'test'
        item['link'] = 'http://item.jd.com/hhh'
        item['shop_name'] = '店铺名'
        item['sales_num'] = int(100)
        item['price'] = float(20.9)

        sql = u'INSERT INTO product(`name`,`link`,`shop_name`,`sales_num`,`price`) VALUES ("%s", "%s", "%s", "%d", "%f")'
        self.cursor.execute(sql % (item["name"], item["link"], item["shop_name"], (item["sales_num"]), (item["price"])))
        self.connect.commit()

if __name__ == '__main__':
    mysql_test = MySQLTest()
    mysql_test.test_insert_product()
