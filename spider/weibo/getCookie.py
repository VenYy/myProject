import json
import time

from selenium import webdriver


def get_cookie_from_network():
    from selenium import webdriver

    url_login = 'http://login.weibo.cn/login/'
    driver = webdriver.PhantomJS()

    driver.get(url_login)

    driver.find_element_by_xpath('//input[@type="text"]').send_keys('your_weibo_accout')  # 改成你的微博账号

    driver.find_element_by_xpath('//input[@type="password"]').send_keys('your_weibo_password')  # 改成你的微博密码

    driver.find_element_by_xpath('//input[@type="submit"]').click()  # 点击登录

    # 获得 cookie信息

    cookie_list = driver.get_cookies()

    cookie_dict = {}

    for cookie in cookie_list:

        # 写入文件

        f = open(cookie['name'] + '.weibo', 'w')

        pickle.dump(cookie, f)

        f.close()

        if cookie.has_key('name') and cookie.has_key('value'):
            cookie_dict[cookie['name']] = cookie['value']

    return cookie_dict
