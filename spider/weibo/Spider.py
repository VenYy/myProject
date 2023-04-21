import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; MEIQIA_TRACK_ID=2OJ8IuURwFva0DJ6mozzqnwM3oz; "
              "MEIQIA_VISIT_ID=2OJ8J36Xmd1SKDDAadIZw1L84sQ; "
              "WBPSESS=qJtA5EKTVAmfo4ozVa9MnqvcR0zz7rHwqy8Cz3zSQ"
              "-fuYQI67cm_6vqyKlGjiP94F6hqvKXCIQqCypSb5EqFpoBS7OrSdPb1NrmF705Ry8RFhseTEqOVgty"
              "-L4hXUDxvnJKdfbc6t7MVbMXB_-COdw==; XSRF-TOKEN=lVVBLoHmzzJpb5XgB15Di3mF; "
              "login_sid_t=c4af16d2ec774da16767ce37a4146782; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; "
              "UOR=,,login.sina.com.cn; SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBuEnrWCd-qFNssR5HD6xGnC3I"
              "-QOAQNBMf6Ob2JWp3HU.; "
              "SUB=_2A25JRaSbDeRhGeFG6FIX-C7LyT-IHXVqMpFTrDV8PUNbmtAGLXHxkW9NecZsSCeGoW6W5CcRmX2aDL0W4Dd7uYl1; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KzhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; ALF=1713571914; SSOLoginState=1682035916; "
              "Apache=459184537911.95636.1682037912071; "
              "ULV=1682037912112:19:19:4:459184537911.95636.1682037912071:1681991557950; PC_TOKEN=2f6600d5c3"
}


class Spider:
    def __init__(self):
        self.url = None

    def parse(self):
        resp = requests.get(self.url, headers=headers)
        resp.encoding = "utf-8"
        # print(resp.text)
        html = etree.HTML(resp.text)
        return html

    def parse_json(self):
        resp = requests.get(self.url, headers=headers)
        resp.encoding = "utf-8"
        return resp.json()

    @staticmethod
    def saveAsCSV(path, item_list, data):

        with open(path, "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=item_list)
            writer.writeheader()
            writer.writerows(data)  # 按行写入数据
            print("Writing CSV--------")

    @staticmethod
    def saveAsJson(path, jData):
        try:
            with open(path, "w", encoding="utf-8") as f:
                jData = {"data": jData}
                json.dump(jData, f, ensure_ascii=False)
                print("Writing JSON-----")
        except Exception as e:
            print("Error On JSON：", e)
