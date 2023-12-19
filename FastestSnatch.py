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
    loginSignal = QtCore.pyqtSignal()

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
        self.loginUrl_Taobao = 'https://login.taobao.com/member/login.jhtml'
        self.loginUrl_Jingdong = 'https://passport.jd.com/new/login.aspx'

        # 目标XPath
        self.aimXPath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button[1]/span'

        # 请求方法
        self.method = 'post'
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

        self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
        self.scheduler.add_job(self.snatchStart, 'interval', seconds=1, id='snatch')

    def getCookies(self):
        """
        获取Cookies
        :return:
        """
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
        browser.get(self.loginUrl_Taobao)
        # 点击跳转扫码界面
        browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div/div[1]/i').click()
        # 静止
        time.sleep(2)
        # 间隔停滞
        time.sleep(round(random.uniform(1, 2), 2))
        print('寻找二维码！')
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
                user = browser.find_element(By.XPATH,
                                            '//*[@id="J_Col_Main"]/div/div[1]/div/div[1]/div[1]/div/div[1]/a/em').text
                # 输出用户信息
                print('您的帐户:' + user)
                # 关闭二维码图像浏览窗口
                self.qrcodeSignal.emit({'operation': 'close', 'username': user})
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
        # print('cookies:' + str(cookies))

    def getSession(self):
        # self.session = requests.request(url='')
        pass

    def login(self):
        """
        登陆函数
        :return:
        """
        print('尝试登陆...')
        try:
            request = self.session.get('https://i.taobao.com/user/baseInfoSet.htm?').text
            print(request)
            if '账号管理' in request:
                print("登录成功！")
                return True
            else:
                print("登录失败！请等待初始化...")
                # 重新获取cookies
                self.loginSignal.emit()
                return False
        except Exception as e:
            print('登陆出错！' + str(e))

    def snatchStart(self):
        """
        抢购请求函数
        :return:
        """
        try:
            print(self.aimXPath)
        except Exception as e:
            print(str(e))
        finally:
            pass

    def jobStart(self):
        if self.login():
            print('开抢！')
            if not self.scheduler.running:
                self.scheduler.start()
            else:
                self.scheduler.resume_job('snatch')

    def jobPause(self):
        print('不抢！')
        self.scheduler.pause_job('snatch')
