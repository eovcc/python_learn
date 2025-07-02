from lxml import etree
from tqdm import tqdm
import pymongo
import requests
import json
import re
import time
import random
import os


def get_full_review(s: requests.Session, review_id: str):
    url = "https://movie.douban.com/j/review/" + review_id + "/full"
    r = s.get(url=url)
    try:
        content: str = ""
        review: str = r.json().get("html")
        review = review.replace("&nbsp;", "")
        review = review.replace("&quot;", "")
        review = review.replace("&amp;#8226;", "")

        html = etree.HTML(review)
        # print(etree.tostring(html, encoding='unicode', pretty_print=True))
        ps = html.xpath("//p | //strong")
        if ps != []:
            for p in ps:
                p_content = p.xpath("./text()")
                if p_content == []:
                    continue
                for temp in p_content:
                    content += temp.strip()
                    content += "\n"
        else:
            content = review.replace("<br>", "\n")

        """ pattern = r"<p>(.*?)</p>"
        contents = re.findall(pattern=pattern, string=review)
        if contents:
            for temp in contents:
                temp = temp.strip()
                if temp.startswith("<strong"):
                    s_cts = re.findall(">(.*?)</strong>", temp)
                    for s_ct in s_cts:
                        if s_ct=="":
                            continue
                        content+=s_ct
                        content+='\n'
                else:
                    if temp=="":
                        continue
                    content+=temp
                    content+='\n'

        pattern = r"<br>(.*?)<br>"
        contents = re.findall(pattern=pattern, string=review)
        if contents:
            for temp in contents:
                temp = temp.strip()
                if temp=="":
                    continue
                content+=temp
                content+='\n' """

        return content
    except Exception as e:
        print(f"错误：{str(e)}")
        return None


def get_review_info(s: requests.Session, movie_id: str, start="0"):
    review_info = []
    param = {"sort": "hostest", "start": start}
    url = "https://movie.douban.com/subject/" + movie_id + "/reviews"
    r = s.get(url=url, params=param)
    try:
        html = etree.HTML(r.content.decode())
        reviews = html.xpath('//div[@class="main review-item"]')
        for review in reviews:
            review_dict = {}
            id = review.xpath("./@id")[0].strip()
            name = review.xpath('.//a[@class="name"]/text()')[0].strip()
            time = review.xpath('.//span[@class="main-meta"]/text()')[0].strip()
            useful_count = review.xpath('.//a[@class="action-btn up"]/span/text()')[
                0
            ].strip()
            useless_count = review.xpath('.//a[@class="action-btn down"]/span/text()')[
                0
            ].strip()
            review_dict["id"] = id
            review_dict["name"] = name
            review_dict["time"] = time
            review_dict["useful_count"] = useful_count
            review_dict["useless_count"] = useless_count
            review_info.append(review_dict)
        return review_info
    except Exception as e:
        print(f"错误：{str(e)}")
        return review_info


def get_top250movie_info(s: requests.Session, start="25"):
    movie_info = []
    param = {
        "start": start,
    }
    url = "https://movie.douban.com/top250"
    r = s.get(url=url, params=param)
    try:
        html = etree.HTML(r.content.decode())
        movies = html.xpath('//div[@class="item"]')
        for movie in movies:
            movie_dict = {}
            id_ref = movie.xpath('.//div[@class="hd"]/a/@href')[0].strip()
            id = re.search(r"\d+", id_ref).group()
            name = movie.xpath('.//span[@class="title"][1]/text()')[0].strip()
            score = movie.xpath('.//div[@class="bd"]/div/span[2]/text()')[0].strip()
            score_count = movie.xpath('.//div[@class="bd"]/div/span[4]/text()')[
                0
            ].strip()
            quote = movie.xpath('.//div[@class="bd"]/p[2]/span/text()')[0].strip()
            movie_dict["id"] = id
            movie_dict["name"] = name
            movie_dict["score"] = score
            movie_dict["score_count"] = score_count
            movie_dict["quote"] = quote
            movie_info.append(movie_dict)
        return movie_info
    except Exception as e:
        print(f"错误：{str(e)}")
        return movie_info


def main():
    url = "mongodb://root:ao8oNpAWyqeXmGCU@120.79.216.106:27017/"
    mg_client = pymongo.MongoClient(url)
    collection = mg_client["inventory"]["top250movies_info"]

    s = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "Cookie": 'll="118282"; bid=M9Gar2bZnKs; ap_v=0,6.0; dbcl2="169089110:7vMqYYHyZek"; ck=HEl9; push_noty_num=0; push_doumail_num=0; frodotk_db="8249c9b1db90e89286dd5d1592b2b9b6"',
    }
    s.headers = headers

    # rv_content = get_full_review(s, "1000369")
    # print(rv_content)
    # rv_info = get_review_info(s, "1292052", start=20)
    # mv_info = get_top250movie_info(s, start="0")

    # 爬取250个电影的信息
    mv_info = []
    for i in tqdm(range(25), desc="获取电影信息", unit="页"):
        start = str(i * 25)
        mv_info.extend(get_top250movie_info(s, start=start))
    print(f"{len(mv_info)=}")

    # time.sleep(random.randint(2, 5)/10)
    # for mv in mv_info:
    #     try:
    #         collection.insert_one(mv)
    #     except Exception as e:
    #         print(str(e))

    # 目标文件夹
    dest_fold = "reviews"
    try:
        os.mkdir(dest_fold)
    except:
        pass

    # 爬取每个电影的评论
    for mv in mv_info:
        mv_id = mv.get("id")
        mv_name = mv.get("name")

        # 爬取每部电影影评信息
        rv_info = []
        start = 0
        while start <= 99:
            temp = get_review_info(s, mv_id, start=start)
            if temp == []:
                break
            rv_info.extend(temp)
            start += 20
            # time.sleep(random.randint(1, 2)/10)

        # 爬取每部电影影评内容
        f = open(f"{dest_fold}/{mv_name}.txt", "w", encoding="utf-8")
        for rv in tqdm(rv_info, desc=f"获取{mv_name}影评内容", unit="条"):
            rv_id = rv.get("id")
            rv_time = rv.get("time")
            rv_name = rv.get("name")
            rv_ufc = rv.get("useful_count")
            rv_ulc = rv.get("useless_count")
            rv_content = get_full_review(s, rv_id)
            head = f"{rv_name} {rv_time} ({rv_ufc}人觉得有用，{rv_ulc}人觉得没用)"
            f.write(head)
            f.write("\n")
            f.write(rv_content)
            f.write("\n" * 2)

            # time.sleep(random.randint(50, 100)/1000)
        f.close()


if __name__ == "__main__":
    main()
