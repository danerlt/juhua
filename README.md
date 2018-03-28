# juhua
Scrapy爬取京东，淘宝商品数据

## 如何运行
- 1.安装Python3
具体过程请参考[Python官网](https://python.org)
- 2.安装依赖

进入项目目录，执行：
```
pip install -r requirements.txt
```
- 3.配置chromeDriver

将项目目录下的geckodriver目录加入到PATH中
- 4.修改数据库配置
在settings.py中
```
# 数据库的配置，请将下面的换成你自己的数据库配置
DB_HOST = 'localhost'  # 主机名
DB_PORT = 3306  # 端口号
DB_USER = 'root'    # 用户名
DB_PASSWD = '123456'  # 密码
DB_DB = 'juhua'  # 数据库名
```
- 5.爬取数据：
```
scrapy crawl jd
scrapy crawl taobao
scrapy crawl product_info
```
