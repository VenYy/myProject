import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; MEIQIA_TRACK_ID=2OJ8IuURwFva0DJ6mozzqnwM3oz; "
              "MEIQIA_VISIT_ID=2OJ8J36Xmd1SKDDAadIZw1L84sQ; ALF=1683880803; SSOLoginState=1681288805; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBuy2jSGnTTJXljgxwKUck1Egtndp8zA9TIBEhOGeSZlI.; "
              "SUB=_2A25JMh42DeRhGeFG6FIX-C7LyT-IHXVqRgj-rDV8PUNbmtAGLWbtkW9NecZsSHRZMGu7VJy8TrZmNsYmHkdoUaUB; "
              "_s_tentry=login.sina.com.cn; UOR=,,127.0.0.1; Apache=9572794205924.457.1681288808771; "
              "ULV=1681288808813:12:12:7:9572794205924.457.1681288808771:1681173414488; PC_TOKEN=5292e45054 "
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
            print("Writing CSV-------")

    @staticmethod
    def saveAsJson(path, jData):
        try:
            with open(path, "w", encoding="utf-8") as f:
                jData = {"data": jData}
                json.dump(jData, f, ensure_ascii=False)
                print("Writing JSON-----")
        except Exception as e:
            print("Error On JSON：", e)