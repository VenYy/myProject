import os
import time
from datetime import datetime
from spider.weibo.Spider import *


def parseData(html):
    words = html.xpath("//tbody/tr/td/a/text()")[1:]            # 词条
    # print(len(words), words)
    hot = html.xpath("//tbody/tr/td/span/text()")               # 热度
    hots = []
    for _ in hot:
        hot = _.split(" ")[1]
        hots.append(hot)
    # print(len(hots), hots)

    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M")     # 时间

    result = []
    trendResult = []

    if len(words) == len(hots):
        for word, hot in zip(words, hots):
            # print(word, hot)
            if len(hot) == 0:
                # print(word, hot)
                pass
            else:
                key = f"%23{word}%23"
                href = f"https://m.weibo.cn/p/index?containerid=231522type%3D60%26q%3D{key}%26t%3D0&title=热门-"
                trend = f"https://m.s.weibo.com/ajax_topic/trend?q={key}"
                result.append({"timeStamp": timeStamp, "word": word, "hot": hot, "href": href})
                # 热搜词条趋势
                trendResult.append({"word": word, "href": href, "trend": trend})
        return result, trendResult
    else:
        return None





def run():
    os.chdir("/media/venyy/Codes/project/spider/weibo")
    current_dir = os.getcwd()
    hotSearchSpider = Spider()
    hotSearchSpider.url = "https://s.weibo.com/top/summary/"
    html = hotSearchSpider.parse()
    data, trendResult = parseData(html)
    hotSearchSpider.saveAsCSV(path=f"{current_dir}/files/hotSearch.csv", data=data,
                              item_list=["timeStamp", "word", "hot", "href"])
    hotSearchSpider.saveAsCSV(path=f"{current_dir}/files/searchTrend.csv", data=trendResult,
                              item_list=["word", "href", "trend"])
    # hotSearchSpider.saveAsJson(path="./files/hotSearch.json", jData={"data": data})
    print("Saving hotSearch....")

# run()