# 参考：https://zhuanlan.zhihu.com/p/498425181
# 微博移动端


"""
评论区
如果是第一页，不需要传`max_id`参数
否则，需要传入`max_id`参数，来自上一页的`max_id`
"""
import csv
import os
import threading
import time
from datetime import datetime

from sqlalchemy import text

from spider.weibo.DBManager import DBManager, Comment
from spider.weibo.hotTopic import filter_emoji
from spider.weibo.Spider import Spider

db = DBManager()
os.chdir("/media/venyy/Codes/project/spider/weibo/")




comments_spider = Spider()






def get_urls():
    # 每次运行将对最近5个小时的评论数大于50的博文进行评论获取
    queryData = db.session.execute(text(
        "select mid, topic_name from topicDetail where comments_count != 0 "
        "and timeStamp >= DATE_SUB(NOW(), INTERVAL 120 MINUTE);"
    )).fetchall()
    urls = []
    for i in queryData:
        urls.append((f"https://m.weibo.cn/comments/hotflow?id={i[0]}&mid={i[0]}", i[0]))
    return urls



# 不使用多线程的url_list获取程序
def solve(url, url_list, headers):
    url_list.append(url)
    comments_spider.url = url
    comments_spider.headers = headers
    try:
        jData = comments_spider.parse_json()
        time.sleep(1)
        if jData["ok"] == 0:
            pass
        else:
            max_id = jData["data"]["max_id"]
            if max_id == "":
                pass
            elif max_id == 0:
                pass
            else:
                u = f"{url}&max_id={max_id}"
                url_list.append(u)
    except Exception as e:
        print("Error on get urls: ", e)


# 使用单线程获取评论
def get_comments(url_list, comments_data):
    for url in url_list:
        comments_spider.url = url
        print("正在获取：", url)
        time.sleep(2)
        try:
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
                        "created_at": datetime.strptime(j["created_at"], '%a %b %d %H:%M:%S %z %Y'),
                        "text": filter_emoji(j["text"]),
                        "like_count": j["like_count"],
                        "mid": mid
                    }
                    comments_data.append(dic)

        except Exception as e:
            print("Error on get comments: ", e)


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
            try:
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
                            "created_at": datetime.strptime(j["created_at"], '%a %b %d %H:%M:%S %z %Y'),
                            "text": filter_emoji(j["text"]),
                            "like_count": j["like_count"],
                            "mid": mid
                        }
                        self.comments_data.append(dic)
            except Exception as e:
                print(e)
                continue


# 将评论数据存储到数据库中
def saveCommentsToDB(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        insertCount = 0
        updateCount = 0
        for row in reader:
            existing_record = db.session.query(Comment).filter_by(comment_id=row["comment_id"]).first()
            if existing_record is None:
                comments = Comment(
                    comment_id=row["comment_id"],                   # 评论ID
                    screen_name=row["screen_name"],                 # 发布者昵称
                    profile_url=row["profile_url"],                 # 个人主页
                    source=row["source"],                           # 发布者所在地
                    created_at=row["created_at"],                   # 评论发布时间
                    text_=row["text"],                              # 正文
                    like_count=row["like_count"],                   # 点赞数
                    mid=row["mid"]                                  # 对应的文章的ID
                )
                db.add_data(comments)
                db.session.commit()
                insertCount += 1
            else:
                # 对
                update_required = False
                if existing_record.comment_id != row["comment_id"]:
                    existing_record.comment_id = row["comment_id"]
                    update_required = True
                if existing_record.like_count != row["like_count"]:
                    existing_record.like_count = row["like_count"]
                    update_required = True
                if update_required:
                    print(f"Updating: ", existing_record.comment_id)
                    db.session.commit()
                    updateCount += 1

        print(f"comments表共更新了{updateCount}条数据")
        print(f"comments表共新增了{insertCount}条数据")



def run():
    start = time.time()

    '''
    使用单线程获取评论的分页链接
    '''
    urls = get_urls()
    url_list = []
    for url, tn in urls:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                          "Safari/537.36",
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
            #           "application/signed-exchange;v=b3;q=0.7",
            # "accept-encoding": "gzip, deflate, br",
            # "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "WEIBOCN_FROM=1110006030; SUB=_2A25JQ1_SDeRhGeBK7VoU8izJwziIHXVqzGGarDV6PUJbkdB"
                      "-LWPCkW1NR5N03I0DfRwuFR-ea9npqpQaYuHL0KA2;"
                      "_T_WM=67285126995; MLOGIN=1; XSRF-TOKEN=02aa48; "
                      "mweibo_short_token=34c351c4cf;"
                      "M_WEIBOCN_PARAMS=oid={mid}&luicode=20000061&lfid={mid}&uicode=20000061&fid;"
                      "={mid}".format(mid=tn)
        }
        solve(url, url_list, headers)

    '''
    使用单线程获取评论
    '''

    comments_data = []
    if len(url_list) > 0:
        get_comments(url_list, comments_data)
        comments_spider.saveAsCSV("./files/comments.csv",
                                  ["comment_id", "screen_name", "profile_url", "source",
                                   "created_at", "text",
                                   "like_count",
                                   "mid", "topic_name"],
                                  comments_data)

    else:
        print("近半小时暂无数据")



    '''
    使用多线程获取评论的分页链接
    '''
    # urls = get_urls()
    # url_list = []
    # url_thread_list = []
    # for u, tn in urls:
    #     url_thread = UrlThread(u)
    #     url_thread_list.append(url_thread)
    #     url_thread.start()
    # for t in url_thread_list:
    #     time.sleep(5)
    #     t.join()



    ''' 
    使用多线程获取每个分页链接内的评论。batch_size是对链接总数(url_list)进行分割，分割大小为batch_size块，
    因此线程数量为：url_list//batch_size
    '''
    # if len(url_list) > 0:
    #     comments_data = []
    #     comments_thread_list = []
    #     if len(url_list) > 4:
    #         batch_size = len(url_list)//2
    #     else:
    #         batch_size = 1
    #     for i in range(0, len(url_list), batch_size):
    #     # for url in url_list:
    #         batch_urls = url_list[i: i+batch_size]
    #         comments_thread = CommentsThread(batch_urls, comments_data)
    #         comments_thread_list.append(comments_thread)
    #         comments_thread.start()
    #     for t in comments_thread_list:
    #         t.join()
    #
    #     print(comments_data)
    #
    #     '''
    #     将获取到的评论数据存储到csv文件中，以便于存入数据库
    #     '''
    #     comments_spider.saveAsCSV("./files/comments.csv",
    #                               ["comment_id", "screen_name", "profile_url", "source",
    #                                "created_at", "text",
    #                                "like_count",
    #                                "mid", "topic_name"],
    #                               comments_data)
    #
    # else:
    #     print("近半小时尚无评论")
    saveCommentsToDB("./files/comments.csv")

    end = time.time()
    print("耗时：", end - start)

run()