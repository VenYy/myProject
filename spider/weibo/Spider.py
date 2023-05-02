import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "cookie": "SINAGLOBAL=3770871368101.858.1682216847804; UOR=,,127.0.0.1:5000; "
              "ULV=1682508426340:9:9:9:4310444262528.1367.1682508426316:1682501947758; "
              "XSRF-TOKEN=PHp4PtfXABBE6oq64Q7ZZZrf; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBa5VX6omvLsMQAmtbU-ST9WEPKRlnqjPd-4eAtckvU4M.; "
              "SUB=_2A25JVAN8DeRhGeFG6FIX-C7LyT-IHXVqIHO0rDV8PUNbmtANLXfmkW9NecZsSEE-i088RT8C6AcigcO3MFFpeplN; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KzhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; ALF=1714529964; SSOLoginState=1682993964; "
              "WBPSESS=Dt2hbAUaXfkVprjyrAZT_EDdL9F9kle35K3tk9SkyD9aVm5tjbqZG_MBqVkoiM7P8KsxJJzX4DvdoBe9SmouNqpI25Dy_xjkelp45l3r4MRVKiS1YkO1qJNF-dZpSMexXx5KtJYDfAb-ke4dCnbbSUbXnBxXay8beCCaAxZBSd3YEpaTIP8zVFSmjceznB9neAC2kJMdVreQnwz3PGChaQ=="
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
