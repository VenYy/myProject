import os
import time

from sqlalchemy import text

from spider.weibo.DBManager import DBManager, Topic, HotSearch, SearchTrend, TopicDetail
import csv

db = DBManager()
db.create_all()
os.chdir("/media/venyy/Codes/project/spider/weibo/")


def saveHotSearchToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hotSearch = HotSearch(word=row["word"], hot=row["hot"],
                                  href=row["href"], timeStamp=row["timeStamp"])
            db.add_data(hotSearch)
            db.session.commit()
        print("Save hotSearch to database success")


def saveTopicToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            topic = Topic(word=row["word"], summary=row["summary"],
                          read=row["read"], mention=row["mention"],
                          href=row["href"], link=row["link"],
                          timeStamp=row["time_stamp"])
            db.add_data(topic)
            db.session.commit()
        print("Save topic to database success")


def saveTrendToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = [i[0] for i in db.session.execute(text("select word from searchTrend")).fetchall()]
        print(data)
        for row in reader:
            if row["word"] not in data:
                trend = SearchTrend(word=row["word"], href=row["href"], trend=row["trend"], timeStamp=row["timeStamp"])
                db.add_data(trend)
                db.session.commit()

        print("Save search trend to database success")


def saveDetailToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        d = [i[0] for i in db.session.execute(text("select mid from topicDetail")).fetchall()]
        # print(d)
        for row in reader:
            # print(row["mid"])
            if row["mid"] not in d:
                topicDetail = TopicDetail(mid=row["mid"], detail_url=row["detail_url"],
                                          screen_name=row["screen_name"], followers_count=row["followers_count"],
                                          status_province=row["status_province"],
                                          type_=row["type"], topic_name=row["topic_name"],
                                          attitudes_count=row["attitudes_count"], comments_count=row["comments_count"],
                                          reposts_count=row["reposts_count"],
                                          text_=row["text"], timeStamp=row["timeStamp"])
                db.add_data(topicDetail)
                db.session.commit()

        print("Save topic detail to database success")


def run():
    saveHotSearchToDB("./files/hotSearch.csv")
    saveTopicToDB("./files/topic.csv")
    saveTrendToDB("./files/searchTrend.csv")
    saveDetailToDB("./files/topicDetail.csv")
    print("Saving to DB....")



# run()