# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import os
import codecs
class DfcfnewsPipeline(object):
    def __init__(self):
        #连接mysql数据库的参数配置
        self.dbparam =dict(
            host = 'localhost',
            port = 3306,
            db = 'demo',
            user = 'root',
            passwd = 'root',
            use_unicode = False,
            charset = 'utf8'
        )
        self.conn = pymysql.connect(**self.dbparam)
        self.cor = self.conn.cursor()

    def process_item(self, item, spider):
        #新闻内容以txt形式存储的路径
        path = 'D:/PycharmProjects/dfcfnews/data'
        title = item['news_title']
        # 文件名中不能出现的英文符号有\/:*?"<>|，如果出现，需要将其替换，暂定全部替换为空格
        title = title.replace(' ', '').replace('\\', '') \
            .replace('/', '').replace('*', '').replace('?', '') \
            .replace(':', '').replace('"', '').replace('<', '') \
            .replace('>', '').replace('|', '')
        stock_name = item['stock_name']
        stock_id = item['stock_id']
        time = item['news_pubtime']
        content = item['news_content']
        text_path = path+'/'+stock_name+'/'+str(time)+' '+title+'.txt'
        if not os.path.isfile(text_path):
            sql = (("replace into dfcf_news (news_title,stock_id,stock_name,news_pubtime) values (%s,%s,%s,%s)"))
            params = (title.encode('utf-8'),stock_id.encode('utf-8'),stock_name.encode('utf-8'),time.encode('utf-8'))
            self.cor.execute(sql, params)
            self.conn.commit()
            file = codecs.open(text_path, 'wb', encoding='utf-8')
            file.write(content)
            file.close()
        else:
            print("该条新闻已经抓取！")
        return item

class DfcfreviewPipeline(object):
    def __init__(self):
        # 连接mysql数据库的参数配置
        self.dbparam = dict(
            host='localhost',
            port=3306,
            db='demo',
            user='root',
            passwd='root',
            use_unicode=False,
            charset='utf8'
        )
        self.conn = pymysql.connect(**self.dbparam)
        self.cor = self.conn.cursor()

    def process_item(self, item, spider):
        review = item['review']
        pub_time = item['pub_time']
        stock_id = item['stock_id']
        stock_name = item['stock_name']
        sql = (("replace into dfcf_review (stock_id,stock_name,review,pub_time) values (%s,%s,%s,%s)"))
        params = (
            stock_id.encode('utf-8'), stock_name.encode('utf-8'), review.encode('utf-8'), pub_time.encode('utf-8'))
        self.cor.execute(sql, params)
        self.conn.commit()
        return item

