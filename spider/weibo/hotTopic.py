import time
from datetime import datetime

from spider.weibo.Spider import *
import os
import re

hotTopicSpider = Spider()


def filter_emoji(desstr, restr=""):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def parse():
    data = []
    for i in range(1, 11):
        hotTopicSpider.url = f"https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page={i}&count=20"
        content = hotTopicSpider.parse_json()
        for c in content["data"]["statuses"]:
            # print(j["topic"])
            topic = filter_emoji(c["topic"].replace("\n", ""))  # 话题名称
            summary = filter_emoji(c["summary"].replace("\n", ""))  # 导语
            read = c["read"]  # 阅读量
            mention = c["mention"]  # 讨论量
            timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M")  # 时间
            # href = f"https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D{topic}%26t%3D0&title=热门-"
            href = f"https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D60%26q%3D%23{topic}%23%26t%3D10&title=%E7%83%AD%E9%97%A8-%23{topic}%23"
            link = f"https://s.weibo.com/weibo?q=%23{topic}%23"
            topic_dic = {"word": topic, "summary": summary, "read": read, "mention": mention, "href": href,
                         "link": link, "time_stamp": timeStamp}

            data.append(topic_dic)
    return data


def saveCSV(data):
    os.chdir("/media/venyy/Codes/project/spider/weibo")
    current_dir = os.getcwd()
    # print(current_dir)
    item_list = ["word", "summary", "read", "mention", "href", "link", "time_stamp"]
    # print(data)
    hotTopicSpider.saveAsCSV(path=f"{current_dir}/files/topic.csv", data=data, item_list=item_list)


# saveCSV()


def saveDetail(data):
    jsonList = []
    for i in data:
        url = i["href"]
        # print(url)
        hotTopicSpider.url = url
        jsonData = hotTopicSpider.parse_json()
        # print(json["data"])
        print("loading-----")
        try:
            # print(jsonData["data"]["cards"])
            if len(jsonData["data"]["cards"]) == 0:
                pass
            else:
                jsonList.append(jsonData["data"]["cards"])
        except Exception as e:
            print("Error: ", e)
            pass
    try:
        with open("./files/tmp.json", "w", encoding="utf-8") as f:
            jData = {"data": jsonList}
            json.dump(jData, f, ensure_ascii=False)
            print("Writing-----")
    except Exception as e:
        print("Error: ", e)


def run():
    os.chdir("/media/venyy/Codes/project/spider/weibo/")
    data = parse()
    saveCSV(data)
    print("Saving hotTopic....")

    saveDetail(data)

# run()
