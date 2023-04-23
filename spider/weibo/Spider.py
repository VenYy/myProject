import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "WBPSESS=qJtA5EKTVAmfo4ozVa9MnqvcR0zz7rHwqy8Cz3zSQ"
              "-fuYQI67cm_6vqyKlGjiP94F6hqvKXCIQqCypSb5EqFpiGbkhoSM75UCnPQrfCi4f8BGEq5LZZV1kN_Oa3jUaiNtVUaaI4rrk21RA1t10SS_A==; SINAGLOBAL=3770871368101.858.1682216847804; XSRF-TOKEN=UhsPTgStNconz1wyieI0dJ92; login_sid_t=5f701c2ec0556b7dbd3821bc91541879; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; UOR=,,login.sina.com.cn; Apache=2901535690986.8096.1682230949411; ULV=1682230949417:2:2:2:2901535690986.8096.1682230949411:1682216847809; SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBIrQi52jNGdBmsHV45q--YhNeBwjFryr3T3FWcRjmreA.; SUB=_2A25JQL6RDeRhGeFG6FIX-C7LyT-IHXVqN5dZrDV8PUNbmtAbLRX1kW9NecZsSHHLy2E0lI3EW-HjtiEsNoxEyQR0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KzhUgL.FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; ALF=1713766976; SSOLoginState=1682230978"
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
        # print(resp.status_code)
        try:
            resp.encoding = "utf-8"
            return resp.json()
        except Exception as e:
            print("Error: ", e)
            print(resp.status_code)
            pass

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
