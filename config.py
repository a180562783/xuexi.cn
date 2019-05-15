#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# 用户配置
USER_CONFIG = {
    # 此项必填！
    "chrome_driver": "xxx",
    # "chrome_driver": r"C:\Users\69540\PycharmProjects\xuexi.cn\chromedriver\chromedriver.exe",
    # 下列可选
    "chrome_mute": True,  # 浏览器静音
    "hide_page": False,  # 浏览器隐藏，浏览器如果隐藏则不算有效阅读
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
            "shiping_title": '//*[@data-data-id="shiping-title"]/div/div[2]/span',
            "comment": '//*[@data-data-id="textListGrid"]/div/div/div/div[{}]/div/div/div/span',
        },
        "video": {
            "active_btn": '//*[@class="btn active"]',
            "next_btn": '//*[@class="btn"]',
            "tv": '//*[@id="root"]/div/header/div[2]/div[1]/div[2]/a[2]',
            "videos": '//*[@id="dcd4"]/div/div/div/div/div/section/div[2]',
            "one_video": '//*[@class="Pic"]',
        }
    },
}
