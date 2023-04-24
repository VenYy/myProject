# 参考：https://zhuanlan.zhihu.com/p/498425181

"""
评论区
如果是第一页，不需要传`max_id`参数
否则，需要传入`max_id`参数，来自上一页的`max_id`
"""

import os
import threading
import time
from datetime import datetime

from sqlalchemy import text

from spider.weibo.DBManager import DBManager
from spider.weibo.hotTopic import filter_emoji

db = DBManager()
os.chdir("/media/venyy/Codes/project/spider/weibo/")

from spider.weibo.Spider import Spider

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "cookie": "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBuW6uZSZOrfYwAUvUlf6XAxaSP4r1Jc9kjbSVN-Vu3yE.; "
              "ALF=1684894099; "
              "SUB=_2A25JQnBrDeRhGeBK7VoU8izJwziIHXVqzRAjrDV6PUJbkdANLWn6kW1NR5N03BRDyLyFauBE1YJztjDbimQFl-ZV; "
              "_T_WM=55088307293; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=439dda; "
              "mweibo_short_token=b6df494d89; "
              "M_WEIBOCN_PARAMS=oid=4894142264513314&luicode=20000061&lfid=4894142264513314"
}
comments_spider = Spider()
comments_spider.headers = headers


def get_urls():
    queryData = db.session.execute(text(
        "select mid, topic_name from topicDetail where comments_count > 50 and timeStamp >= DATE_SUB(NOW(), INTERVAL 300 MINUTE)"
    )).fetchall()
    urls = []
    for i in queryData:
        urls.append((f"https://m.weibo.cn/comments/hotflow?id={i[0]}&mid={i[0]}", i[1]))
    return urls


# 不使用多线程的url_list获取程序
# def solve(url, url_list):
#     url_list.append(url)
#     comments_spider.url = url
#     jData = comments_spider.parse_json()
#     if jData["ok"] == 0:
#         pass
#     else:
#         max_id = jData["data"]["max_id"]
#         if max_id == "":
#             print("JSON return nothing")
#             pass
#         elif max_id == 0:
#             pass
#         else:
#             u = f"{url}&max_id={max_id}"
#             url_list.append(u)


# 使用多线程获取url_list
class UrlThread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        url_list.append(self.url)
        comments_spider.url = self.url
        jData = comments_spider.parse_json()
        if jData["ok"] == 0:
            print("Json return nothing")
            pass
        else:
            max_id = jData["data"]["max_id"]
            if max_id == "":
                pass
            elif max_id == 0:
                pass
            else:
                u = f"{self.url}&max_id={max_id}"
                url_list.append(u)


class CommentsThread(threading.Thread):
    def __init__(self, urls, comments_data):
        super().__init__()
        self.url_list = urls
        self.comments_data = comments_data

    def run(self):
        for url in self.url_list:
            comments_spider.url = url
            print("正在获取：", url)
            jData = comments_spider.parse_json()
            if jData["ok"] == 0:
                print("Json return nothing")
                pass
            else:
                jData = jData["data"]
                for j in jData["data"]:
                    analysis_extra = j["analysis_extra"]
                    mid = analysis_extra.split("|")[1].lstrip("mid:")
                    dic = {
                        "comment_id": j["id"],
                        "screen_name": j["user"]["screen_name"],
                        "profile_url": j["user"]["profile_url"],
                        "source": j["source"].lstrip("来自"),
                        "follow_count": j["user"]["follow_count"],
                        "followers_count": j["user"]["followers_count"],
                        "created_at": datetime.strptime(j["created_at"], '%a %b %d %H:%M:%S %z %Y'),
                        "text": filter_emoji(j["text"]),
                        "mid": mid
                    }
                    self.comments_data.append(dic)


def saveCommentsToDB():
    pass



if __name__ == "__main__":
    start = time.time()

    # urls = get_urls()
    # url_list = []
    # for url, tn in urls:
    #     solve(url, url_list)
    # print(url_list)

    urls = get_urls()
    url_list = []
    url_thread_list = []
    for u, tn in urls:
        url_thread = UrlThread(u)
        url_thread_list.append(url_thread)
        url_thread.start()
    for t in url_thread_list:
        t.join()
    # print(url_list)

    comments_data = []
    comments_thread_list = []
    batch_size = 10
    for i in range(0, len(url_list), batch_size):
    # for url in url_list:
        batch_urls = url_list[i: i+batch_size]
        comments_thread = CommentsThread(batch_urls, comments_data)
        comments_thread_list.append(comments_thread)
        comments_thread.start()
    for t in comments_thread_list:
        t.join()

    comments_spider.saveAsCSV("./files/comments.csv",
                              ["comment_id", "screen_name", "profile_url", "source",
                               "follow_count", "followers_count",
                               "created_at", "text",
                               "mid", "topic_name"],
                              comments_data)

    end = time.time()
    print("耗时：", end - start)
