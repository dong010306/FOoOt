#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> FOoOtFunc
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/18 14:24
@Desc   ：
=================================================="""
import os
import sys
import threading

import typing

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel

from FOoOt import Ui_FOoOt
from FastestSnatch import FastestSnatch
from QrcodeFunc import QrcodeDialog


class FOoOtWindow(Ui_FOoOt, QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化UI
        self.setupUi(self)
        # 最速抢夺
        self.fastestSnatch = FastestSnatch(1, 30)
        # 抢夺触发按钮回调
        self.startButton.clicked.connect(self.fastestSnatch.jobStart)
        self.stopButton.clicked.connect(self.fastestSnatch.jobPause)
        self.initButton.clicked.connect(self.initUser)
        self.fastestSnatch.loginSignal.connect(self.initUser)
        # 启动二维码窗口
        self.fastestSnatch.qrcodeSignal.connect(self.qrcodeDialogShow)
        # 弹出的二维码窗口
        self.qrcodeDialog = QrcodeDialog()

    def initUser(self):
        # 设置厨师按钮不可用
        self.initButton.setDisabled(True)
        # 启动初始化线程
        getCookiesThread = threading.Thread(target=self.fastestSnatch.getCookies)
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
        if message['operation'] == 'open':
            # 获取二维码图片地址
            image_path = message['path']
            url_father = os.path.dirname(os.path.abspath(__file__))
            image_path = url_father + image_path
            # 加载图片
            labelPix = QLabel("show", self.qrcodeDialog)
            pic = QPixmap(image_path)
            labelPix.setPixmap(pic)
            # 打开对话框
            self.qrcodeDialog.verticalLayout.addWidget(labelPix)
            self.qrcodeDialog.show()
        # 关闭
        elif message['operation'] == 'close':
            self.initButton.setText(message['username'])
            self.qrcodeDialog.verticalLayout.itemAt(0).widget().deleteLater()
            self.qrcodeDialog.close()

    def closeEvent(self, a0: typing.Optional[QtGui.QCloseEvent]) -> None:
        self.qrcodeDialog.close()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fOoOtWindow = FOoOtWindow()
    fOoOtWindow.show()
    app.exec_()
