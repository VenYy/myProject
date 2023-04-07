# 热搜榜

import requests
import os
import csv
from datetime import datetime

import schedule as schedule

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; UOR=,,login.sina.com.cn; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; "
              "ULV=1680776206447:3:3:3:6939995810390.054.1680776206404:1680672584157; "
              "XSRF-TOKEN=RQjjhHUnsRsek3sJ8QfXf0UO; ALF=1683437419; SSOLoginState=1680845421; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBgVu-cCTDKRTpCtYGUbJH3aca_0FMADYM1MJgTHlWDho.; "
              "SUB=_2A25JK9o-DeRhGeFG6FIX-C7LyT-IHXVqQUz2rDV8PUNbmtAbLU_jkW9NecZsSCCDZZnxKJ3Alu8T_zz4R2aoobH0; "
              "WBPSESS=qJtA5EKTVAmfo4ozVa9MnqvcR0zz7rHwqy8Cz3zSQ"
              "-fuYQI67cm_6vqyKlGjiP94F6hqvKXCIQqCypSb5EqFptlUUWcLjNXwIeGzPmY2LtzRsKrmARkZlIuBWgDo"
              "-c3EFya9WSX4iMkZOTfXXXnEQw== "

}


def parse_json(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    return resp.json()

def save_csv(path, item_list, item):
    try:
        # if not os.path.exists(path):
        #     # 第一次写入文件，第一行添加表头
        #     with open(path, "w", newline="", encoding="utf-8") as f:
        #         writer = csv.DictWriter(f, fieldnames=item_list)
        #         writer.writeheader()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=item_list)
            writer.writeheader()
            writer = csv.DictWriter(f, fieldnames=item_list)
            writer.writerows(item)  # 按行写入数据
    except Exception as e:
        print("Write Error：", e)

def parse_data(item):
    data = []
    try:

        for i in item["data"]["realtime"]:
            word = i["word"]  # 热搜词条
            # category = i["category"].split(",")  # 类别
            value = i["raw_hot"]  # 热度
            time_stamp = datetime.now().strftime("%Y/%m/%d  %H:%M")     # 时间
            hot_band_dic = {"时间": time_stamp, "词条": word, "热度": value}
            data.append(hot_band_dic)
    except Exception as e:
        print("Error: ", e)
        pass
    return data


def run():
    url = "https://weibo.com/ajax/side/hotSearch"
    path = "./files/hot_band.csv"
    item_list = ["时间", "词条", "热度"]

    json = parse_json(url)
    data = parse_data(json)
    save_csv(path, item_list, data)
    print("Saving--------")


schedule.every(1).minutes.do(run)
count = 1
while True:
    schedule.run_pending()

