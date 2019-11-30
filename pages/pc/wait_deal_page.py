#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-30 Created by tongdg'

from common.main_testing import MainTesting
from common.main_testing import router


class WaitDealPage(MainTesting):

    def pre_operation(self):
        self.driver.move_to('#tabmore')
        self.driver.click('待办')

    @router(r'wait_deal')
    def wait_deal(self):
        self.pre_operation()
        mark = self.driver.find_elements(
            '#root > div > section > section > section > main > section > '
            'section > main > section > main > div > div.components-todo-formcontent__'
            'record_lists--29V_wNCX')
        assert mark

    @router(r'already_deal')
    def already_deal(self):
        self.pre_operation()
        self.driver.click('已办任务')
        mark = self.driver.find_elements(
            '#root > div > section > section > section > main > section > section > main > section > main > div >'
            ' div.components-todo-formcontent__record_lists--29V_wNCX > div > div'
        )
        assert mark







