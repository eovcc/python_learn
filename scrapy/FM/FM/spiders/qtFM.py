import re
import scrapy
import scrapy.http


class QtfmSpider(scrapy.Spider):
    name = "qtFM"
    allowed_domains = ["qtfm.cn"]
    start_urls = ["https://m.qtfm.cn/rank"]

    def parse(self, response:scrapy.http.Response):
        # print(f"{response.headers=}")
        # print(f"{response.request.headers=}")
        a_list:list[scrapy.Selector] = response.xpath('//div[@class="rank-list"]/a')
        for a in a_list:
            rank = a.xpath('./div[1]/text()').extract_first()
            title = a.xpath('./div[2]/div[1]/text()').extract_first().strip()
            desc = a.xpath('./div[2]/div[2]/text()').extract_first()
            img_url = a.xpath('./img/@src').extract_first()
            hot = a.xpath('./div[2]/div[3]/div[1]/span/text()').extract_first()
            peroids = a.xpath('./div[2]/div[3]/div[2]/span/text()').extract_first()
            # print("------>", rank, title, desc, img_url, hot, peroids)
            a_dict = {
                "type" : "info",
                "rank" : rank,
                "title" : title,
                "desc" : desc,
                "img_url" : img_url,
                "hot" : hot,
                "peroids" : peroids,
            }

            yield a_dict
            yield scrapy.Request(url=img_url, callback=self.parse_img, cb_kwargs={"img_name":title})


    def parse_img(self, response:scrapy.http.Response, img_name:str):
        illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'  # 包含控制字符和系统保留字符
        new_img_name = re.sub(pattern=illegal_chars, repl='', string=img_name)

        yield {
            "type" : "img",
            "img_name" : new_img_name+".jpg",
            "img_bytes" : response.body,
        }
