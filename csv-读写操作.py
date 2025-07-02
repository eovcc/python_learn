import csv

header = ["name", "age", "gender"]
data = [
    ["小王", "18", "男"],
    ["小李", "21", "男"],
    ["小美", "20", "女"],
    ["小c", "26", "无"],
]

dict_data = [
    {
        "name": "小王",
        "age": "18",
        "gender": "男",
    },
    {
        "name": "小李",
        "age": "21",
        "gender": "男",
    },
    {
        "name": "小美",
        "age": "20",
        "gender": "女",
    },
    {
        "name": "小c",
        "age": "26",
        "gender": "无",
    },
]


def main():
    with open("csv_writer.csv", "w", encoding="utf-8", newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        # f_csv.writeheader()
        f_csv.writerows(data)

    with open("csv_writer.csv", "r", encoding="utf-8") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            print(type(row), row)

    with open("csv_dictwriter.csv", "w", encoding="utf-8", newline="") as f:
        f_csv = csv.DictWriter(f, header)
        f_csv.writeheader()
        f_csv.writerows(dict_data)

    with open("csv_dictwriter.csv", "r", encoding="utf-8") as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            print(type(row), row)


if __name__ == "__main__":
    main()
