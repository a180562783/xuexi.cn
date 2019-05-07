#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# 用户配置：chromedriver.exe文件地址 是否静音
USER_CONFIG = {
    "chrome_driver": r"C:\Users\69540\PycharmProjects\xuexi.cn\chromedriver\chromedriver.exe",
    "chrome_mute": True,
    "hide_page": False,
    "read_time": 120,
    "video_time": 200,
}

WEBSITE = {
    "url": {
        "main": r"https://www.xuexi.cn/",
        "login": r"https://pc.xuexi.cn/points/login.html",
        "my_points": r"https://pc.xuexi.cn/points/my-points.html",
    },
    "xpath": {
        "login": {
            "success": '//*[@id="app"]/div/div[2]/div/div/div[1]/div/a[3]/div/div[2]/div[1]/span',
        },
        "points": {
            "read_points": '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]',
            "video_points": '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[3]/div[2]/div[1]/div[2]',
        },
        "read": {
            "news": '//*[@data-data-id="grid-business-title"]/div/div/div/div/section/div/div/div/div/section/div/div/div/div[2]/section/div/div/div[1]/div[{}]/div/div/div/span',
        },
        "video": {
            # "enter": '//*[@data-data-id="most-beautiful-chinese-title"]/div/div[1]/span',
            "shibo": '//*[@data-data-id="shibo-platform-title"]/div/div[1]/span',
            "shibo_video": '//*[@class="screen"]/div/div[2]/div/div[3]/div/div[{}]/div',
            # "video": '//*[@class="div-background-img-stretching"]/div[2]/div[2]/div/div[{}]/div',
        }
    },
}
