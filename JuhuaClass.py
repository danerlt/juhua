import re
from _mysql import Error

from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql.cursors
from decimal import Decimal
from queue import Queue


class Taobao:


    def __init__(self):
        self.webdriver = webdriver.Chrome()  # 构造模拟浏览器
        self.webdriver.get('https://taobao.com')
        self.products = []
        self.product_infos = []
        self.page_url_queue = Queue()  # 产品列表页面url队列
        self.info_url_queue = Queue()  # 产品信息url队列
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
        self.webdriver.close()
        self.cursor.close()
        self.connect.close()

    def search(self, key=None):
        '''
        根据key搜索商品
        :param key: 关键字
        :return: 模拟浏览器
        '''
        self.webdriver.find_element_by_id('q').send_keys(key)
        self.webdriver.find_element_by_class_name('btn-search').click()
        page_num = self.get_page_num()
        base_url = r'https://s.taobao.com/search?q={0}&s={1}'
        for i in range(page_num):
            url = base_url.format(key, i * 44)
            self.page_url_queue.put(url)

    def get_page_num(self):
        '''
            获取页面数量
            :param firefox: 模拟浏览器
            :return: 页面数量
            '''
        page = self.webdriver.page_source
        soup = BeautifulSoup(page, 'lxml')
        comments = soup.find_all("div", class_="total")  # 匹配总的页数
        match = re.search(r'(\d+)', comments[0].text)  # 将数字页数提取
        page_num = int(match.group(0))
        return page_num  # 用于循环的次数设置

    def parse_product(self, url):
        '''
        解析商品列表页的数据
        :return: 商品列表数据
        '''
        self.webdriver.get(url)
        page = self.webdriver.page_source
        soup = BeautifulSoup(page, 'lxml')
        comments = soup.find_all("div", class_="ctx-box J_MouseEneterLeave J_IconMoreNew")
        for i in comments:
            data = []
            item = i.find_all("div", class_="row row-2 title")  # 相关信息
            product_name = item[0].text.strip()
            data.append(product_name)
            print('商品名： %s' % product_name)
            link = item[0].find('a').get('href')
            if 'https' not in link:
                link = 'http:' + link
            data.append(link)
            print('商品链接： %s' % link)

            shop_div = i.find_all("div", class_="row row-3 g-clearfix")
            for j in shop_div:
                a = j.find_all("span")
                shop_name = a[-1].text  # 店铺名称
                data.append(shop_name)
                print('店铺名称： %s' % shop_name)

            address_div = i.find_all('div', class_='location')
            shop_addr = address_div[0].text.strip()  # 店铺所在地
            data.append(shop_addr)
            print('店铺所在地： %s' % shop_addr)

            price_num_div = i.find_all("div", class_="row row-1 g-clearfix")
            for m in price_num_div:
                price_div = m.find_all('div', class_='price g_price g_price-highlight')
                price_str = price_div[0].text.strip()
                match = re.search(r'(\d+.\d+)', price_str)
                price = match.group(0)
                data.append(float(Decimal(price)))  # 商品价格
                print('价格: %.2f ' % float(Decimal(price)))

                num_div = m.find_all('div', class_='deal-cnt')
                num_str = num_div[0].text.strip()
                match = re.search(r'(\d+)', num_str)
                num = int(match.group(0))
                data.append(num)  # 购买人数
                print('购买人数: %d' % num)
            self.products.append(data)


    def get_id_by_name(self, name):
        sql = u"SELECT id FROM product where `name` like '{}'".format(name)
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        pid = row[0]
        return pid

    def insert_product(self, products=[]):
        try:
            count = 0
            for product in products:
                # 执行sql语句
                select_sql = u"SELECT id from product where name like '%s'"
                self.cursor.execute(select_sql % (product[0],))
                result = self.cursor.fetchone()
                if result is None:
                    sql = u"INSERT INTO product (name, link, shop_name, shop_addr, price, sales_num) VALUES ('%s', '%s', '%s', '%s', '%.2f', '%d')"
                    # data = ('艺福堂胎菊王新工艺 菊博士胎菊 正宗桐乡杭白菊花茶 茶叶花草茶', 'test', '艺福堂茗茶旗舰店', '浙江 杭州', float(Decimal('25.00')), 5701)
                    self.cursor.execute(sql % tuple(product))
                    # 提交到数据库执行
                    self.connect.commit()
                    count = count + 1
                    print("成功插入%d条数据" % count)
        except:
            # 如果发生错误则回滚
            self.connect.rollback()

    def insert_product_info(self, info=[]):
        # 插入数据
        sql = u"INSERT INTO product_info (pid, origin_price, real_price, monthly_sales, brand, province, city," \
              u" category, weight, quality_guarantee_period, pack_type)" \
              u" VALUES ('%s', '%.2f', '%.2f', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        try:
            # 执行sql语句
            self.cursor.execute(sql % tuple(info))
            # 提交到数据库执行
            self.connect.commit()
        except Error as e:
            # 如果发生错误则回滚
            self.connect.rollback()
            print(e)

    def cawl_product(self, key):
        self.search(key)
        while not self.page_url_queue.empty():
            url = self.page_url_queue.get()
            self.parse_product(url)
        self.insert_product(self.products)



    # 初始化产品详情url队列
    def init_info_url_queue(self):
        sql = u"SELECT link from  product where id not in (SELECT pid from product_info);"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            print(row[0])
            self.info_url_queue.put(row[0])

    def parse_product_info(self, url):
        try:
            self.webdriver.get(url)
            info = []
            page = self.webdriver.page_source
            soup = BeautifulSoup(page, 'lxml')
            attr_list = soup.select('.attributes-list > li')  # 淘宝属性列表
            origin_price = 0  # 原价
            real_price = 0  # 卖价
            monthly_sales = 0  # 月销量
            pid = None
            if attr_list:
                # 淘宝的数据
                name = soup.find(class_='tb-main-title').text.strip()
                pid = self.get_id_by_name(name)
                prices = soup.find_all(class_='tb-rmb-num')
                if len(prices) == 2:
                    origin_price = prices[0].text
                    real_price = prices[1].text
                    if real_price == '':
                        real_price = origin_price
                elif len(prices) == 1:
                    origin_price = prices[0].text
                    real_price = origin_price
                monthly_sales = 0  # 淘宝查看不了月销量 设置为0

                info.append(pid)
                info.append(float(Decimal(origin_price)))
                info.append(float(Decimal(real_price)))
                info.append(monthly_sales)
            else:
                attr_list = soup.select('#J_AttrUL > li')  # 天猫属性列表
                h1 = soup.select('.tb-detail-hd > h1')[0]
                name = h1.text.strip()
                pid = self.get_id_by_name(name)
                prices = soup.find_all(class_='tm-price')
                if len(prices) == 2:
                    origin_price = prices[0].text
                    real_price = prices[1].text
                    if real_price == '':
                        real_price = origin_price
                elif len(prices) == 1:
                    origin_price = prices[0].text
                    real_price = origin_price
                monthly_sales = int(soup.find(class_='tm-count').text)

                info.append(pid)
                info.append(float(Decimal(origin_price)))
                info.append(float(Decimal(real_price)))
                info.append(monthly_sales)
            my_dict = {}
            for item in attr_list:
                i = item.text.strip().split('：')
                if len(i) == 2:
                    key = i[0].strip()
                    value = i[1].strip()
                    my_dict.setdefault(key, value)
                else:
                    i = item.text.strip().split(':')
                    key = i[0].strip()
                    value = i[1].strip()
                    my_dict.setdefault(key, value)
            brand = my_dict.get('品牌')  # 品牌
            province = my_dict.get('省份')  # 省份
            city = my_dict.get('城市')  # 城市
            category = my_dict.get('茶种类')  # 菊花茶种类
            weight = my_dict.get('净含量')  # 净含量
            quality_guarantee_period = my_dict.get('保质期')  # 保质期
            pack_type = my_dict.get('包装种类')  # 包装种类

            info.append(brand)
            info.append(province)
            info.append(city)
            info.append(category)
            info.append(weight)
            info.append(quality_guarantee_period)
            info.append(pack_type)

            self.product_infos.append(info)
            self.insert_product_info(info)
            return info
        except Exception as e:
            print(e)

    def cawl_product_info(self):
        self.init_info_url_queue()
        while not self.info_url_queue.empty():
            url = self.info_url_queue.get()
            self.parse_product_info(url)


if __name__ == '__main__':
    t = Taobao()
    t.cawl_product('菊花茶')
    t.cawl_product_info()
    print("信息爬取完成")
