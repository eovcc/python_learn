from lxml import etree
import requests


def main():
    url = "https://movie.douban.com/top250"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    # 使用lxml解析HTML
    html = etree.HTML(response.text)
    # 使用XPath提取电影信息
    movies = html.xpath('//li//span[@class="title"][1]/text()')
    quote = html.xpath('//li//p[@class="quote"]/span/text()')
    rating_num = html.xpath('//li//span[@class="rating_num"]/text()')
    rating_count = html.xpath('//li//div[@class="bd"]//div//span[last()]/text()')
    print("-" * 60)
    for i, movie in enumerate(movies):
        print(
            f'{i + 1}. {movie.strip()}-"{quote[i].strip()}" {rating_count[i]}-{rating_num[i]}分'
        )
    print("-" * 60)


if __name__ == "__main__":
    main()
