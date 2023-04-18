import time

from sqlalchemy import text

from spider.weibo.DBManager import DBManager, Topic, HotSearch, SearchTrend
import csv

db = DBManager()
db.create_all()

def saveHotSearchToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hotSearch = HotSearch(word=row["word"], hot=row["hot"],
                                  href=row["href"], timeStamp=row["timeStamp"])
            db.add_data(hotSearch)
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

        print("Save topic to database success")

def saveTrendToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = [i[0] for i in db.session.execute(text("select word from searchTrend")).fetchall()]
        print(data)
        for row in reader:
            if row["word"] not in data:
                trend = SearchTrend(word=row["word"], href=row["href"], trend=row["trend"])
                db.add_data(trend)

        print("Save search trend to database success")
def run():
    saveHotSearchToDB("./files/hotSearch.csv")
    saveTopicToDB("./files/topic.csv")
    saveTrendToDB("./files/searchTrend.csv")
    print("Saving to DB....")



# run()