from datetime import datetime
import time
import requests
import csv
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
              "Safari/537.36 ",
    "cookie": "SINAGLOBAL=9551435337052.799.1680615041641; UOR=,,login.sina.com.cn; "
              "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UsQWzFS7rHN-kXpM6N5vH5JpX5KMhUgL"
              ".FoMRe05c1h5Neoe2dJLoI79c9g44wHYt; "
              "ULV=1680776206447:3:3:3:6939995810390.054.1680776206404:1680672584157; "
              "XSRF-TOKEN=RQjjhHUnsRsek3sJ8QfXf0UO; ALF=1683437419; SSOLoginState=1680845421; "
              "SCF=Ap1xha1wDXEMROVsZPqkRYk02OfrzUpAyhNjiuEBCsrBgVu-cCTDKRTpCtYGUbJH3aca_0FMADYM1MJgTHlWDho.; "
              "SUB=_2A25JK9o-DeRhGeFG6FIX-C7LyT-IHXVqQUz2rDV8PUNbmtAbLU_jkW9NecZsSCCDZZnxKJ3Alu8T_zz4R2aoobH0; "
              "WBPSESS=qJtA5EKTVAmfo4ozVa9MnqvcR0zz7rHwqy8Cz3zSQ"
              "-fuYQI67cm_6vqyKlGjiP94F6hqvKXCIQqCypSb5EqFptlUUWcLjNXwIeGzPmY2LtzRsKrmARkZlIuBWgDo"
              "-c3EFya9WSX4iMkZOTfXXXnEQw== "

}

def parse(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    # print(resp.text)
    html = etree.HTML(resp.text)
    return html

def parse_data(html):
    words = html.xpath("//tbody/tr/td/a/text()")[1:]            # 词条
    # print(len(words), words)
    hot = html.xpath("//tbody/tr/td/span/text()")               # 热度
    hots = []
    for _ in hot:
        hot = _.split(" ")[1]
        hots.append(hot)
    # print(len(hots), hots)

    time_stamp = datetime.now().strftime("%Y/%m/%d  %H:%M")     # 时间





    result = []

    if len(words) == len(hots):
        for word, hot in zip(words, hots):
            # print(word, hot)
            if len(hot) == 0:
                # print(word, hot)
                pass
            else:
                result.append({"时间": time_stamp, "词条": word, "热度": hot})
        return result
    else:
        return None

def save(path, item_list, data):
    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=item_list)
        writer.writeheader()
        writer.writerows(data[::-1])  # 按行写入数据
def run():
    url = "https://s.weibo.com/top/summary/"
    html = parse(url)
    data = parse_data(html)
    # print(data)
    path = "./files/hot_band_bak.csv"
    item_list = ["时间", "词条", "热度"]
    save(path, item_list, data)


if __name__ == '__main__':
    count = 1
    while True:
        run()
        print(f"Saving{count}-----")
        count += 1
        time.sleep(60)