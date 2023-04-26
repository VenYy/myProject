import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "SINAGLOBAL=3770871368101.858.1682216847804; "
              "ULV=1682380720471:7:7:7:9197602508132.838.1682380720467:1682345209570; UOR=,,127.0.0.1:5000; "
              "WBPSESS"
              "=Dt2hbAUaXfkVprjyrAZT_EDdL9F9kle35K3tk9SkyD9aVm5tjbqZG_MBqVkoiM7P8KsxJJzX4DvdoBe9SmouNqpI25Dy_xjkelp45l3r4MRVKiS1YkO1qJNF-dZpSMexfVxNeDM-4LrKl9Sdv1sa9BYLyFhftstN09iDKjG7O6jIsS0aZsFyK3fPcUqdEJ4g-Xzlin4e80bjqPT2HG4MbA==;"
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt;"
              "ALF=1685062169; SSOLoginState=1682470172; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBXEEGNx7OFFRxgBn75p5PNzT3XPLdk_DkGOPUpSNo-TU.; "
              "SUB=_2A25JTAVNDeRhGeFG6FIX-C7LyT-IHXVqOHGFrDV8PUNbmtAbLWLnkW9NecZsSI6on-C8OyJ5Oq8Y8XhIlvYA1xfa; "
              "XSRF-TOKEN=58Z19Yq9SbxBy7e8UTPYwHTr"
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
