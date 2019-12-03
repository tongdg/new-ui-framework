#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-26 Created by tongdg'

from selenium.webdriver.common.by import By
from common.browser import Browser
from utils import page_utils
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from config import setting
from common.log import logger
from selenium.webdriver.remote.command import Command
from common.own_error import SendKeysNoneError
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import win32con
import win32gui
from seleniumbase.fixtures import js_utils


class Page(Browser):

    def find_elements(self, selector, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT, ):
        _selector = selector
        selector, by = self.__recalculate_selector(selector, by)
        logger.debug("find elements:(%s, %s)" % (by, selector))
        try:
            self.driver_wait(selector, time_out, by)
        except Exception as e:
            logger.error('find elements:(%s, %s) error, info: %s.' % (by, selector, e))
            return False
        web_elements = self.driver.find_elements(by, selector)
        if len(web_elements) == 1:
            self.execute("arguments[0].focus();", web_elements[0])
            if 'tag=iframe' != _selector:
                self.alter_attribute('style', 'border: 2px solid red;', web_elements[0])
            return web_elements[0]
        else:
            return web_elements

    def __unpack(self, *args):
        if isinstance(args[0], WebElement):
            web_element = args[0]
        else:
            web_element = self.find_elements(*args)
        return web_element

    def click(self, selector, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT,):
        """通过js进行元素点击"""
        web_elements = self.__unpack(selector, by, time_out)
        if not web_elements:
            raise TimeoutError('find element error!')
        web_element = None
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        if self.type == "ie":
            self.driver.execute(Command.W3C_CLEAR_ACTIONS)
            self.execute("arguments[0].click();", web_element)
        else:
            try:
                web_element.click()
            except Exception as e:
                self.execute("arguments[0].click();", web_element)
                logger.info('click error %s.' % e)
        logger.info("click element: %s" % selector)

    # 解决click点击无效，不报错的问题
    def js_click(self, selector, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT,):
        web_elements = self.__unpack(selector, by, time_out)
        if not web_elements:
            raise TimeoutError('find element error!')
        web_element = None
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        self.execute("arguments[0].click();", web_element)
        logger.info("click element: %s" % selector)

    def move_to(self, selector, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT, ):
        web_elements = self.__unpack(selector, by, time_out)
        if not web_elements:
            raise TimeoutError('find element error!')
        web_element = None
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        """鼠标在指定元素悬停"""
        action = ActionChains(self.driver)
        action.reset_actions()
        if self.type == 'ie':
            x = web_element.location['x']
            y = web_element.location['y']
            # self.driver.get_window_size()
            # action.w3c_actions.pointer_inputs[0].clear_actions()
            action.move_by_offset(x, y).perform()
        else:
            action.move_to_element(web_element).perform()
        logger.info("click element: %s" % selector)

    def send_keys(self, selector, text, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT, ):
        if text is None:
            raise SendKeysNoneError('Please input your text.')
        web_elements = self.__unpack(selector, by, time_out)
        if not web_elements:
            raise TimeoutError('find element error!')
        web_element = None
        if isinstance(web_elements, list):
            web_element = web_elements[0]
        else:
            web_element = web_elements
        self.wait(0.5)
        if self.is_displayed(web_element):
            web_element.clear()
        if self.type == "ie":
            text = str(text)
            for i in text:
                web_element.send_keys(i)
        else:
            web_element.send_keys(str(text))
        logger.info("send keys to element: %s value: %s" % (selector, text))

    def get_attribute(self, selector, attr, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT):
        logger.debug("get attributes to element:(%s, %s) name: %s" % (by, selector, attr))
        try:
            web_element = self.__unpack(selector, by, time_out)
            return getattr(web_element, attr) if hasattr(web_element, attr) else web_element.get_attribute(attr)
        except Exception:
            return ''

    def get_attributes(self, selector, attr, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT):
        values = []
        logger.debug("get attributes to element:(%s, %s) name: %s" % (by, selector, attr))
        web_elements = self.__unpack(selector, by, time_out)
        for web_element in web_elements:
            try:
                values.append(getattr(web_element, attr) if hasattr(web_element, attr) else web_element.get_attribute(attr))
            except Exception:
                values.append('')
        return values

    def is_displayed(self, web_element):
        return web_element.is_displayed()

    def switch_to_frame(self, selector, by=By.CSS_SELECTOR, time_out=setting.TIMEOUT):
        web_element = self.__unpack(selector, by, time_out)
        self.driver.switch_to.frame(web_element)
        logger.info("switch to frame: {}".format(selector))

    def switch_to_parent_frame(self):
        """切换回上一级iframe表单"""
        self.driver.switch_to.parent_frame()
        logger.info("switch to parent frame.")

    def execute(self, js, *args):
        """执行js"""
        self.driver.execute_script(js, *args)
        logger.debug("execute javascript: %s" % js)

    def alter_attribute(self, name, value, web_element):
        if name == 'style':
            js = "arguments[0].setAttribute('style', '%s');" % value
        else:
            js = "arguments[0].%s = '%s';" % (name, value)
        self.execute(js, web_element)

    def driver_wait(self, selector, time_out=setting.TIMEOUT, by=By.CSS_SELECTOR, ):
        logger.info('driver_wait %s.' % time_out)
        WebDriverWait(self.driver, time_out).until(expected_conditions.presence_of_element_located((by, selector)))

    def __recalculate_selector(self, selector, by):
        # Try to determine the type of selector automatically
        if page_utils.is_xpath_selector(selector):
            by = By.XPATH
            return selector, by
        elif page_utils.is_link_text_selector(selector):
            selector = page_utils.get_link_text_from_selector(selector)
            by = By.LINK_TEXT
            return selector, by
        elif page_utils.is_partial_link_text_selector(selector):
            selector = page_utils.get_partial_link_text_from_selector(selector)
            by = By.PARTIAL_LINK_TEXT
            return selector, by
        elif page_utils.is_name_selector(selector):
            name = page_utils.get_name_from_selector(selector)
            selector = '[name="%s"]' % name
            by = By.CSS_SELECTOR
            return selector, by

        elif page_utils.is_tag_selector(selector):
            tag = page_utils.get_tag_name_from_selector(selector)
            selector = tag
            by = By.TAG_NAME
            return selector, by

        elif by == By.LINK_TEXT or by == By.PARTIAL_LINK_TEXT:
            if self.browser == "safari" and selector.lower() != selector:
                selector = ("""//a[contains(translate(.,"ABCDEFGHIJKLMNOPQR"""
                            """STUVWXYZ","abcdefghijklmnopqrstuvw"""
                            """xyz"),"%s")]""" % selector.lower())
                by = By.XPATH
                return selector, by
        # 现在仅支持#和.开头的CSS检索
        elif not page_utils.is_css_selector(selector):
            selector = setting.TEXT_XPATH % selector
            by = By.XPATH
            return selector, by

        else:
            return selector, by

    # 等待元素消失
    def wait_element_disapper(self, selector, interval_time=setting.INTERVAL_TIME,
                              by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        logger.info('wait (%s, %s) begin.' % (by, selector))
        all_time = 0
        try:
            while self.driver.find_element(by, selector):
                self.wait(interval_time)
                all_time = all_time + interval_time
                if all_time >= 5:
                    logger.info('wait (%s, %s, %f) timeout.' % (by, selector, all_time))
                    break
        except NoSuchElementException:
            logger.info('wait (%s, %s) end.' % (by, selector))
        except StaleElementReferenceException:
            logger.info('wait (%s, %s) end.' % (by, selector))

    # 元素没有消失，等待元素的display值由True变为False,或者由False变为True
    def wait_element_change_display(self, selector, interval_time=setting.INTERVAL_TIME,
                                   by=By.CSS_SELECTOR):
        selector, by = self.__recalculate_selector(selector, by)
        logger.info('wait (%s, %s) begin.' % (by, selector))
        all_time = 0
        self.wait(0.5)
        self.driver_wait(selector=selector, by=by, time_out=5)
        if self.is_displayed(self.driver.find_element(by, selector)) is True:
            while self.is_displayed(self.driver.find_element(by, selector)) is True:
                self.wait(interval_time)
                all_time = all_time + interval_time
                if all_time >= 5:
                    logger.info('wait (%s, %s, %f) true timeout.' % (by, selector, all_time))
                    break
        else:
            while self.is_displayed(self.driver.find_element(by, selector)) is False:
                self.wait(interval_time)
                all_time = all_time + interval_time
                if all_time >= 5:
                    logger.info('wait (%s, %s, %f) false timeout.' % (by, selector, all_time))
                    break
        logger.info('wait (%s, %s) end.' % (by, selector))

    # 元素没有消失，等待元素的属性值改变,默认获取元素的文本属性值
    def wait_element_change_attr(self, selector, attr_value, interval_time=setting.INTERVAL_TIME,
                                   by=By.CSS_SELECTOR, attr='text', ):
        selector, by = self.__recalculate_selector(selector, by)
        logger.info('wait (%s, %s, %s) begin.' % (by, selector, attr_value))
        all_time = 0
        self.driver_wait(selector=selector, by=by, time_out=5)
        while self.get_attribute(selector=self.driver.find_element(by, selector), attr=attr) in attr_value:
            self.wait(interval_time)
            all_time = all_time + interval_time
            if all_time >= 5:
                logger.info('wait (%s, %s, %f) timeout.' % (by, selector, all_time))
                break
        logger.info('wait (%s, %s, %s) end.' % (by, selector, attr_value))

    def upload_file(self, path):
        """上传附件"""
        self.wait(2)
        dialog = win32gui.FindWindow('#32770', u'打开')  # 识别对话框句柄
        combo_box_ex32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        combo_box = win32gui.FindWindowEx(combo_box_ex32, 0, 'ComboBox', None)
        edit = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)  # 找到输入框Edit对象的句柄
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 找到按钮Button
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, path)  # 往输入框输入绝对地址
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
        logger.info("upload file: %s" % path)


if __name__ == '__main__':

    page = Page()
    page.get('http://app.yuanian.com')
    page.send_keys('//*[@id="loginName"]', 'tong')
    page.send_keys('#pwd', '123456')
    page.click('#components-form-demo-normal-login > form > div:nth-child(4) > div > div > span > button')
    page.click('多租户空库0814')
    page.move_to('#tabmore')
    page.click('费用报销')
    page.switch_to_frame('tag=iframe')
    page.click('我的支出记录')
    page.move_to('新增支出记录')
    page.click('上传发票')
    page.upload_file(r'C:\Users\Administrator\Desktop\发票\fapiao\机打\机打票_采购.jpg')
    page.wait_element_change_display('Loading...')
    assert page.find_elements('识别成功', 1)
    page.move_to('生成支出记录')
    page.click('逐条生成')
    page.click('输入支出类型')
    page.click('客户招待费用')
    page.send_keys('#DEF_KHRS_005', 2)
    page.send_keys('#DEF_BWYGRS_010', 1)
    page.wait(1)
    page.js_click('增加附件')
    page.upload_file(r'C:\Users\Administrator\Desktop\发票\fapiao\机打\机打票_采购.jpg')
    page.send_keys('#DEF_KHMC_006', 'sdfsdafsadfsd')
    page.js_click('保 存')

















