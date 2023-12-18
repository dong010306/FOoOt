#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> FastestSnatch
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/18 14:35
@Desc   ：
=================================================="""
import random
import threading
import time
from io import BytesIO
from queue import Queue

import psutil
import requests
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.common.by import By


class FastestSnatch(QWidget):
    qrcodeSignal = QtCore.pyqtSignal(dict)

    def __init__(self, interval, outAttempts):
        super().__init__()
        # 间隔时间
        self.interval = interval
        # 尝试次数
        self.outAttempts = outAttempts
        # 开始时间
        self.startDatetime = None
        # 停止时间
        self.stopDatetime = None
        # 请求url
        self.url = 'https://login.taobao.com/member/login.jhtml'
        # 请求方法
        self.method = ''
        # 请求头
        self.User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/120.0.0.0 Safari/537.36 " \
                          "Edg/120.0.0.0"
        self.headers = {'User-Agent': self.User_Agent}
        # 参数体
        self.params = None
        # 请求体
        self.body = None

        # 账号
        self.username = ''
        # 密码
        self.password = ''
        # session并存放headers
        self.session = requests.session()
        self.session.headers.update(self.headers)

        # 存放请求结果
        self.queue = Queue(maxsize=100)

        self.scheduler = BlockingScheduler(timezone='Asia/Shanghai')
        self.scheduler.add_job(self.snatchStart, 'interval', seconds=1)
        # self.scheduler.add_job(self.snatchStart, 'corn', hour=0)

        self.snatchThread = threading.Thread(target=self.scheduler.start, name='snatchThread')
        self.snatchThread.daemon = True

    def getCookies(self):
        # webdriver设置
        options = webdriver.ChromeOptions()
        # 去掉webdriver痕迹
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("disable-blink-features=AutomationControlled")
        # 无界面启动
        options.add_argument('--headless')
        # webdriver启动
        browser = webdriver.Chrome(options=options)
        # url = 'https://login.taobao.com/member/login.jhtml'
        browser.get(self.url)
        # 点击跳转扫码界面
        browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div/div[1]/i').click()
        # 静止
        time.sleep(2)
        # 间隔停滞
        time.sleep(round(random.uniform(1, 2), 2))
        # 获取并保存二维码截图
        qrcode_img_data = browser.find_element(By.XPATH, '//*[@id="login"]/div[2]/div/div[1]/div[1]').screenshot_as_png
        qrcode_img = Image.open(BytesIO(qrcode_img_data))
        qrcode_img.save('./user_images/qrcode.png')
        self.qrcodeSignal.emit({'operation': 'open', 'path': '/user_images/qrcode.png'})
        print("请扫码登录！")
        time.sleep(2)
        # 尝试次数
        attempt = 0
        while attempt < self.outAttempts:
            try:
                # 寻找页面中的用户名元素
                info = browser.find_element(By.XPATH,
                                            '//*[@id="J_Col_Main"]/div/div[1]/div/div[1]/div[1]/div/div[1]/a/em').text
                # 输出用户信息
                print('您的帐户:' + info)
                # 关闭二维码图像浏览窗口
                self.qrcodeSignal.emit({'operation': 'close', 'username': info})
                # 结束检测循环
                break
            except Exception as e:
                attempt += 1
                time.sleep(2)
        if attempt == self.outAttempts:
            return
        # 获取Cookie并保持在session中
        selenium_cookies = browser.get_cookies()
        # 间隔停滞
        time.sleep(round(random.uniform(1, 2), 2))
        # 退出浏览器
        browser.quit()
        # 创建cookiesJar并获取所有
        cookies = RequestsCookieJar()
        for item in selenium_cookies:
            cookies.set(item["name"], item["value"])
        # 保存本地session
        self.session.cookies.update(cookies)

    def getSession(self):
        # self.session = requests.request(url='')
        pass

    def snatchStart(self):
        """
        抢购请求函数
        :return:
        """
        try:
            requests.request(url=self.url, method=self.method)
        except Exception as e:
            print(str(e))
        finally:
            pass

    def jobStart(self):
        print('Snatch is Starting！')
        self.snatchThread.start()
