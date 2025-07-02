import requests


def main():
    url = "https://webapi.qtfm.cn/api/mobile/rank/hotSaleWeekly"
    headers = {
        # "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/138.0.0.0"
    }
    s = requests.Session()
    r = s.get(url=url, headers=headers)
    print("-" * 60)
    for item in r.request.headers.items():
        print(f"{item[0]}:{item[1]}")
    print("-" * 60)
    for item in r.headers.items():
        print(f"{item[0]}:{item[1]}")
    print("-" * 60)
    rankinglist = r.json().get("rankinglist")
    for i, book in enumerate(rankinglist):
        title = book.get("title")
        desc = book.get("desc")
        play_count = book.get("playCount")
        print(f"{i+1}.{title}:{desc}-{play_count}")
    print("-" * 60)


if __name__ == "__main__":
    main()
