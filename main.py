#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> main
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/23 22:26
@Desc   ：
=================================================="""
import sys

from PyQt5.QtWidgets import QApplication, QWidget

from FOoOtFunc import FOoOtWindow
from FOoOtLoginFunc import FOoOtLoginWindow


class Dispatch(QWidget):
    """
    调度类
    """

    def __init__(self):
        super(Dispatch, self).__init__()
        # 认证类
        self.identity = None
        # 登陆窗口
        self.fOoOtLoginWindow = None
        # 主窗口
        self.fOoOtWindow = None
        # 启动登陆
        self.login()

    def login(self):
        self.fOoOtLoginWindow = FOoOtLoginWindow()
        # 连接主要窗口信号
        self.fOoOtLoginWindow.loginSignal.connect(self.fOoOt)
        # 显示窗口
        self.fOoOtLoginWindow.show()

    def fOoOt(self):
        # 认证类转移
        self.identity = self.fOoOtLoginWindow.identity
        # 主窗口显示
        self.fOoOtWindow = FOoOtWindow()
        self.fOoOtWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dispatch = Dispatch()
    app.exec_()
