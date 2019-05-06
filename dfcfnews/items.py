# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DfcfnewsItem(scrapy.Item):
    #新闻标题
    news_title = scrapy.Field()
    #股票代码
    stock_id = scrapy.Field()
    #股票名称
    stock_name = scrapy.Field()
    #新闻发布时间
    news_pubtime = scrapy.Field()
    #新闻内容
    news_content = scrapy.Field()
    #评论内容
    review = scrapy.Field()
    #评论时间
    pub_time = scrapy.Field()