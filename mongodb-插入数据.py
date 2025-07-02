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

    query = {"$where": "this._id > 0 && this._id % 100 == 0"}
    #count_documents不能用$where
    """ count = test_collection.count_documents(query)
    print(f"{count=}") """
    rst = test_collection.find(query)
    for item in rst:
        print(item)


if __name__ == "__main__":
    main()
