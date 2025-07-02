import pymongo


def main():
    url = "mongodb://root:ao8oNpAWyqeXmGCU@120.79.216.106:27017/"
    client = pymongo.MongoClient(url)
    test_collection = client["test"]["test_collection"]

    info = [{"_id": i, "name": f"py{i}"} for i in range(1000)]

    try:
        rst = test_collection.insert_many(info)
    except:
        pass

    rst = test_collection.find({"$where": "this._id > 0 && this._id%100 == 0"})


if __name__ == "__main__":
    main()
