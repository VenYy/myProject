import csv
import json

import requests
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; UOR=,,127.0.0.1:5000; "
              "ULV=1681173414488:11:11:6:640614947259.3503.1681173414436:1681132194532; ALF=1683858563; "
              "SSOLoginState=1681266565; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBTbmbzAcaSY-_1YjvJgwKMmDdRlCMYiuvVsQ3SAIB1cE.; "
              "SUB=_2A25JMmfVDeRhGeFG6FIX-C7LyT-IHXVqRt4drDV8PUNbmtAGLWPNkW9NecZsSAfyLSKX4f_thng9IsFwzAjj1LKu; "
              "XSRF-TOKEN=wjtM_rsW_1hroKGmP42sj4Tn; "
              "WBPSESS=qJtA5EKTVAmfo4ozVa9MnqvcR0zz7rHwqy8Cz3zSQ"
              "-fuYQI67cm_6vqyKlGjiP94F6hqvKXCIQqCypSb5EqFpsJWAH3os0oJVAUrYIUuhcKwrXZOoVF9yYSfQHzzIvsewP"
              "-RBAlkG9XnEpWkwHUPOA== "
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