import csv
import json
import os
import re
from datetime import datetime


def solve():

    with open("./files/tmp.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        # print(len(data["data"]))
        resData = []
        for i in data["data"]:
            for j in i:
                try:
                    attitudes_count = j["mblog"]["attitudes_count"]         # 点赞数
                    comments_count = j["mblog"]["comments_count"]           # 评论数
                    reposts_count = j["mblog"]["reposts_count"]             # 转发数
                    try:
                        status_province = j["mblog"]["status_province"]     # 所在城市
                    except Exception as e:
                        print(e)
                        status_province = "未知"

                    mid = j["mblog"]["mid"]                                         # 唯一ID
                    detail_url = f"https://m.weibo.cn/detail/{mid}"
                    screen_name = j["mblog"]["user"]["screen_name"]                 # 博主昵称
                    uid = j["mblog"]["user"]["id"]                                  # 博主ID
                    profile_url = j["mblog"]["user"]["profile_url"]                 # 博主主页
                    followers_count = j["mblog"]["user"]["followers_count"]         # 粉丝数

                    topic_name = j["actionlog"]["ext"]                              # 话题名称
                    topic_name = "".join(re.findall("[\u4e00-\u9fa5]", topic_name))
                    type = j["mblog"]["page_info"]["type"]                          # 类型

                    text = j["mblog"]["text"]                               # 内容
                    # 匹配所有中文字符和符号
                    res = re.findall(
                        "[\uff01\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]", text)
                    result = ''.join(res).rstrip("全文").lstrip(topic_name).rstrip("网页链接")                             # 正文

                    time = datetime.strptime(j["mblog"]["created_at"], "%a %b %d %H:%M:%S %z %Y")
                    timeStamp = time.strftime("%Y-%m-%d %H:%M:%S")                  # 发布时间

                    resData.append({"mid": mid,                                     # 唯一ID
                                    "detail_url": detail_url,                       # 博文链接
                                    "screen_name": screen_name,                     # 博主昵称
                                    "uid": uid,                                     # 博主ID
                                    "profile_url": profile_url,                     # 博主主页
                                    "followers_count": followers_count,             # 粉丝数
                                    "status_province": status_province,             # 所在地区
                                    "type": type,                                   # 博文类型
                                    "topic_name": topic_name,                       # 话题名称
                                    "attitudes_count": attitudes_count,             # 点赞数
                                    "comments_count": comments_count,               # 评论数
                                    "reposts_count": reposts_count,                 # 转发数
                                    "text": result,                                 # 正文
                                    "timeStamp": timeStamp                          # 时间
                                    })
                except Exception as e:
                    print(e)

        return resData
# print(resData)


def saveToCSV(resData):
    with open("./files/topicDetail.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mid", "detail_url",
                                               "screen_name", "uid", "profile_url",
                                               "followers_count",
                                               "status_province", "type", "topic_name",
                                               "attitudes_count", "comments_count", "reposts_count",
                                               "text", "timeStamp"])

        writer.writeheader()
        writer.writerows(resData)


def run():
    os.chdir("/media/venyy/Codes/project/spider/weibo/")
    resData = solve()
    saveToCSV(resData)

# run()