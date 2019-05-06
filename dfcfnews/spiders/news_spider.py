#coding:utf-8
"""
爬取东方财富网股吧某一股票的新闻
"""
from scrapy.spiders import Spider
from ..items import DfcfnewsItem
from scrapy.selector import Selector
from scrapy import Request
import re
class YaowenSpider(Spider):
    name = 'dfcf_news'
    start_urls = []
    orignal_url = 'http://guba.eastmoney.com'
    def start_requests(self):
        #获取东方财富网某特定股票的股吧中的新闻
        url_head = 'http://guba.eastmoney.com/list,002415,1,f_%s.html'
        for i in range(1,17):
            complete_url = url_head%(str(i))
            self.start_urls.append(complete_url)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    #解析每个页面，获取该页面上所有新闻的url
    def parse(self, response):
        sel = Selector(response)
        link_list_1 = sel.xpath('//div[@class="articleh"]/span[3]/a/@href').extract()
        # link_list_2 = sel.xpath('//div[@class="articleh odd"]/span[3]/a/@href').extract()
        for link in link_list_1:
            out = self.orignal_url+link
            yield Request(out,callback=self.parse_link)

    #解析每个新闻的链接，获取新闻的标题，内容，摘要等相关信息
    def parse_link(self,response):
        item = DfcfnewsItem()
        sel = Selector(response)
        #获得该新闻对应的股票名称
        stock_name = sel.xpath('//div[@id="stockheader"]/span/span/a/text()').extract_first()
        item['stock_name'] = stock_name[:-1]
        #获得该新闻对应的股票代码
        tmp = response.url.split(',')[1]
        item['stock_id'] = tmp
        #获得新闻标题
        title = sel.xpath('//div[@id="zwconttbt"]/text()').extract_first()
        item['news_title'] = title.strip().replace('\r','').replace('\n','')
        #获得新闻发布的时间
        time = sel.xpath('//div[@id="zwconttb"]/div[2]/text()').extract_first()
        item['news_pubtime'] = self.TransferTime(time)
        #获得新闻的内容
        contents = sel.xpath('//div[@id="zw_body"]/p/text()').extract()
        # contents = sel.xpath('//div[@id="zwconbody"]/div/p/text()').extract()
        content = ''
        for i in contents:
            content += i.strip().replace("\u3000", "").replace(' ','')
        content = content.strip().replace(" ", "")
        item['news_content'] = content
        yield item

    #小工具：对时间进行处理，利用正则匹配获得满足格式要求的时间
    @staticmethod
    def TransferTime(time_str):
        qq = re.compile(r'\d{4}-\d{2}-\d{2}')
        out = re.findall(qq,time_str)
        return out[0]