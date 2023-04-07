import requests
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 "
                  "Safari/537.36 "
}

url = "https://api.bilibili.com/x/v1/dm/list.so?oid=1077949812"

response = requests.get(url, headers=headers)
response.encoding = "utf-8"
# print(response.text)
# print(response.status_code)
comments = re.findall('<d.*?>(.*?)</d>', response.text)


for comment in comments:
    # print(comment, end="\n")
    with open("./files/comments.txt", mode="a", encoding="utf-8") as f:
        f.write(comment)
        f.write("\n")
