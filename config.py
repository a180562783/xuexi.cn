#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# 用户配置
USER_CONFIG = {
    # 此项必填！
    "chrome_driver": "xxx",
    # "chrome_driver": r"C:\Users\69540\PycharmProjects\xuexi.cn\chromedriver\chromedriver.exe",
    # 下列可选
    "chrome_mute": True,  # 浏览器静音
    "hide_page": False,  # 浏览器隐藏
    "read_time": 130,  # 一篇文章的阅读时间
    "video_time": 190,  # 一部视频的观看时间
}

WEBSITE = {
    "url": {
        "main": r"https://www.xuexi.cn/",
        "login": r"https://pc.xuexi.cn/points/login.html",
        "my_points": r"https://pc.xuexi.cn/points/my-points.html",
    },
    "xpath": {
        "login": {
            "login_text": '//*[@class="ddlogintext"]',
            "success": '//*[@id="app"]/div/div[2]/div/div/div[1]/div/a[3]/div/div[2]/div[1]/span',
        },
        "points": {
            "read_points": '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]',
            "video_points": '//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[3]/div[2]/div[1]/div[2]',
        },
        "read": {
            "news": '//*[@data-data-id="grid-business-title"]/div/div/div/div/section/div/div/div/div/section/div/div/div/div[2]/section/div/div/div[1]/div[{}]/div/div/div/span',
            "shiping": '//*[@data-data-id="shiping-text-list-grid"]/div/div/div/div[{}]/div/div/div/span',
        },
        "video": {
            # "enter": '//*[@data-data-id="most-beautiful-chinese-title"]/div/div[1]/span',
            "shibo": '//*[@data-data-id="shibo-platform-title"]/div/div[1]/span',
            "shibo_video": '//*[@class="screen"]/div/div[2]/div/div[3]/div/div[{}]/div',
            "tv": '//*[@id="root"]/div/header/div[2]/div[1]/div[2]/a[2]',
            "videos": '//*[@id="dcd4"]/div/div/div/div/div/section/div[2]',
            "one_video": '//*[@class="Pic"]',
            # "video": '//*[@class="div-background-img-stretching"]/div[2]/div[2]/div/div[{}]/div',
        }
    },
}
