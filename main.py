#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import sys
import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *

VIDEO_HISTORY = set()
ARTICLE_HISTORY = set()


class Browser:
    def __init__(self, config, website):
        self.config = config
        self.website = website
        self.xpath = self.website["xpath"]
        self.sep = "*" * 30
        self.driver = self._login()

    def __del__(self):
        self.driver.quit()

    def _login(self):
        # chrome配置
        chrome_options = webdriver.ChromeOptions()
        if self.config["chrome_mute"]:
            chrome_options.add_argument('--mute-audio')  # 关闭声音
        if self.config["hide_page"]:
            chrome_options.add_argument("--headless")  # 隐藏页面

        chrome_driver = self.config["chrome_driver"]  # chromedriver的路径
        # 确保chromedriver.exe文件存在
        if not os.path.exists(chrome_driver):
            print("任务失败！")
            print("请按README.md说明文档配置chromedriver.exe文件地址到系统路径，并在config.py文件中补充。")
            time.sleep(120)
            sys.exit(-1)
        # 实例化浏览器
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        driver.maximize_window()
        # 加载登录页面
        driver.get(self.website["url"]["login"])
        # 移动页面到最下方，显示二维码
        try:
            locator = (By.XPATH, self.xpath["login"]["login_text"])
            WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located(locator))
            js = "var q=document.documentElement.scrollTop=" + str(3000)
            driver.execute_script(js)
        except Exception as e:
            raise e

        # 等待用户扫码登录
        print("{0}\n请使用软件扫码登录。\n{0}".format(self.sep))
        while True:
            try:
                text = driver.find_element_by_xpath(self.xpath["login"]["success"]).text
                # 扫码登陆成功
                if "学习积分" in text:
                    if self.config["hide_page"]:
                        driver.minimize_window()
                    break
            except:
                time.sleep(1)

        return driver

    def refresh(self, sleep_time=2):
        self.driver.refresh()
        time.sleep(sleep_time)

    def wait(self, key1, key2, wait_time=15):
        try:
            locator = (By.XPATH, self.xpath[key1][key2])
            WebDriverWait(self.driver, wait_time, 0.5).until(EC.presence_of_element_located(locator))
        except Exception as e:
            raise e

    def click(self, key1, key2, index=-100, value=None):
        if index < -99:
            try:
                locator = (By.XPATH, self.xpath[key1][key2].format(value))
                WebDriverWait(self.driver, 15, 0.5).until(EC.presence_of_element_located(locator)).click()
                self.cur_page()
            except Exception as e:
                raise e
        else:
            try:
                locator = (By.XPATH, self.xpath[key1][key2].format(value))
                WebDriverWait(self.driver, 15, 0.5).until(EC.presence_of_element_located(locator))
                self.driver.find_elements_by_xpath(self.xpath[key1][key2])[index].click()
                self.cur_page()
            except Exception as e:
                raise e

    def page_down(self, lenth=1000):
        js = "var q=document.documentElement.scrollTop=" + str(lenth)
        self.driver.execute_script(js)

    def page_scroll(self, downward, all_time):
        # 页面滚动即是有效阅读
        if downward:
            length = random.randint(100, 300)
            for i in range(1, 11):
                self.page_down(length)
                time.sleep(all_time // 10)
                length += random.randint(100, 300)
        else:
            for i in range(1, 11):
                self.page_down(random.randint(200, 500))
                time.sleep(all_time // 10)

    def get_page(self, page_name, sleep_time=2, distance=0):
        self.driver.get(self.website["url"][page_name])
        time.sleep(sleep_time)
        self.page_down(distance)

    def get_text(self, key1, key2, index=-1, wait_time=15):
        if not wait_time:
            if index < 0:
                return self.driver.find_element_by_xpath(self.xpath[key1][key2]).text
            else:
                return self.driver.find_elements_by_xpath(self.xpath[key1][key2])[index].text
        else:
            locator = (By.XPATH, self.xpath[key1][key2])
            if index < 0:
                return WebDriverWait(self.driver, wait_time, 0.5).until(EC.presence_of_element_located(locator)).text
            elif index >= 0:
                return WebDriverWait(self.driver, wait_time, 0.5).until(EC.presence_of_all_elements_located(locator))[
                    index].text

    def cur_page(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        if self.config["hide_page"]:
            self.driver.minimize_window()

    def back(self):
        self.cur_page()
        self.driver.close()
        self.cur_page()


def get_random_num(start, end, history):
    if len(history) == int(end - start + 1):
        print("history 已满。")
        history.clear()
    num = random.randint(start, end)
    while num in history:
        num = random.randint(start, end)
    return num


def get_my_points(browser):
    browser.get_page("my_points")
    print("今日积分获取情况")
    read_point = browser.get_text("points", "read_points")
    video_point = browser.get_text("points", "video_points")
    print("阅读积分：{0}\n视频积分：{1}\n{2}".format(read_point, video_point, browser.sep))
    return {
        "read_point": int(read_point.split('/')[0][0]),
        "read_point_all": int(read_point.split('/')[1][0]),
        "video_point": int(video_point.split('/')[0][0]),
        "video_point_all": int(video_point.split('/')[1][0]),
    }


def read_one_article(browser):
    # 获取一篇未读过的文章
    random_num = get_random_num(1, 20, ARTICLE_HISTORY)
    ARTICLE_HISTORY.add(random_num)
    print("阅读历史：{}".format(ARTICLE_HISTORY))
    # 读文章
    browser.click("read", "comment", value=str(random_num))
    browser.page_scroll(downward=True, all_time=browser.config["read_time"])
    browser.back()
    return True


def read_article(browser, need_read_num):
    print("开始阅读文章，总共需要阅读{}篇".format(need_read_num))
    # 进入学习时评
    browser.get_page("main", sleep_time=5, distance=1500)
    browser.click("read", "shiping_title")
    while need_read_num:
        print("尚需阅读{0}篇文章".format(need_read_num))
        read_one_article(browser)
        need_read_num -= 1
    browser.back()
    print("阅读文章结束\n{}".format(browser.sep))
    return True


def watch_one_video(browser):
    # 获取未观看过的视频
    random_num = get_random_num(0, 19, VIDEO_HISTORY)
    VIDEO_HISTORY.add(random_num)
    print("视频历史：{}".format(VIDEO_HISTORY))
    # 看视频
    browser.click("video", "one_video", index=random_num)
    browser.page_scroll(downward=False, all_time=browser.config["video_time"])
    browser.back()
    return True


def watch_video(browser, need_watch_num):
    print("开始观看视频，共需观看{}部".format(need_watch_num))
    # 进入学习电视台
    browser.get_page("main", 5)
    browser.click("video", "tv")
    browser.click("video", "videos")
    # 随机翻几页
    page = random.randint(1, 11)
    while True:
        if browser.get_text("video", "active_btn") == str(page):
            break
        else:
            browser.click("video", "next_btn", index=-2)
            time.sleep(1)
    while need_watch_num:
        print("尚需观看视频{0}部".format(need_watch_num))
        watch_one_video(browser)
        need_watch_num -= 1
    browser.back()
    print("观看视频结束\n{}".format(browser.sep))
    return True


def auto_get_points(browser):
    # 获取当前积分情况
    my_points = get_my_points(browser)

    # 读文章 2分钟1篇
    while my_points["read_point"] != my_points["read_point_all"]:
        read_article(browser, my_points["read_point_all"] - my_points["read_point"])
        my_points = get_my_points(browser)

    # 看视频 3分钟1部
    while my_points["video_point"] != my_points["video_point_all"]:
        watch_video(browser, my_points["video_point_all"] - my_points["video_point"])
        my_points = get_my_points(browser)

    return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    # 登录
    browser = Browser(USER_CONFIG, WEBSITE)
    # 自动获取积分
    auto_get_points(browser)
