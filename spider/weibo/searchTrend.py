import os

from sqlalchemy import text

from spider.weibo.DBManager import DBManager
from spider.weibo.Spider import Spider

spider = Spider()

db = DBManager()


def queryData():
    result = db.session.execute(
        text("select * from searchTrend where word in "
             "(select word from (select word from hotSearch order by timeStamp desc, hot desc limit 5) as hSw);")
    ).fetchall()
    word = []
    href = []
    trend = []
    for i in result:
        word.append(i[0])
        href.append(i[1])
        trend.append(i[2])

    return word, trend


def parseData(word, trend):
    data = []
    for w, t in zip(word, trend):
        try:
            spider.url = t
            trendJson = spider.parse_json()
            # print(trendJson)
            data.append({"word": w,
                         "read": trendJson["data"]["read"],
                         "mention": trendJson["data"]["me"],
                         "ori": trendJson["data"]["ori"]})
        except Exception as e:
            print(e)
            pass
    # print(data)
    return data


def run():
    word, trend = queryData()
    data = parseData(word, trend)
    spider.saveAsJson(f"./files/trend.json", data)


# run()