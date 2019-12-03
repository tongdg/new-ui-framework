#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-27 Created by tongdg'

import os

# 工程根路径
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
# 日志目录
LOG_PATH = os.path.join(BASE_PATH, 'log')
# 报告目录
REPORT_PATH = os.path.join(BASE_PATH, 'report')
# 驱动目录
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
# 工作目录
UTILS_PATH = os.path.join(BASE_PATH, 'utils')
# 测试企业名称
TEST_ENTERPRISE = '多租户空库0814'
# 测试报告里面的名称
REPORT_CASE_NAME = '必维自动化测试报告'
# 测试报告的名称
REPORT_NAME = 'BW_TestResult'

# local chrome  本地驱动和远程驱动设置
DRIVER_MODE = 'local'
DRIVER_URL = 'http://192.168.61.3'
DRIVER_PORT = '5555'

# 测试环境 http://117.50.100.99
# 正式环境 http://app.yuanian.com
url = 'http://app.yuanian.com'

# 设置超时上线值
TIMEOUT = 10
# 设置间隔时间
INTERVAL_TIME = 0.1


# 设置测试浏览器
browser = 'chrome'

DEFAULT_MESSAGE_DURATION = 5



# 设置高亮次数
HIGHLIGHTS = 4

# 移动端设置

# 常用元素按钮定位xpath
TEXT_XPATH = "//*[text()='%s']"






