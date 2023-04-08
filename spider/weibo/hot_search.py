from datetime import datetime
import time
import requests
import csv
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; ALF=1683437419; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBgVu-cCTDKRTpCtYGUbJH3aca_0FMADYM1MJgTHlWDho.; UOR=,,"
              "www.bing.com; SUB=_2AkMTbHPRf8NxqwJRmPoVy2_gbIpzzwrEieKlMIIKJRMxHRl-yT9yqhcmtRB6OOxdPhlNmGj78230"
              "-azbL0uU3TfPFp1b; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF92zvB9WyMneS6-U5rRhaA; "
              "_s_tentry=passport.weibo.com; Apache=9091549699167.816.1680932072142; "
              "ULV=1680932072203:5:5:5:9091549699167.816.1680932072142:1680855673285; "
              "XSRF-TOKEN=PPLfGDcO_u661st7kIEVxAdy; "
              "WBPSESS=Jx_XaCleItbWmjWmltuZpE7HivfzRcmscsoJKyXTLM4iIrvSNJjjV4d541tlydr6ZRCy9pO"
              "-TGsyuBvoNKsdaikM02ziDbqjhCwiqI5zP4_xElHgrNUpZPx6uez93WNkRxMNfzLEBnY49JJfNaRTJu3DfuGSAcfQT-0LYwdIQdk= "

}

def parse(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    # print(resp.text)
    html = etree.HTML(resp.text)
    return html

def parse_data(html):
    words = html.xpath("//tbody/tr/td/a/text()")[1:]            # 词条
    # print(len(words), words)
    hot = html.xpath("//tbody/tr/td/span/text()")               # 热度
    hots = []
    for _ in hot:
        hot = _.split(" ")[1]
        hots.append(hot)
    # print(len(hots), hots)

    time_stamp = datetime.now().strftime("%Y/%m/%d  %H:%M")     # 时间

    result = []

    if len(words) == len(hots):
        for word, hot in zip(words, hots):
            # print(word, hot)
            if len(hot) == 0:
                # print(word, hot)
                pass
            else:
                result.append({"时间": time_stamp, "词条": word, "热度": hot})
        return result
    else:
        return None

def save(path, item_list, data):
    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=item_list)
        writer.writeheader()
        writer.writerows(data)  # 按行写入数据
def run():
    url = "https://s.weibo.com/top/summary/"
    html = parse(url)
    data = parse_data(html)
    print(data)
    path = "./files/hot_band_bak.csv"
    item_list = ["时间", "词条", "热度"]
    save(path, item_list, data)


if __name__ == '__main__':
    count = 1
    while True:
        run()
        print(f"Saving{count}-----")
        count += 1
        time.sleep(60)