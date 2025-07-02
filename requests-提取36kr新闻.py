import re
import requests


def main():
    url = "https://m.36kr.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/138.0.0.0"
    }
    r = requests.get(url=url, headers=headers)
    """ print(r.status_code)
    print(r.headers.get("content-type")) """
    content = r.content.decode()
    # print(content)

    # 匹配出需要的结果
    pattern = r'<a.*?href="([^"]*)".*?title weight-bold[^>]*>([^<]*)</'  # 一定要使用非贪婪模式
    ret = re.compile(pattern=pattern)
    news_list = ret.findall(content)
    # print(news_list)
    print("-" * 60)
    for i, news in enumerate(news_list):
        print(f"{i+1}:{url+news[0]} {news[1]}")
    print("-" * 60)


if __name__ == "__main__":
    main()
