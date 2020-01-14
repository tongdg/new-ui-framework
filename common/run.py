#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-30 Created by tongdg'

# 解决jenkins部署需要配置PYTHONPATH的问题
import sys
from config.setting import BASE_PATH
sys.path.append(BASE_PATH)
# ---------------------------------
from common.my_test import MyTest, MyMobileTest
from data import flow_list
import unittest
from utils import BeautifulReport
import time
from config.setting import LOG_PATH, REPORT_PATH
from config import setting
import os


TEST_CLS = {
    'pc_flow': MyTest,
    'mobile_flow': MyMobileTest,
}


# 非常巧妙的处理
def load_case(suite):
    """装载测试用例"""
    # 这里在装载的时候，通过改变测试用例的名字
    # 可以实现1.装载相同的测试用例
    # 2.多个测试用例调用的一个执行方法test_case
    # 3.所有的name对应的都是test_case
    def set_case(cls, name, remark):
        setattr(cls, name, cls.test_case)
        testcase = getattr(cls, name)
        testcase.__doc__ = remark
        print(name)
        suite.addTest(cls(name))

    # 获取flow_list的属性
    flow_list_locals = flow_list.get_flow_list_locals()

    # 组装测试用例
    for control_flow in flow_list_locals.get('flow'):
        for key in control_flow.keys():
            if control_flow[key]:
                flow_lis = flow_list_locals.get(key)
                if flow_lis is None:
                    return
                for flo in flow_lis:
                    for loacl_key in flow_list_locals.keys():
                        if flow_list_locals[loacl_key] == flo:
                            test_case_name = "test_%s" % loacl_key
                            set_case(TEST_CLS[key], test_case_name, remark=test_case_name)


def get_report_name(name='TestResult'):
    """生成Report Name"""
    now = time.strftime('%Y%m%d_%H%M%S')
    return '%s%s.html' % (name, now)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    load_case(suite)
    test_report = os.path.join(REPORT_PATH, 'testReport')
    if not os.path.exists(test_report):
        os.makedirs(test_report)
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    # result = BeautifulReport.BeautifulReport(suite)
    # result.report(setting.REPORT_CASE_NAME, get_report_name(), LOG_PATH, test_report)
    unittest.TextTestRunner().run(suite)


