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
    resultSignal = QtCore.pyqtSignal(str)

    def __init__(self, interval=1):
        super().__init__()
        # 间隔时间
        self.interval = interval
        # 开始时间
        self.startTime = None
        # 停止时间
        self.endTime = None
        # 请求url
        self.url = None

        # 目标XPath
        self.XPath = '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[6]/div[1]/button[1]/span'

        # 请求方法
        self.method = 'post'
        # 请求头
        self.User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/120.0.0.0 Safari/537.36 " \
                          "Edg/120.0.0.0"
        self.headers = {'User-Agent': self.User_Agent}
        # 参数体
        self.params = {}
        # 请求体
        self.body = {}

        self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    def updateSettings(self, settings):
        # 间隔时间1, 0.5, 0.1, 0.01, 0.005, 0.001
        self.interval = settings['interval']
        # 请求头合并
        self.headers.update(settings['headers'])
        # 更新params参数
        self.params.update(settings['params'])
        # 更新请求body参数
        self.body.update(settings['body'])
        # XPath元素
        # self.XPath = settings['XPath']

        # 开始时间
        self.startTime = settings['startTime']
        # 停止时间
        self.endTime = settings['endTime']

        # url
        self.url = settings['url']

    def submitOrder(self):
        """
        订单生成函数
        :return:
        """
        pass

    def snatchStart(self):
        """
        抢购请求函数
        :return:
        """
        try:
            print(self.XPath)
            # 发送控制台结果
            self.resultSignal.emit(self.XPath)
        except Exception as e:
            print(str(e))
            # 输出控制台报错
            self.resultSignal.emit(str(e))
        finally:
            pass

    def jobStart(self):
        if not self.scheduler.running:
            # print('开抢！')
            self.resultSignal.emit('启动定时任务，开抢！')
            self.scheduler.add_job(self.snatchStart, 'interval', seconds=self.interval, id='snatch')
            self.scheduler.start()

    def jobPause(self):
        if self.scheduler.running:
            # print('不抢！')
            self.resultSignal.emit('结束定时任务，不抢！')
            self.scheduler.shutdown()
            self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
