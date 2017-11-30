import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql.cursors
from decimal import Decimal


def init():
    firefox = webdriver.Chrome()  # 构造模拟浏览器
    firefox.get('https://taobao.com')  # 淘宝页面
    return firefox


def search(firefox, key):
    '''
    根据key搜索商品
    :param firefox:  模拟浏览器
    :param key: 关键字
    :return: 模拟浏览器
    '''
    firefox.find_element_by_id('q').send_keys(key)
    firefox.find_element_by_class_name('btn-search').click()
    return firefox


def getPageNum(firefox):
    '''
    获取页面数量
    :param firefox: 模拟浏览器
    :return: 页面数量
    '''
    page = firefox.page_source
    soup = BeautifulSoup(page, 'lxml')
    comments = soup.find_all("div", class_="total")  # 匹配总的页数
    pattern = re.compile(r'[0-9]')
    pageNum = pattern.findall(comments[0].text)  # 将数字页数提取
    pageNum = int(pageNum[0])
    return pageNum  # 用于循环的次数设置


# 点击下一页 //更新数据。
def nextPage(firefox):
    firefox.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]').click()  # 点击下一页ajax刷新数据


def obtainHtml(firefox):
    page = firefox.page_source
    soup = BeautifulSoup(page, 'lxml')
    comments = soup.find_all("div", class_="ctx-box J_MouseEneterLeave J_IconMoreNew")
    for i in comments:
        data = []
        Item = i.find_all("div", class_="row row-2 title")  # 相关信息
        product_name = Item[0].text.strip()
        data.append(product_name)
        print('商品名： %s' % product_name)

        link = 'http:' + Item[0].find('a').get('href')
        data.append(link)
        print('商品链接： %s' % link)

        shopDiv = i.find_all("div", class_="row row-3 g-clearfix")
        for j in shopDiv:
            a = j.find_all("span")
            shop_name = a[-1].text  # 店铺名称
            data.append(shop_name)
            print('店铺名称： %s' % shop_name)

        addressDiv = i.find_all('div', class_='location')
        shop_addr = addressDiv[0].text.strip()  # 店铺所在地
        data.append(shop_addr)
        print('店铺所在地： %s' % shop_addr)

        priceAndNumDiv = i.find_all("div", class_="row row-1 g-clearfix")
        for m in priceAndNumDiv:
            priceDiv = m.find_all('div', class_='price g_price g_price-highlight')
            priceStr = priceDiv[0].text.strip()
            match = re.search(r'(\d+.\d+)', priceStr)
            price = match.group(0)
            data.append(float(Decimal(price)))  # 商品价格
            print('价格: %.2f ' % float(Decimal(price)))

            numDiv = m.find_all('div', class_='deal-cnt')
            numStr = numDiv[0].text.strip()
            match = re.search(r'(\d+)', numStr)
            num = int(match.group(0))
            data.append(num)  # 购买人数
            print('购买人数: %d' % num)
        # insert_data(data)


def insert_data(data=[]):
    # 连接数据库
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='juhua',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    # 插入数据
    sql = u"INSERT INTO product (name, link, shop_name, shop_addr, price, sales_num) VALUES ('%s', '%s', '%s', '%s', '%.2f', '%d')"
    # data = ('艺福堂胎菊王新工艺 菊博士胎菊 正宗桐乡杭白菊花茶 茶叶花草茶', 'test', '艺福堂茗茶旗舰店', '浙江 杭州', float(Decimal('25.00')), 5701)
    cursor.execute(sql % tuple(data))
    connect.commit()
    print('成功插入', cursor.rowcount, '条数据')
    # 关闭连接
    cursor.close()
    connect.close()


if __name__ == '__main__':
    # insert_data()
    firefox = init()
    firefox = search(firefox, '菊花')
    num = getPageNum(firefox)
    for i in range(num):
        obtainHtml(firefox)
        nextPage(firefox)
    print("信息爬取完成")
