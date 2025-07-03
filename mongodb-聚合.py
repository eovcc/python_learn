import pymongo


def main():
    url = "mongodb://root:ao8oNpAWyqeXmGCU@120.79.216.106:27017/"
    try:
        client = pymongo.MongoClient(url, serverSelectionTimeoutMS=3000)
        # 尝试获取服务器信息
        client.server_info()
        print("MongoDB连接成功！")
    except Exception as e:
        print("MongoDB连接失败：", e)

    collection = client["inventory"]["top250movies_info"]
    print(f"{collection.count_documents({})=}")

    rst = collection.aggregate([
        {"$match": {"score": {"$gt": "9.5"}}},
        {"$group": {"_id": "$score", "count": {"$sum": 1}, "name":{"$push": "$name"}}},
    ])
    for item in rst:
        print(item)


if __name__ == "__main__":
    main()