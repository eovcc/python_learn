import requests


def main():
    # 使用requests发送请求，获取响应
    # 常用get, post,不常用put,delete,option
    url = "http://gips0.baidu.com/it/u=3602773692,1512483864&fm=3028&app=3028&f=JPEG&fmt=auto?w=960&h=1280"
    response = requests.get(
        url,
    )
    print(f"状态码：\n{response.status_code}")
    # response.encoding = "utf-8"
    # print(f"内容：\n{response.text}")
    # print(f"二进制内容：\n{response.content}")
    with open("images/test.jpg", "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    main()
