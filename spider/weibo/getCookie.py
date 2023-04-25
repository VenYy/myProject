import json
import os
import time

import requests
from selenium import webdriver


os.chdir("/media/venyy/Codes/project/spider/weibo/")
def init_browser():
    path = "../../chromedriver"
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)
    driver.maximize_window()
    driver.get("https://m.weibo.cn/login")
    time.sleep(20)
    return driver


def get_cookies(driver):
    driver.get("https://m.weibo.cn/login")
    time.sleep(30)
    cookies = driver.get_cookies()
    jsCookies = json.dumps(cookies)
    with open("./files/cookies.txt", "w", encoding="utf-8") as f:
        f.write(jsCookies)
    print("写入cookie中")


def read_cookies():
    files = os.path.exists('./files/cookies.txt')
    if files:
        with open('./files/cookies.txt', 'r', encoding='utf-8') as f:
            Cookies = json.loads(f.read())
        cookies = []
        for cookie in Cookies:
            cookie_dict = {
                'domain': '.weibo.cn',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                'expires': '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            cookies.append(cookie_dict)
        return cookies
    else:
        return False


def check_cookies():
    cookies = read_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie["name"], cookie["value"])
    resp = s.get("https://m.weibo.cn")
    resp.encoding = resp.apparent_encoding
    html_t = resp.text
    print(html_t)
    if "登录/注册" in html_t:
        return False
    else:
        return True


def login(driver):
    cookies = read_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(3)
    driver.refresh()    # 刷新网页



if __name__ == '__main__':
    # 从本地读取cookie
    flag = read_cookies()
    if flag:
        # 验证cookie是否有效
        res = check_cookies()
        # cookie 无效，重新登录
        if not res:
            print("cookie 无效，需要重新登录")
            driver = init_browser()
            get_cookies(driver)
        else:
            # 登录成功
            driver = init_browser()
    else:
        # 扫码登录
        driver = init_browser()
        get_cookies(driver)
