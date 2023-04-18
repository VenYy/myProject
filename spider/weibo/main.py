import time

from spider.weibo import hotTopic, analyse, hotSearch, searchTrend

if __name__ == '__main__':
    count = 1
    while True:
        print(f"第{count}次执行")

        hotTopic.run()
        hotSearch.run()
        analyse.run()
        searchTrend.run()

        count += 1

        time.sleep(60*5)