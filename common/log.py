#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-27 Created by tongdg'

import logging
import os
import time
from config.setting import LOG_PATH


class Log:
    def __init__(self, path=LOG_PATH):
        # 文件命名
        self.log_path = path
        self.logname = os.path.join(self.log_path, '%s.log' % time.strftime("%Y-%m-%d"))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # 日志输出格式
        self.formatter = self.formatter = logging.Formatter('[%(asctime)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a') # a 追加模式
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    # 很巧妙的二次封装
    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


logger = Log()

if __name__ == '__main__':
    log = Log()
    log.info("---测试开始----")
    log.info("输入密码")
    log.warning("----测试结束----")







