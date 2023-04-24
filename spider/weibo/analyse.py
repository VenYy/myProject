from sqlalchemy import text

from spider.weibo.DBManager import DBManager, Topic, HotSearch, SearchTrend, TopicDetail, Comments
import csv


db = DBManager()
db.create_all()


def saveHotSearchToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        insertCount = 0
        reader = csv.DictReader(f)
        for row in reader:
            hotSearch = HotSearch(word=row["word"], hot=row["hot"],
                                  href=row["href"], timeStamp=row["timeStamp"])
            db.add_data(hotSearch)
            insertCount += 1
            db.session.commit()
        print("Save hotSearch to database success")
        print(f"hotSearch表共新增了：{insertCount}条数据")


def saveTopicToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        insertCount = 0
        reader = csv.DictReader(f)
        for row in reader:
            topic = Topic(word=row["word"], summary=row["summary"],
                          read=row["read"], mention=row["mention"],
                          href=row["href"], link=row["link"],
                          timeStamp=row["time_stamp"])
            db.add_data(topic)
            insertCount += 1
            db.session.commit()
        print("Save topic to database success")
        print(f"topic表共新增了：{insertCount}条数据")


def saveTrendToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        insertCount = 0
        reader = csv.DictReader(f)
        data = [i[0] for i in db.session.execute(text("select word from searchTrend")).fetchall()]
        print(data)
        for row in reader:
            if row["word"] not in data:
                trend = SearchTrend(word=row["word"], href=row["href"], trend=row["trend"], timeStamp=row["timeStamp"])
                db.add_data(trend)
                insertCount += 1
                db.session.commit()

        print("Save search trend to database success")
        print(f"searchTrend表共新增了：{insertCount}条数据")


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


def saveCommentsToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        insertCount = 0
        updateCount = 0
        for row in reader:
            existing_record = db.session.query(Comments).filter_by(comment_id=row["comment_id"]).first()
            if existing_record is None:
                comments = Comments(
                    comment_id=row["comment_id"],
                    screen_name=row["screen_name"],
                    profile_url=row["profile_url"],
                    source=row["source"],
                    follow_count=row["follow_count"],
                    followers_count=row["followers_count"],
                    created_at=row["created_at"],
                    text_=row["text"],
                    mid=row["mid"]
                )
                db.add_data(comments)
                db.session.commit()
                insertCount += 1
            else:
                update_required = False
                if existing_record.comment_id != row["comment_id"]:
                    existing_record.comment_id = row["comment_id"]
                if update_required:
                    print(f"Updating: ", existing_record.comment_id)
                    db.session.commit()
                    updateCount += 1

        print(f"comments表共更新了{updateCount}条数据")
        print(f"comments表共新增了{insertCount}条数据")

def run():
    saveHotSearchToDB("./files/hotSearch.csv")
    saveTopicToDB("./files/topic.csv")
    saveTrendToDB("./files/searchTrend.csv")
    saveDetailToDB("./files/test.csv")
    saveCommentsToDB("./files/comments.csv")


run()