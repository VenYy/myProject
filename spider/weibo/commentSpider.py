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
def get_comments(url_list: list, key: str) -> list:
    '''
    :param key: 话题名称
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
                        "gender": {"f": "女", "m": "男"}.get(j["user"]["gender"], "未知"),
                        "source": j["source"].lstrip("来自"),
                        "created_at": datetime.strptime(j["created_at"], '%a %b %d %H:%M:%S %z %Y'),
                        "text": filter_emoji(j["text"]),
                        "like_count": j["like_count"],
                        "mid": mid,
                        "topic_name": key
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
    insert_rows = []
    update_rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # rows = [literal_eval(row) for row in reader]

        # 将评论数据分成需要插入的和需要更新的两部分

        for row in reader:
            existing_record = db.session.query(Comment).filter_by(comment_id=row["comment_id"]).first()
            # 不存在当前行的comments_id，则将当前行添加至数据库
            if existing_record is None:
                insert_rows.append(row)
            else:
                # 否则判断是否需要更新数据操作
                try:
                    if existing_record.like_count != row["like_count"]:
                        existing_record.like_count = row["like_count"]
                        update_rows.append({
                            "comment_id": existing_record.comment_id,
                            "like_count": row["like_count"]
                        })
                    if existing_record.gender != row["gender"]:
                        existing_record.gender = row["gender"]
                        update_rows.append({
                            "comment_id": existing_record.comment_id,
                            "gender": row["gender"]
                        })
                except Exception as e:
                    print(e)
                    continue

    # bulk_insert_mappings() 方法是用于批量插入数据的方法。
    # 它可以将一个由字典对象组成的列表一次性插入到数据库中，从而提高插入数据的效率

    print(insert_rows)
    print(update_rows)

    try:
        # 批量插入新评论数据
        if insert_rows:
            db.session.bulk_insert_mappings(Comment, insert_rows)
            db.session.commit()

        # 批量更新已存在的评论数据
        if update_rows:
            db.session.bulk_update_mappings(Comment, update_rows)
            db.session.commit()
    except Exception as e:
        print(e)
        pass

    # 输出插入和更新的数量
    insertCount = len(insert_rows)
    updateCount = len(update_rows)
    print(f"Inserted: {insertCount}, Updated: {updateCount}")


if __name__ == '__main__':
    start_time = time.time()

    # 回滚之前未提交的事务并关闭数据库连接
    db.session.rollback()
    db.session.close_all()

    words = db.session.execute(text(
        "select distinct word from topic where mention > 3000 order by timeStamp desc;"
    )).fetchall()
    count = 1
    words = words[45:50]
    for word in words:
        key = word[0]
        urls = get_base_url(key)
        print(f"正在获取话题：“{key}”的评论数据，剩余：{len(words) - count}")
        count += 1
        url_list = []
        for url, mid in urls:
            headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                              "Safari/537.36",
                "cookie": "SSOLoginState=1682470171; ALF=1685062171; WEIBOCN_FROM=1110006030; "
                          "SUB=_2A25JTPJtDeRhGeBK7VoU8izJwziIHXVqzp4lrDV6PUJbkdANLVHAkW1NR5N03G2"
                          "-wVzRhnaNYrRd2MlqqnS0eBU-; _T_WM=47174926062; MLOGIN=1; XSRF-TOKEN=47414f; "
                          "M_WEIBOCN_PARAMS=oid%3D{mid}%26luicode%3D20000061%26lfid=%3D{mid}"
                          "%26uicode%3D20000061%26fid%3D{mid}; mweibo_short_token=cac3ff6a1c"
                .format(mid=mid),
                "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'"
            }
            url_list.extend(get_urls(url, headers))
        print(url_list)
        comments_data = get_comments(url_list, key)

        comments_spider.saveAsCSV("./files/comments.csv",
                                  ["comment_id",
                                   "screen_name",
                                   "profile_url",
                                   "gender",
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
