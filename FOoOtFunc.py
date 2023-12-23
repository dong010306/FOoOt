#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> FOoOtFunc
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/18 14:24
@Desc   ：
@Comment:写的太好了 太牛了
=================================================="""
import os
import sys
import threading

import typing

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QTextCursor
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
        self.fastestSnatch = FastestSnatch()
        # 控制台信号触发
        self.fastestSnatch.resultSignal.connect(self.refreshConsole)
        # 所有参数
        self.settings = {'requestMethod': None, 'url': None, 'interval': 0.0, 'startTime': None, 'endTime': None,
                         'XPath': None, 'params': {}, 'body': {}, 'headers': {}}
        # 抢夺触发按钮回调
        # 启动
        self.startButton.clicked.connect(self.start)
        # 停止
        self.stopButton.clicked.connect(self.stop)

    def getSettings(self):
        tempInterval = self.intervalTime.currentText()
        if tempInterval == '1ms':
            self.settings['interval'] = 0.001
        elif tempInterval == '5ms':
            self.settings['interval'] = 0.005
        elif tempInterval == '10ms':
            self.settings['interval'] = 0.01
        elif tempInterval == '100ms':
            self.settings['interval'] = 0.1
        elif tempInterval == '500ms':
            self.settings['interval'] = 0.5
        elif tempInterval == '1s':
            self.settings['interval'] = 1

    def refreshConsole(self, content):
        # 插入控制台
        self.plainTextEdit.insertPlainText(content + '\n')
        # 滚动条移动到最下方
        self.plainTextEdit.moveCursor(QTextCursor.End)

    def start(self):
        # 获取所有设置
        self.getSettings()
        # 加载所有设置
        self.fastestSnatch.updateSettings(self.settings)
        # 清空控制台
        self.plainTextEdit.clear()
        # 启动定时器
        self.fastestSnatch.jobStart()

    def stop(self):
        # 停止定时器
        self.fastestSnatch.jobPause()

    def closeEvent(self, a0: typing.Optional[QtGui.QCloseEvent]) -> None:
        # 停止定时器
        self.stop()
        # 退出程序
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fOoOtWindow = FOoOtWindow()
    fOoOtWindow.show()
    app.exec_()
