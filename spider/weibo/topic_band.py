# 话题榜
# https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page=1&count=20


import requests
import csv
import time
import json

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


def parse():
    data = []
    for i in range(1, 7):
        url = f"https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page={i}&count=20"
        resp = requests.get(url, headers=headers)
        resp.encoding = "utf-8"
        content = resp.json()
        for c in content["data"]["statuses"]:
            # print(j["topic"])e
            topic = c["topic"]  # 话题名称
            summary = c["summary"]  # 导语
            read = c["read"]  # 阅读量
            mention = c["mention"]  # 讨论量
            href = f"https://s.weibo.com/weibo?q=%23{topic}%23"
            topic_dic = {"话题名称": topic, "导语": summary, "阅读量": read, "讨论量": mention, "链接": href}
            data.append(topic_dic)
    return data

def save(data, path):
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["话题名称", "导语", "阅读量", "讨论量", "链接"])
            writer.writeheader()
            writer.writerows(data)
            print("writing CSV------")
    except Exception as e:
        print("Error:", e)

def saveAsJson(data, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            jData = {"data": data}
            json.dump(jData, f, ensure_ascii=False)
            print("Writing JSON-----")
    except Exception as e:
        print("Error: ", e)
def run():
    data = parse()
    # path = "./files/topic_band.csv"
    # save(data, path)
    path = "./files/topic_band.json"
    saveAsJson(data, path)


while True:
    run()
    time.sleep(60)