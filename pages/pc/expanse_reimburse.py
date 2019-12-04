#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-12-03 Created by tongdg'

from common.main_testing import MainTesting,router


class ExpanseReimburse(MainTesting):

    def pre_operation(self):
        self.driver.move_to('#tabmore')
        self.driver.click('费用报销')
        self.driver.switch_to_frame('tag=iframe')

    @router(r'add_pay_record')
    def add_pay_record(self, invoice_path, enclosure_path):
        self.pre_operation()

        self.driver.click('我的支出记录')
        self.driver.move_to('新增支出记录')
        self.driver.click('上传发票')
        self.driver.upload_file(invoice_path)
        self.driver.wait_element_change_display('Loading...')
        assert self.driver.find_elements('识别成功', time_out=2)
        self.driver.move_to('生成支出记录')
        if self.driver.find_elements('汇总生成', time_out=3):
            self.driver.click('汇总生成')
        else:
            self.driver.click('逐条生成')
        self.driver.click('输入支出类型')
        self.driver.click('客户招待费用')
        # self.driver.send_keys('#AMOUNT', 50)
        self.driver.send_keys('#DEF_KHRS_005', 2)
        self.driver.send_keys('#DEF_BWYGRS_010', 1)
        self.driver.send_keys('#DEF_KHMC_006', '测试添加支出记录！')
        self.driver.js_click('增加附件')
        self.driver.upload_file(enclosure_path)
        self.driver.js_click('保 存')
        assert self.driver.find_elements('保存成功！', time_out=2)
        # 还原数据
        self.driver.click('删除')
        self.driver.click('确 定')
        assert self.driver.find_elements('删除成功！')
        self.driver.click('待处理发票')
        self.driver.click('删除发票')
        self.driver.click('确 定')
        assert self.driver.find_elements('删除成功！')

    @router(r'creat_flex_apply_bill')
    def creat_flex_apply_bill(self):
        self.pre_operation()
        self.driver.click('我的申请')
        self.driver.move_to('创建申请单')
        self.driver.click('FLEX账号申请表')
        self.driver.send_keys('#editor > div > div > div > div:nth-child(3) > div:nth-child(1) > div > div > div > '
                              'span.field_control > div > input', '测试人员')
        self.driver.send_keys('#editor > div > div > div > div:nth-child(3) > div:nth-child(2) > div > div > div > '
                              'span.field_control > div > input', 'SFID')
        self.driver.click('#editor > div > div > div > div:nth-child(3) > div:nth-child(3) > div > div > div > '
                          'span.field_control > div > span > span > span.ant-select-selection__rendered')
        self.driver.click('AP Manger')
        self.driver.click('#editor > div > div > div > div:nth-child(4) > div:nth-child(1) > div > div > div > '
                          'span.field_control > div > span')
        self.driver.click('HK')
        self.driver.send_keys('#editor > div > div > div > div:nth-child(4) > div:nth-child(2) > div > div > div > '
                              'span.field_control > div > input', '直属经理')
        self.driver.send_keys('#editor > div > div > div > div:nth-child(4) > div:nth-child(3) > div > div > div > '
                              'span.field_control > div > input','892431872@qq.com')
        self.driver.click('提交')










