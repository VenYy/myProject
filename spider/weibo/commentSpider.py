# 对指定话题的评论进行获取
import csv
import os
import time
from datetime import datetime

from sqlalchemy import text

from spider.weibo.DBManager import DBManager, Comment
from spider.weibo.Spider import Spider
from spider.weibo.hotTopic import filter_emoji

db = DBManager()
os.chdir("/media/venyy/Codes/project/spider/weibo/")

comments_spider = Spider()


def get_base_url(key: str) -> list:
    '''
    :param key: 指定需要获取评论数据的话题名称
    :return: urls 指定话题下的每一个正文链接
    '''
    queryData = db.session.execute(text(
        f"select mid, topic_name from topicDetail where topic_name = '{key}' and comments_count > 5;"
    )).fetchall()
    urls = []
    for i in queryData:
        urls.append((f"https://m.weibo.cn/comments/hotflow?id={i[0]}&mid={i[0]}", i[0]))
    return urls


# 获取微博正文内的每一页的链接
def get_urls(url: list, headers: dict) -> list:
    '''
    :param url: 正文的链接，需要从此获取每一个分页的链接
    :param headers: 请求头。每一个正文的cookie中需要当前页面的ID
    :return: url_list 最终需要获取的数据来源
    '''

    url_list = []
    url_list.append(url)

    comments_spider.url = url
    comments_spider.headers = headers
    try:
        jData = comments_spider.parse_json()
        time.sleep(1)
        if jData["ok"] == 0:
            pass
        else:
            '''
            max_id == '': 表示仅存在一页评论数据,
            max_id == 0 : 当前页面是最后一页
            max_id == ..: 构造链接 
            '''
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
    return url_list


# 获取评论数据
def get_comments(url_list: list) -> list:
    '''
    :param url_list: 最终需要获取的数据来源，来自get_urls()
    :return: comments_data
    '''
    comments_data = []
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
            print("Error when getting comments: ", e)

    return comments_data


# 从csv文件读取评论数据并存入数据库
def saveCommentsToDB(path: str) -> None:
    '''
    :param path: 评论数据csv文件路径
    :return: None
    '''
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        insertCount = 0  # 累计添加数量
        updateCount = 0  # 累计更改数量
        for row in reader:
            '''
            判断是否需要新增或更改数据
            '''
            existing_record = db.session.query(Comment).filter_by(comment_id=row["comment_id"]).first()
            if existing_record is None:
                comments = Comment(
                    comment_id=row["comment_id"],  # 评论ID
                    screen_name=row["screen_name"],  # 发布者昵称
                    profile_url=row["profile_url"],  # 个人主页
                    source=row["source"],  # 发布者所在地
                    created_at=row["created_at"],  # 评论发布时间
                    text_=row["text"],  # 正文
                    like_count=row["like_count"],  # 点赞数
                    mid=row["mid"]  # 对应的文章的ID
                )
                db.add_data(comments)
                db.session.commit()
                insertCount += 1
            else:
                update_required = False
                if existing_record.like_count != row["like_count"]:
                    existing_record.like_count = row["like_count"]
                    update_required = True
                if update_required:
                    print(f"Updating: ", existing_record.comment_id)
                    db.session.commit()
                    updateCount += 1

        print(f"comments表共更新了{updateCount}条数据")
        print(f"comments表共新增了{insertCount}条数据")


if __name__ == '__main__':
    start_time = time.time()

    words = db.session.execute(text(
        "select distinct word from topic order by timeStamp desc limit 50;"
    )).fetchall()
    count = 1
    for word in words:
        key = word[0]
        urls = get_base_url(key)
        print(f"正在获取话题：{key}的评论数据，剩余：{len(words) - count}")
        count += 1
        url_list = []
        for url, mid in urls:
            headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                              "Safari/537.36",
                "cookie": "WEIBOCN_FROM=1110006030; SUB=_2A25JQ1_SDeRhGeBK7VoU8izJwziIHXVqzGGarDV6PUJbkdB"
                          "-LWPCkW1NR5N03I0DfRwuFR-ea9npqpQaYuHL0KA2;"
                          "_T_WM=67285126995; MLOGIN=1; XSRF-TOKEN=56c53c; "
                          "mweibo_short_token=2cd2eef66f;"
                          "M_WEIBOCN_PARAMS=oid={mid}&luicode=20000061&lfid={mid}&uicode=20000061&fid;"
                          "={mid}".format(mid=mid)
            }
            url_list.extend(get_urls(url, headers))
        print(url_list)
        comments_data = get_comments(url_list)

        comments_spider.saveAsCSV("./files/comments.csv",
                                  ["comment_id",
                                   "screen_name",
                                   "profile_url",
                                   "source",
                                   "created_at",
                                   "text",
                                   "like_count",
                                   "mid",
                                   "topic_name"],
                                  comments_data)

        saveCommentsToDB("./files/comments.csv")

        end_time = time.time()
    print("共耗时：", end_time - start_time)
