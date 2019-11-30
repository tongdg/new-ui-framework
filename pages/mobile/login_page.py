#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-29 Created by tongdg'

from common.main_testing import MainTesting
from common.main_testing import router


class MobileLoginPage(MainTesting):

    @router(r'mobile_login')
    def login(self, username, password, enterprise, assert_value):
        self.driver.send_keys('#loginName', username)
        self.driver.send_keys('#pwd', password)
        self.driver.click('#components-form-demo-normal-login > form '
                          '> div:nth-child(4) > div > div > span > button')
        self.driver.click(enterprise)
        self.driver.click('#root > div > div > div.home_tabbar___2b8uE '
                          '> div > div > div > div > div:nth-child(3) > p')
        mark = self.driver.get_element_text(
            self.driver.find_elements('#root > div > div > div.content___ItU_U > div.top___3gs4z > div.am-list.'
                                      'avatar___1dflk > div > div > div.am-list-line.am-list-line-multiple >'
                                      ' div.am-list-content')
        )
        assert assert_value in mark




