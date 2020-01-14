#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-29 Created by tongdg'

import unittest
from common.log import logger
from common.main_testing import MainTesting
from data import flow_list
import base64
from config import setting

flo_list = flow_list.get_flow_list_locals()


HTML_IMG_TEMPLATE = """
    <img src="data:image/png;base64, %s" width="%spx" height="%spx"/>
"""


class MyTest(unittest.TestCase):

    def setUp(self):
        logger.warning("=========================START=========================\n")
        logger.debug("测试用例开始执行:{}".format(self._testMethodName))
        flo = self._testMethodName.split("test_")[1]
        print(flo)
        self.flow_list = flo_list.get(flo)
        print(self.flow_list)

    def test_case(self):
        test = MainTesting(self.flow_list, setting.browser, 'pc')
        print(111111111)
        test.driver.get(setting.url)
        try:
            test.main(self.flow_list)
        except Exception as e:
            img_path = test.driver.save_screen_shot()
            with open(img_path, 'rb') as file:
                img = file.read()
            data = base64.b64encode(img).decode()
            # 记到日志里面展示
            logger.info(HTML_IMG_TEMPLATE % (data, 1000, 500))
            logger.error('Message: %s' % str(flow_list))
            logger.error(e)
            raise e
        finally:
            test.driver.quit()

    def tearDown(self):
        logger.debug("测试用例执行结束:{}".format(self._testMethodName))
        logger.warning("========================= END =========================\n")


class MyMobileTest(unittest.TestCase):

    def setUp(self):
        logger.warning("=========================START=========================\n")
        logger.debug("测试用例开始执行:{}".format(self._testMethodName))
        flo = self._testMethodName.split("test_")[1]
        print(flo)
        self.flow_list = flo_list.get(flo)
        print(self.flow_list)

    def test_case(self):
        test = MainTesting(self.flow_list, setting.browser, 'mobile')
        test.driver.get(setting.url)
        try:
            test.main(self.flow_list)
        except Exception as e:
            img_path = test.driver.save_screen_shot()
            with open(img_path, 'rb') as file:
                img = file.read()
            data = base64.b64encode(img).decode()
            # 记到日志里面展示
            logger.info(HTML_IMG_TEMPLATE % (data, 1000, 500))
            logger.error('Message: %s' % str(flow_list))
            logger.error(e)
            raise e
        finally:
            test.driver.quit()

    def tearDown(self):
        logger.debug("测试用例执行结束:{}".format(self._testMethodName))
        logger.warning("========================= END =========================\n")


if __name__ == '__main__':
    unittest.main()



