# 话题榜
# https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page=1&count=20


import requests
import os
import csv

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 "
}

path = "./files/topic_band.csv"

data = []

for i in range(1, 6):
    url = f"https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page={i}&count=20"
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    content = resp.json()
    # print(content)
    for j in content["data"]["statuses"]:
        # print(j["topic"])e
        topic = j["topic"]          # 话题名称
        read = j["read"]            # 阅读量
        mention = j["mention"]      # 讨论量
        href = f"https://s.weibo.com/weibo?q=%23{topic}%23"
        topic_dic = {"话题名称": topic, "阅读量": read, "讨论量": mention, "链接": href}
        data.append(topic_dic)
        # print(topic_dic)
        try:
            if not os.path.exists("path"):
                # 第一次写入文件，第一行添加表头
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["话题名称", "阅读量", "讨论量", "链接"])
                    writer.writeheader()
            with open(path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["话题名称", "阅读量", "讨论量", "链接"])
                writer.writerows(data)       # 按行写入数据
        except Exception as e:
            print("Write Error：", e)


# https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4886508405005063&is_show_bulletin=2&is_mix=0&count=10&uid=5257157053&fetch_level=0
# https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=4886508405005063&is_show_bulletin=2&is_mix=0&max_id=141890512748400&count=20&uid=5257157053&fetch_level=0
# https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=4886508405005063&is_show_bulletin=2&is_mix=0&max_id=139416612391643&count=20&uid=5257157053&fetch_level=0
# https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=4886508405005063&is_show_bulletin=2&is_mix=0&max_id=138866843135593&count=20&uid=5257157053&fetch_level=0
# https://weibo.com/ajax/statuses/buildComments?flow=0&is_reload=1&id=4886508405005063&is_show_bulletin=2&is_mix=0&max_id=138591980357514&count=20&uid=5257157053&fetch_level=0