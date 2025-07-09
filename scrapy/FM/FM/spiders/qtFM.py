import scrapy


class QtfmSpider(scrapy.Spider):
    name = "qtFM"
    allowed_domains = ["qtfm.cn"]
    start_urls = ["https://m.qtfm.cn/rank"]

    def parse(self, response):
        a_list = response.xpath('//div[@class="rank-list"]/a')
        for a in a_list:
            rank = a.xpath('./div[1]/text()')
            print("------>", rank)
