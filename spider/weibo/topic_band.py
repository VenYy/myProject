# 话题榜
# https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page=1&count=20


import requests
import csv
import time
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; ALF=1683600145; SSOLoginState=1681008147; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBwUf6J2kzV-I6DNS3PcQYUML8WqoKXBFFPVyY7sLs0iA.; "
              "SUB=_2A25JNlZEDeRhGeFG6FIX-C7LyT-IHXVqQsCMrDV8PUNbmtAGLUL4kW9NecZsSHFRBaT7YBwOqJfmQBCIr6qIH4hU; "
              "_s_tentry=login.sina.com.cn; Apache=5543990509605.156.1681008151583; "
              "ULV=1681008151592:6:6:1:5543990509605.156.1681008151583:1680932072203; UOR=,,127.0.0.1:5000; "
              "PC_TOKEN=7ab9c640c4 "

}

def parse():
    data = []
    for i in range(1, 11):
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
            # try:
            #     mid = c["mid"]
            #     top_link = f"https://m.weibo.cn/detail/{mid}"
            # except Exception as e:
            #     mid = ""
            #     top_link = f"https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23{topic}%23%26t%3D&title=%E7%83%AD%E9%97%A8-"
            # href = f"https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23{topic}%23%26t%3D&title=%E7%83%AD%E9%97%A8-"
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