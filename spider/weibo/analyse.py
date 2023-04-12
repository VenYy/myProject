from spider.weibo.DBManager import DBManager, Topic, HotSearch
import csv

db = DBManager()
db.create_all()

def saveHotSearchToSQL(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hotSearch = HotSearch(word=row["word"], hot=row["hot"],
                                  href=row["href"], timeStamp=row["timeStamp"])
            db.add_data(hotSearch)
            print("Insert hotSearch------")
        print("Save to Sql success")

def saveTopicToSQL(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            topic = Topic(word=row["word"], summary=row["summary"],
                          read=row["read"], mention=row["mention"],
                          href=row["href"], timeStamp=row["time_stamp"])
            db.add_data(topic)

            print("Insert topic-------")
        print("Save to Sql success")


def run():
    saveHotSearchToSQL("./files/hotSearch.csv")
    saveTopicToSQL("./files/topic.csv")
    print("Saving to Sql....")


run()