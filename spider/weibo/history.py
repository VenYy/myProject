"""
补充历史话题的数据
"""
import csv
import json
import os
import re
import threading
import time
from datetime import datetime

from bs4 import BeautifulSoup
from sqlalchemy import text

from spider.weibo.DBManager import TopicDetail, DBManager

from spider.weibo.hotTopic import hotTopicSpider, saveCSV, filter_emoji

os.chdir("/media/venyy/Codes/project/spider/weibo/")

db = DBManager()


data = db.session.execute(text(
    "select word,href from topic group by word;"
)).fetchall()

link = [i[1] for i in data]


class DetailThread(threading.Thread):
    def __init__(self, res):
        super().__init__()
        self.res = res

    def run(self):
        try:
            with open("./files/tmpp.json", "a+", encoding="utf-8") as f:
                for i in link:
                    hotTopicSpider.url = i
                    jsonData = hotTopicSpider.parse_json()

                    try:
                        if len(jsonData["data"]["cards"]) == 0:
                            pass
                        else:
                            # self.jsonList.append(jsonData["data"]["cards"])
                            self.res.append(jsonData["data"]["cards"])
                            # json.dump({"data": jsonData["data"]["cards"]}, f, ensure_ascii=False)
                    except Exception as e:
                        print("Error: ", e)
                        pass
                    print("Writing-----")
        except Exception as e:
            print("Error: ", e)


def runA():
    if os.path.exists("./files/tmpp.json"):
        os.remove("./files/tmpp.json")

    detailThreads = []
    batchSize = 5
    index = 0
    res = []

    for i in range(0, len(data), batchSize):
        thread = DetailThread(res)
        index += 1
        detailThreads.append(thread)
        thread.start()
    for t in detailThreads:
        t.join()
    with open("./files/tmpp.json", "w", encoding="utf-8") as f:
        json.dump({"data": res}, f)


def solve():
    resData = []
    with open("./files/tmpp.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in data["data"]:
            for j in i:
                mblog = j.get("mblog", {})
                mid = mblog.get("mid")
                if not mid:
                    continue

                user = mblog.get("user", {})
                actionlog = j.get("actionlog", {})
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


def saveToCSV(resData):
    with open("./files/testt.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mid", "detail_url",
                                               "screen_name", "uid", "gender", "profile_url",
                                               "followers_count",
                                               "status_province", "type", "topic_name",
                                               "attitudes_count", "comments_count", "reposts_count",
                                               "text", "timeStamp"])

        writer.writeheader()
        writer.writerows(resData)


def saveDetailToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        updateCount = 0
        insertCount = 0
        for row in reader:
            '''
            如果主键不存在，则添加数据，否则修改数据
            '''
            try:
                existing_record = db.session.query(TopicDetail).filter_by(mid=row["mid"]).first()
                if existing_record is None:
                    topicDetail = TopicDetail(mid=row["mid"],
                                              detail_url=row["detail_url"],
                                              screen_name=row["screen_name"],
                                              uid=row["uid"],
                                              gender=row["gender"],
                                              profile_url=row["profile_url"],
                                              followers_count=row["followers_count"],
                                              status_province=row["status_province"],
                                              type_=row["type"],
                                              topic_name=row["topic_name"],
                                              attitudes_count=row["attitudes_count"],
                                              comments_count=row["comments_count"],
                                              reposts_count=row["reposts_count"],
                                              text_=row["text"],
                                              timeStamp=row["timeStamp"])
                    db.add_data(topicDetail)
                    insertCount += 1
                    db.session.commit()
                else:
                    # 只有满足至少一个条件时才会更新数据
                    update_required = False
                    if existing_record.uid != row["uid"]:
                        existing_record.uid = row["uid"]
                        update_required = True
                    if existing_record.gender != row["gender"]:
                        existing_record.gender = row["gender"]
                        update_required = True
                    if existing_record.text != row["text"]:
                        existing_record.text = row["text"]
                        update_required = True

                    if existing_record.attitudes_count != int(row["attitudes_count"]):
                        existing_record.attitudes_count = int(row["attitudes_count"])
                        update_required = True
                    if existing_record.comments_count != int(row["comments_count"]):
                        existing_record.comments_count = int(row["comments_count"])
                        update_required = True
                    if existing_record.reposts_count != int(row["reposts_count"]):
                        existing_record.reposts_count = int(row["reposts_count"])
                        update_required = True

                    if update_required:
                        print(f"Updating: {existing_record.mid} ...")
                        db.session.commit()
                        updateCount += 1
            except Exception as e:
                print("Error when saving topic detail: ", e)
                continue
        print("Save topic detail to database success")
        print(f"topicDetail表共更新了{updateCount}条数据")
        print(f"topicDetail表共新增了{insertCount}条数据")



if __name__ == '__main__':
    startTime = time.time()
    runA()
    resData = solve()
    print(resData)
    saveToCSV(resData)
    saveDetailToDB("./files/testt.csv")

    endTime = time.time()
    print("用时：", endTime - startTime)