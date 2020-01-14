#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-27 Created by tongdg'

import time
from selenium import webdriver
from config.setting import DRIVER_PATH
from common.own_error import UnSupportBrowserTypeError, UnSupportDriverModeError
from common.log import logger
from common.decorator import xmlrpc
from config import setting
import os

PHANTOMJSDRIVER_PATH = DRIVER_PATH + r'\phantomjs.exe'
FIREFOXDRIVER_PATH = DRIVER_PATH + r'\geckodriver.exe'
CHROMEDRIVER_PATH = DRIVER_PATH + r'\chromedriver.exe'
EDGEDRIVER_PATH = DRIVER_PATH + r'\MicrosoftWebDriver.exe'
IEDRIVER_PATH = DRIVER_PATH + r'\IEDriverServer.exe'

TYPES = {'phantomjs': webdriver.PhantomJS,
         'firefox': webdriver.Firefox,
         'chrome': webdriver.Chrome,
         'edge': webdriver.Edge,
         'ie': webdriver.Ie}

OPTIONS_PATH = {'firefox': webdriver.FirefoxOptions,
                'chrome': webdriver.ChromeOptions,
                'ie': webdriver.IeOptions,
                }
EXECUTABLE_PATH = {'phantomjs': PHANTOMJSDRIVER_PATH,
                   'firefox': FIREFOXDRIVER_PATH,
                   'chrome': CHROMEDRIVER_PATH,
                   'edge': EDGEDRIVER_PATH,
                   'ie': IEDRIVER_PATH}

chrome_arguments = [
    # '--headless',  # 谷歌无头模式
    '--disable-gpu',  # 谷歌文档提到需要加上这个属性来规避bug
    'disable-infobars',  # 隐藏"Chrome正在受到自动软件的控制"
    'lang=zh_CN.UTF-8',  # 设置成中文
    # 'blink-settings=imagesEnabled=false',  # 提升速度
]

# 以iPhone X的模式打开浏览器
chrome_mobileEmulation = {
    'deviceName': 'iPhone X'
}


OPTIONS = {
    'chrome_options': {
        # 启动参数
        'arguments': chrome_arguments,
        # 设置模拟器打开
        'mobileEmulation': chrome_mobileEmulation
    },
}


class Browser(object):

    def __init__(self, dev='pc', browser_type='chrome'):
        self.type = browser_type.lower()
        if self.type in TYPES:
            self.browser = TYPES[self.type]
        else:
            raise UnSupportBrowserTypeError('仅支持: %s!' % ', '.join(TYPES.keys()))
        self.driver = None
        self.options = None
        self.dev = dev
        self.browser_type = browser_type

    def get(self, url, maximize_window=True, implicitly_wait=30):
        self._set_driver()
        self.driver.get(url)
        if maximize_window:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        logger.info("open the page: %s" % self.current_url)
        return self  # returen self 可以继续调用别的方法 很巧妙

    def _set_driver(self):
        if self.type == 'chrome':
            self.set_options(OPTIONS)
            if setting.DRIVER_MODE == 'local':
                self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], chrome_options=self.options, )
            elif setting.DRIVER_MODE == 'remote':
                self.driver = webdriver.Remote(
                    command_executor='%s:%s/wd/hub' % (setting.DRIVER_URL, setting.DRIVER_PORT),
                    desired_capabilities={
                        'platform': 'ANY',
                        'browserName': self.type,
                        'version': '',
                        'javascriptEnabled': True,
                    }
                )
            else:
                raise UnSupportBrowserTypeError('%s,错误的驱动模式，请在setting中配置DRIVER_MODE的值为remote或者local!' % setting.DRIVER_MODE)
        elif self.type == 'firefox':
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], firefox_options=self.options, )
        elif self.type == 'ie':
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], ie_options=self.options, )
        else:
            self.driver = self.browser(executable_path=EXECUTABLE_PATH[self.type], )

    @xmlrpc(in_=(dict, ))
    def set_options(self, options):
        if self.options is None:
            if self.type in OPTIONS_PATH:
                self.options = OPTIONS_PATH[self.type]()
            else:
                raise UnSupportBrowserTypeError('提供配置支持的浏览器: %s!' % ', '.join(OPTIONS_PATH.keys()))
        if self.type == 'chrome':
            _browser = "%s_%s" % (self.type, 'options')
            # 添加参数
            [self.options.add_argument(argument) for argument in options[_browser]['arguments']]
            # 移动端设置
            if self.dev == 'mobile':
                self.options.add_experimental_option('mobileEmulation', options[_browser]['mobileEmulation'])

    @property
    def current_url(self):
        current_url = self.driver.current_url
        return current_url

    @property
    def title(self):
        title = self.driver.title
        logger.info("get current page title: %s" % title)
        return title

    def wait(self, seconds=1):
        time.sleep(seconds)
        logger.info("wait %f seconds" % seconds)

    def get_driver(self):
        return self.driver

    def quit(self):
        logger.info("quit browser")
        self.driver.quit()


    def close(self):
        self.driver.close()
        logger.info("close the current page: %s" % self.current_url)

    def refresh(self):
        self.driver.refresh()
        logger.info("page refresh: %s" % self.current_url)

    def forward(self):
        self.driver.forward()
        logger.info("page forward to the: %s" % self.current_url)

    def back(self):
        self.driver.back()
        logger.info("page back to the: %s" % self.current_url)

    def get_source(self):
        logger.info("page soure to the: %s" % self.current_url)
        return self.driver.page_source

    def get_title(self):
        logger.info("page title to the: %s" % self.current_url)
        return self.driver.title

    @property
    def current_window(self):
        handle = self.driver.current_window_handle
        logger.info("get current page handle: %s" % handle)
        return handle

    def switch_to_window(self, partial_url='', partial_title=''):
        """切换窗口
            如果窗口数<3,不需要传入参数，切换到当前窗口外的窗口；
            如果窗口数>=3，则需要传入参数来确定要跳转到哪个窗口
        """
        all_windows = self.driver.window_handles
        if len(all_windows) == 1:
            logger.warning('只有1个window!')
        elif len(all_windows) == 2:
            other_window = all_windows[1 - all_windows.index(self.current_window)]
            self.driver.switch_to.window(other_window)
        else:
            for window in all_windows:
                self.driver.switch_to.window(window)
                if partial_url in self.current_url or partial_title in self.title:
                    break
        logger.info("switch window to the: %s" % self.current_url)

    def save_screen_shot(self, name='screen_shot'):
        """截图"""
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_path = setting.REPORT_PATH + r'\screenshot_%s' % day
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        tm = time.strftime('%H%M%S', time.localtime(time.time()))
        screenshot = self.driver.save_screenshot(screenshot_path + '\\%s_%s.png' % (name, tm))
        logger.info("capture page images: %s" % screenshot_path + '\\%s_%s.png' % (name, tm))
        return screenshot_path + r'\%s_%s.png' % (name, tm)


if __name__ == '__main__':
    browser = Browser()
    browser.wait()
    browser.get('http://www.baidu.com')
















