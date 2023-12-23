#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> FOoOtLoginFunc
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/23 21:39
@Desc   ：
=================================================="""
import os
import sys
import threading

import typing

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel

from FOoOtFunc import FOoOtWindow
from FOoOtLogin import Ui_Login
from Identity import Identity


class FOoOtLoginWindow(Ui_Login, QWidget):
    loginSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        # 初始化UI
        self.setupUi(self)
        # 认证类
        self.identity = Identity()
        # 信号桉树
        self.qrcodeButton.clicked.connect(self.initQrcode)
        # 二维码信号触发
        self.identity.qrcodeSignal.connect(self.qrcodeDialogShow)
        # 登陆信号触发
        self.identity.loginSignal.connect(self.loginResult)

    def initQrcode(self):
        # 选择平台url
        self.identity.selectPlatforms(self.platformBox_qrcode.currentText())
        # 启动初始化线程
        getCookiesThread = threading.Thread(target=self.identity.loginByQrcode)
        # 设置守护线程
        getCookiesThread.daemon = True
        # 启动线程
        getCookiesThread.start()

    def qrcodeDialogShow(self, message):
        """
        二维码启动函数
        :param message:
        :return:
        """
        # 区分操作，信号控制，打开
        print(message)
        # 获取二维码图片地址
        image_path = message
        url_father = os.path.dirname(os.path.abspath(__file__))
        image_path = url_father + image_path
        # 加载图片
        labelPix = QLabel("show", self)
        pic = QPixmap(image_path)
        labelPix.setPixmap(pic)
        # 打开对话框
        self.qrcodeLayout.addWidget(labelPix)

    def loginResult(self, message):
        # 区分操作，信号控制，打开
        print(message)
        # 关闭
        if message['result']:
            # 打开主页面
            self.loginSignal.emit()
            # 关闭登入页面
            self.hide()
        else:
            self.qrcodeLayout.itemAt(0).widget().deleteLater()

    def closeEvent(self, a0: typing.Optional[QtGui.QCloseEvent]) -> None:
        sys.exit()
