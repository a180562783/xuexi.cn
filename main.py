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
        chrome_options = webdriver.ChromeOptions()
        if self.config["chrome_mute"]:
            chrome_options.add_argument('--mute-audio')  # 关闭声音
        if self.config["hide_page"]:
            chrome_options.add_argument("--headless")  # 隐藏页面
        chrome_driver = self.config["chrome_driver"]  # chromedriver的路径
        # 实例化浏览器
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        driver.maximize_window()

        driver.get(self.website["url"]["login"])
        print("{0}\n请使用软件扫码登录。\n{0}".format(self.sep))
        while True:
            try:
                text = driver.find_element_by_xpath(self.xpath["login"]["success"]).text
                if "学习积分" in text:
                    print("登录成功")
                    break
            except:
                time.sleep(1)

        return driver

    def refresh(self, sleep_time=2):
        self.driver.refresh()
        time.sleep(sleep_time)

    def click(self, key1, key2, value=None):
        try:
            locator = (By.XPATH, self.xpath[key1][key2].format(value))
            WebDriverWait(self.driver, 15, 0.5).until(EC.presence_of_element_located(locator)).click()
        except Exception as e:
            raise e

    def get_page(self, page_name, sleep_time=2):
        self.driver.get(self.website["url"][page_name])
        time.sleep(sleep_time)

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

    def back(self):
        # 关闭新打开的页面
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        self.driver.close()
        # 切换回上个窗口
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])


def get_points_state(browser):
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


def read_one_article(browser, num):
    try:
        browser.click("read", "news", str(num))
    except Exception as e:
        print("点击第{}篇文章失败\n原因：{}".format(num, e))
        return False
    print("阅读第{}篇文章中...等待两分钟。".format(num))
    time.sleep(browser.config["read_time"])
    browser.back()
    return True


def read_article(browser, num):
    need_read_num = num
    print("开始阅读文章，总共需要阅读{}篇".format(need_read_num))
    # 随机选取文章
    random_set = get_random_set(1, 8, need_read_num)
    print("read random:{}".format(random_set))
    while need_read_num:
        print("尚需阅读{}篇文章".format(need_read_num))
        browser.get_page("main")
        read_one_article(browser, random_set.pop())
        need_read_num -= 1

    print("阅读文章结束\n{}".format(browser.sep))
    return True


def get_random_set(start, end, num):
    random_set = set()
    while len(random_set) != num:
        random_set.add(random.randint(start, end))

    return random_set


def watch_video(browser, num):
    need_watch_num = num
    print("开始观看视频，共需观看{}部".format(need_watch_num))
    browser.get_page("main", 10)
    browser.click("video", "shibo")
    browser.cur_page()

    # 随机选取
    random_set = get_random_set(3, 20, need_watch_num)
    print("video random:{}".format(random_set))
    while need_watch_num:
        print("尚需观看视频{}部，每部观看三分钟...".format(need_watch_num))
        browser.click("video", "shibo_video", value=random_set.pop())
        # time.sleep(5)
        time.sleep(browser.config["video_time"])
        browser.back()
        need_watch_num -= 1

    # time.sleep(200)

    return True


def auto_get_points(browser):
    # 获取当前积分情况
    points_state = get_points_state(browser)

    while points_state["read_point"] != points_state["read_point_all"] or \
            points_state["video_point"] != points_state["video_point_all"]:
        # 读文章 2分钟1篇
        read_article(browser, points_state["read_point_all"] - points_state["read_point"])
        points_state = get_points_state(browser)
        # 看视频 3分钟1部
        watch_video(browser, points_state["video_point_all"] - points_state["video_point"])
        points_state = get_points_state(browser)

    # 任务结束
    return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # 登录
    browser = Browser(USER_CONFIG, WEBSITE)
    # 自动获取积分
    auto_get_points(browser)
    # 任务结束
    del browser
