#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> QrcodeFunc
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/18 17:38
@Desc   ：
=================================================="""
from PyQt5.QtWidgets import QDialog

from Qrcode import Ui_Dialog


class QrcodeDialog(Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        # 初始化UI
        self.setupUi(self)
