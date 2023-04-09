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

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; ALF=1683600145; SSOLoginState=1681008147; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBwUf6J2kzV-I6DNS3PcQYUML8WqoKXBFFPVyY7sLs0iA.; "
              "SUB=_2A25JNlZEDeRhGeFG6FIX-C7LyT-IHXVqQsCMrDV8PUNbmtAGLUL4kW9NecZsSHFRBaT7YBwOqJfmQBCIr6qIH4hU; "
              "_s_tentry=login.sina.com.cn; Apache=5543990509605.156.1681008151583; "
              "ULV=1681008151592:6:6:1:5543990509605.156.1681008151583:1680932072203; UOR=,,127.0.0.1:5000; "
              "PC_TOKEN=7ab9c640c4 "

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
    for url in urls:
        detailUrl = parse(url).xpath("//p[@class='from']/a[position()=1]/@href")
        for _ in detailUrl:
            u = "https:" + _.split("?")[0]
            if u not in detailUrls:
                detailUrls.append(u)
    print(detailUrls)
    print(len(detailUrls))

def run():
    urls = getUrl()
    getDetailUrl(urls)


run()