#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-29 Created by tongdg'

from common.main_testing import MainTesting
from common.main_testing import router


class LoginPage(MainTesting):

    @router(r'login')
    def login(self, usrname, password, enterprise, assert_value):
        self.driver.send_keys('#loginName', usrname)
        self.driver.send_keys('#pwd', password)
        self.driver.click('登 录')
        self.driver.click(enterprise)
        mark = self.driver.get_attribute(selector='#components-layout-top > ul > li:nth-child(4) > div > span',
                                         attr='title')
        assert mark in assert_value












