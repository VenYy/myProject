import time

from spider.weibo import hotTopic, hotSearch, analyse

count = 1
while True:
    print(f"第{count}次处理")
    hotSearch.run()
    hotTopic.run()
    count += 1
    time.sleep(1000*60)
    analyse.run()