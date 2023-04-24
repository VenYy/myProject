import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "WBPSESS=qJtA5EKTVAmfo4ozVa9MnqvcR0zz7rHwqy8Cz3zSQ"
              "-fuYQI67cm_6vqyKlGjiP94F6hqvKXCIQqCypSb5EqFpiGbkhoSM75UCnPQrfCi4f8BGEq5LZZV1kN_Oa3jUaiNtVUaaI4rrk21RA1t10SS_A==; SINAGLOBAL=3770871368101.858.1682216847804; UOR=,,login.sina.com.cn; XSRF-TOKEN=I5Gdsi1xs7QEQcWTL_uQJ3mg; PC_TOKEN=1872995fb3; login_sid_t=0b236c36923e8a685e43ad4d17d8da0a; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=1845415765436.7375.1682294218663; ULV=1682294218668:3:3:3:1845415765436.7375.1682294218663:1682230949417; SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrB3tO39Avo7AlrAYSVr6zUNc28YQHZnajNXcRGWoyMCrU.; SUB=_2A25JQbWzDeRhGeFG6FIX-C7LyT-IHXVqNqB7rDV8PUNbmtANLWLmkW9NecZsSDz723rgdZyQvZzs8j6_R8vbPxUd; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KzhUgL.FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; ALF=1713830242; SSOLoginState=1682294243"
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
