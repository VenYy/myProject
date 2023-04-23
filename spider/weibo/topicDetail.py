import csv
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

from spider.weibo.hotTopic import filter_emoji


def solve():
    with open("./files/tmp.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        resData = []
        for i in data["data"]:
            for j in i:
                mblog = j.get("card_group", [{}])[0].get("mblog", {})

                mid = mblog.get("mid")
                if not mid:
                    continue

                user = mblog.get("user", {})
                actionlog = j.get("card_group", [{}])[0].get("actionlog", {})
                detail_url = f"https://m.weibo.cn/detail/{mblog.get('mid')}"
                status_province = mblog.get("status_province", "未知")
                gender = {"f": "女", "m": "男"}.get(user.get("gender"), "未知")
                topic_name = "".join(re.findall(r"#(.*?)#", actionlog.get("ext", "")))

                text = mblog.get("text", "")
                text = filter_emoji(BeautifulSoup(text, "html.parser").get_text().rstrip("网页链接"))

                if mblog.get("created_at"):
                    timeStamp = datetime.strptime(mblog["created_at"], "%a %b %d %H:%M:%S %z %Y").strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                resData.append({
                    "mid": mid,
                    "detail_url": detail_url,
                    "screen_name": user.get("screen_name"),
                    "uid": user.get("id"),
                    "gender": gender,
                    "profile_url": user.get("profile_url"),
                    "followers_count": user.get("followers_count"),
                    "status_province": status_province,
                    "type": mblog.get("page_info", {}).get("type"),
                    "topic_name": topic_name,
                    "attitudes_count": mblog.get("attitudes_count"),
                    "comments_count": mblog.get("comments_count"),
                    "reposts_count": mblog.get("reposts_count"),
                    "text": text,
                    "timeStamp": timeStamp
                })

        return resData

# print(resData)


def saveToCSV(resData):
    with open("./files/test.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mid", "detail_url",
                                               "screen_name", "uid", "gender", "profile_url",
                                               "followers_count",
                                               "status_province", "type", "topic_name",
                                               "attitudes_count", "comments_count", "reposts_count",
                                               "text", "timeStamp"])

        writer.writeheader()
        writer.writerows(resData)


def run():
    resData = solve()
    saveToCSV(resData)


# run()
