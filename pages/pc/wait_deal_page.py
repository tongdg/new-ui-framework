#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-30 Created by tongdg'

from common.main_testing import MainTesting
from common.main_testing import router


class WaitDealPage(MainTesting):

    # 前置操作
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

    @router(r'cc_task')
    def cc_task(self):
        self.pre_operation()
        self.driver.click('抄送任务')
        mark = self.driver.find_elements(
            '#root > div > section > section > section > main > section > section > main > section > main > div > div'
        )
        assert mark

    @router(r'all_task')
    def all_task(self):
        self.pre_operation()
        self.driver.click('全部任务')
        mark = self.driver.find_elements(
            '#root > div > section > section > section > main > section > section > main > section > main > div > '
            'div.components-todo-formcontent__record_lists--29V_wNCX'
        )
        assert mark

    @router(r'at_me')
    def at_me(self):
        self.pre_operation()
        self.driver.click('@我的')
        mark = self.driver.find_elements(
            '#root > div > section > section > section > main > section > section > main > section > main > div'
        )
        assert mark

    @router('my_concern')
    def my_concern(self):
        self.pre_operation()
        self.driver.click('我关注的')
        mark = self.driver.find_elements(
            '#root > div > section > section > section > main > section > section > main > section > main > div > div'
        )
        assert mark

    @router('message_reminder')
    def message_reminder(self):
        self.pre_operation()
        self.driver.click('消息提醒')
        mark = self.driver.find_elements(
            '#root > div > section > section > section > main > section > section > main > section > main > div '
            '> div > div'
        )
        assert mark











