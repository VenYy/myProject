import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "SINAGLOBAL=3770871368101.858.1682216847804; login_sid_t=1d403f0b5f2fdeb8442afa9caf6d0f5c; "
              "cross_origin_proto=SSL; XSRF-TOKEN=pphAvJNb911kY_L-46bQ_tRE; _s_tentry=passport.weibo.com; "
              "Apache=9197602508132.838.1682380720467; "
              "ULV=1682380720471:7:7:7:9197602508132.838.1682380720467:1682345209570; wb_view_log=1920*10801; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBT6Eeov6OE4Tln9jTIwWDX5Qt76Fu78vgU59g8qZohZ4.; "
              "SUB=_2A25JQ2jEDeRhGeFG6FIX-C7LyT-IHXVqOd0MrDV8PUNbmtANLUigkW9NecZsSCo_Zak-Kx6ADr-1ZgYYDC6pzK9V; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KzhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; ALF=1713916947; SSOLoginState=1682380948; UOR=,,127.0.0.1:5000; "
              "WBPSESS"
              "=Dt2hbAUaXfkVprjyrAZT_EDdL9F9kle35K3tk9SkyD9aVm5tjbqZG_MBqVkoiM7P8KsxJJzX4DvdoBe9SmouNqpI25Dy_xjkelp45l3r4MTyCurt-J9Dx9mnIf6ZY3d2XEF62zRy-x5jG5nlE7BWDAv8nj3WSKIg_--XMTSdoerPqkUAyAWNoGYekDRX3fL3uGYVc0oizZzfSbXmhoKVpQ==; PC_TOKEN=23f28977b2"
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
        resp.encoding = "utf-8"
        if resp.status_code == 200:
            return resp.json()
        else:
            print("Response error when parse json: ", resp.status_code)


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
