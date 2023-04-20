import os

from sqlalchemy import text

from spider.weibo.analyse import db

from spider.weibo.Spider import Spider

# [('2023考研报录比约6比1', 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%232023考研报录比约6比1%23%26t%3D0&title
# =热门-', 'https://m.s.weibo.com/ajax_topic/trend?q=%232023考研报录比约6比1%23'), ('你还在用余额宝吗',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23你还在用余额宝吗%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23你还在用余额宝吗%23'), ('左肩有你 振兴钢厂',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23左肩有你 振兴钢厂%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23左肩有你 振兴钢厂%23'), ('我为家乡特色美食来代言',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23我为家乡特色美食来代言%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23我为家乡特色美食来代言%23'), ('数名外籍女子晒中国游引出偷渡案',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23数名外籍女子晒中国游引出偷渡案%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23数名外籍女子晒中国游引出偷渡案%23'), ('易烊千玺专辑封面是巩俐',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23易烊千玺专辑封面是巩俐%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23易烊千玺专辑封面是巩俐%23'), ('瓣人选的95花四美',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23瓣人选的95花四美%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23瓣人选的95花四美%23'), ('离职后你一般怎么退出工作群',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23离职后你一般怎么退出工作群%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23离职后你一般怎么退出工作群%23'), ('迪丽热巴再现复古名伶',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23迪丽热巴再现复古名伶%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23迪丽热巴再现复古名伶%23'), ('追梦格林被驱逐',
# 'https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D%23追梦格林被驱逐%23%26t%3D0&title=热门-',
# 'https://m.s.weibo.com/ajax_topic/trend?q=%23追梦格林被驱逐%23')]

spider = Spider()


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
    os.chdir("/media/venyy/Codes/project/spider/weibo")
    current_dir = os.getcwd()
    word, trend = queryData()
    data = parseData(word, trend)
    spider.saveAsJson(f"{current_dir}/files/trend.json", data)


# run()