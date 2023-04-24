import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "WEIBOCN_FROM=1110006030; loginScene=102003; "
              "M_WEIBOCN_PARAMS=oid=4893995174724830&luicode=20000061&lfid=4893995174724830; "
              "SUB=_2A25JQgQEDeRhGeBK7VoU8izJwziIHXVqzKxMrDV6PUJbkdANLWrakW1NR5N03BgZBQ_QBded0qd0LmXFaxaajtyJ; "
              "_T_WM=74187438527; XSRF-TOKEN=3a7ff8; mweibo_short_token=620df02cf8; MLOGIN=1"
}


class Spider:
    def __init__(self):
        self.url = None
        self.headers = headers

    def parse(self):
        resp = requests.get(self.url, headers=self.headers)

        resp.encoding = "utf-8"
        html = etree.HTML(resp.text)
        return html

    def parse_json(self):
        resp = requests.get(self.url, headers=self.headers)
        # print(resp.status_code)
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
