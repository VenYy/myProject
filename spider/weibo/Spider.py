import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; MEIQIA_TRACK_ID=2OJ8IuURwFva0DJ6mozzqnwM3oz; "
              "MEIQIA_VISIT_ID=2OJ8J36Xmd1SKDDAadIZw1L84sQ; UOR=,,127.0.0.1; "
              "ULV=1681372700753:13:13:8:1274772114835.5806.1681372700724:1681288808813; ALF=1683980339; "
              "SSOLoginState=1681388341; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBl9VGHlpxa--x9VGs9QmJKDHC8JnAijO0WC8ZiMI1mto.; "
              "SUB=_2A25JM4NmDeRhGeFG6FIX-C7LyT-IHXVqSPOurDV8PUNbmtAbLXKtkW9NecZsSFdVmnutEvARITZxxrJxx98DcMaK; "
              "XSRF-TOKEN=PDaHr7ub8ezlgu6jg8019xlk; "
              "WBPSESS=qJtA5EKTVAmfo4ozVa9MnqvcR0zz7rHwqy8Cz3zSQ-fuYQI67cm_6vqyKlGjiP94F6hqvKXCIQqCypSb5EqFpq-Wd"
              "-sMC0v9WJHHXuyTh4qPvPP256FD_zOzR3sf3t3YhaSPCS3iGkFlnNoXYgKJNQ== "
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

    @staticmethod
    def saveAsJson(path, jData):
        try:
            with open(path, "w", encoding="utf-8") as f:
                jData = {"data": jData}
                json.dump(jData, f, ensure_ascii=False)
                print("Writing JSON-----")
        except Exception as e:
            print("Error On JSON：", e)
