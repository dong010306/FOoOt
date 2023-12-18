#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：FOoOt -> UtilsClass
@IDE    ：PyCharm
@Author ：Mr. Dong
@Date   ：2023/12/18 14:34
@Desc   ：
=================================================="""
import random
import threading
import time


class UtilsClass(object):
    def __init__(self):
        pass


# 定时执行线程类
class IntervalLoopThread(threading.Thread):
    def __init__(self, interval, func):
        super().__init__()
        self.running = True
        self.interval = interval
        # self.offset = offset
        self.func = func
        self.lock = threading.Lock()

    # 定时循环执行器
    def run(self):
        while self.running:
            start_time = time.monotonic()
            try:
                self.lock.acquire()
                self.func()
            except Exception as e:
                print(e)
                self.running = False
            finally:
                self.lock.release()
            end_time = time.monotonic()
            elapsed_time = end_time - start_time
            sleep_time = max(self.interval - elapsed_time, 0)
            # 随机变化
            # sleep_time = max(sleep_time + random.uniform(-1 * self.offset, self.offset), 0)
            time.sleep(sleep_time)

    def stop(self):
        self.running = False
