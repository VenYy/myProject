# 参考：https://zhuanlan.zhihu.com/p/498425181


# 内容：text = "//div[@class='card-feed']/div[@class='content']/p/text()"
# 链接：href = "//div[@class='card-feed']/div[@class='content']/p[@class='from']/a[position()=1]/@href"
# 唯一ID：mid = "//div[@class='m-con-l']/div/div/@mid"
# 作者：author = "//p[@node-type='feed_list_content']/@nick-name"
# 转发：forward = "//div[@class='card-act']/ul/li[position()=2]"
# 评论：comment = "//div[@class='card-act']/ul/li[position()=3]"
# 点赞：like = "//div[@class='card-act']/ul/li[position()=4]"

import requests
import json
from lxml import etree
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": ""

}


def parse(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    html = etree.HTML(resp.text)
    return html

def getUrl():
    urls = []
    with open("files/topic_band.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for i in data["data"]:
        # print(i["链接"])
        if i["讨论量"] > 2000:
            urls.append(i["链接"])
    return urls

def getDetailUrl(urls):
    detailUrls = []
    pattern = '([A-Za-z0-9]+)'
    for url in urls:
        detailUrl = parse(url).xpath("//p[@class='from']/a[position()=1]/@href")
        for _ in detailUrl:
            u = "https:" + _.split("?")[0]
            id = re.findall(pattern, u)[4]
            wbApi = f"https://weibo.com/ajax/statuses/show?id={id}"
            if wbApi not in detailUrls:
                detailUrls.append(wbApi)
    # print(detailUrls)
    # print(len(detailUrls))
    return detailUrls

def run():
    urls = getUrl()
    detailUrls = getDetailUrl(urls)
    print(detailUrls)


run()
