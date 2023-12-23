#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> Identity
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/23 21:44
@Desc   ：
=================================================="""
import random
import time
from io import BytesIO

import requests
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.common.by import By


class Identity(QWidget):
    qrcodeSignal = QtCore.pyqtSignal(str)
    loginSignal = QtCore.pyqtSignal(dict)

    def __init__(self):
        """
        初始化函数
        """
        super(Identity, self).__init__()
        self.loginUrl_Taobao = 'https://login.taobao.com/member/login.jhtml'
        self.loginUrl_Jingdong = 'https://passport.jd.com/new/login.aspx'
        # 登陆最终url
        self.loginUrl = None
        # 尝试次数
        self.outAttempts = 50
        # 请求头
        self.User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/120.0.0.0 Safari/537.36 " \
                          "Edg/120.0.0.0"
        self.headers = {'User-Agent': self.User_Agent}
        # 账号
        self.username = ''
        # 密码
        self.password = ''
        # session并存放headers
        self.session = requests.session()
        # 合并session
        self.session.headers.update(self.headers)

    def selectPlatforms(self, label):
        """
        选择平台
        :param label:
        :return:
        """
        print(label)
        if label == '淘宝':
            self.loginUrl = self.loginUrl_Taobao
        if label == '京东':
            self.loginUrl = self.loginUrl_Jingdong

    def loginByPassword(self, username, password):
        pass

    def loginByQrcode(self):
        """
        获取Cookies, 登陆
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
        browser.get(self.loginUrl)
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
        self.qrcodeSignal.emit('/user_images/qrcode.png')
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
                self.loginSignal.emit({'username': user, 'result': True})
                # 结束检测循环
                break
            except Exception as e:
                attempt += 1
                time.sleep(2)
        if attempt == self.outAttempts:
            self.loginSignal.emit({'result': False})
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
