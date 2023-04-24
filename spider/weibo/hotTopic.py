import json
import threading
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


def parse_():
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
            href = f"https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D1%26q%3D%23{topic}%23%26t%3D10&title=%E7%83%AD%E9%97%A8-%23{topic}%23"
            link = f"https://s.weibo.com/weibo?q=%23{topic}%23"
            topic_dic = {"word": topic, "summary": summary, "read": read, "mention": mention, "href": href,
                         "link": link, "time_stamp": timeStamp}

            data.append(topic_dic)
    return data



class TopicThread(threading.Thread):
    def __init__(self, url):
        # 重构run函数
        super(TopicThread, self).__init__()
        self.url = url
        self.result = []

    def run(self):
        self.result = parse(craw(self.url))


def craw(u):
    res = hotTopicSpider.parse_json()
    return res


def parse(res):
    data = []
    for c in res["data"]["statuses"]:
        # print(j["topic"])
        topic = filter_emoji(c["topic"].replace("\n", ""))  # 话题名称
        summary = filter_emoji(c["summary"].replace("\n", ""))  # 导语
        read = c["read"]  # 阅读量
        mention = c["mention"]  # 讨论量
        timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M")  # 时间
        # href = f"https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D{topic}%26t%3D0&title=热门-"
        href = f"https://m.weibo.cn/api/container/getIndex?containerid=231522type%3D1%26q%3D%23{topic}%23%26t%3D10&title=%E7%83%AD%E9%97%A8-%23{topic}%23"
        link = f"https://s.weibo.com/weibo?q=%23{topic}%23"
        topic_dic = {"word": topic, "summary": summary, "read": read, "mention": mention, "href": href,
                     "link": link, "time_stamp": timeStamp}

        data.append(topic_dic)
    return data


class DetailThread(threading.Thread):
    def __init__(self, data, res):
        super().__init__()
        self.data = data
        self.res = res

    def run(self):
        try:
            with open("./files/tmp.json", "a+", encoding="utf-8") as f:
                for i in self.data:
                    url = i["href"]
                    hotTopicSpider.url = url
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


def merge_json_files(filenames, output_filename):
    result = []
    for filename in filenames:
        with open(filename) as f:
            data = json.load(f)
            result.extend(data)
        os.remove(filename)
    with open(output_filename, 'w') as f:
        json.dump(result, f)


def saveCSV(data):
    # print(current_dir)
    item_list = ["word", "summary", "read", "mention", "href", "link", "time_stamp"]
    # print(data)
    hotTopicSpider.saveAsCSV(path=f"./files/topic.csv", data=data, item_list=item_list)


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
    urls = [f"https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page={i}&count=20" for i in
            range(1, 11)]
    data = []
    topicThreads = []
    for url in urls:
        hotTopicSpider.url = url
        t = TopicThread(url)
        topicThreads.append(t)
        t.start()
    for t in topicThreads:
        t.join()
        data.extend(t.result)

    if os.path.exists("./files/tmp.json"):
        os.remove("./files/tmp.json")

    detailThreads = []
    batchSize = 5
    index = 0
    res = []

    for i in range(0, len(data), batchSize):
        batchData = data[i:i+batchSize]
        thread = DetailThread(batchData, res)
        index += 1
        detailThreads.append(thread)
        thread.start()
    for t in detailThreads:
        t.join()
    with open("./files/tmp.json", "w", encoding="utf-8") as f:
        json.dump({"data": res}, f)
    saveCSV(data)


    # saveCSV(data)
    # print("Saving hotTopic....")

    # saveDetail(data)

# run()
