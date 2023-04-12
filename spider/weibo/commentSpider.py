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
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; UOR=,,login.sina.com.cn; ALF=1683678659; SSOLoginState=1681086661; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBxASdB1XQFZvUju25WH0QFpXlXJ5mZ0vB6eoeCuqSpfM.; "
              "SUB=_2A25JNyiWDeRhGeFG6FIX-C7LyT-IHXVqRR1erDV8PUNbmtAGLVWhkW9NecZsSFsW-xJ2UpD3LHbc3goM7dV77gwx; "
              "_s_tentry=login.sina.com.cn; Apache=4824609377262.867.1681086669169; "
              "ULV=1681086669188:8:8:3:4824609377262.867.1681086669169:1681033533220; PC_TOKEN=9340f12267; "
              "WBStorage=4d96c54e|undefined "

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