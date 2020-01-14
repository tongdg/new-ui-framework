#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-29 Created by tongdg'


from functools import wraps
from common.own_error import InitError
from common.page import Page
from data.flow_list import pc_flow
from utils import pubilc_utils
from common.decorator import urlpatterns

# 将url与方法绑定
def router(urlk):
    def fool(func):
        if urlk in urlpatterns.keys():
            raise Exception('url to the repeated: %s' % urlk)
        urlpatterns[urlk] = func
        @wraps(func)
        def test(*args, **kwargs):
            return func(*args, **kwargs)
        return test
    return fool


class MainTesting(object):
    data_pool = dict()

    def __init__(self, flow_list, browser, dev='pc'):
        if dev.lower() == 'pc':
            # 导入的同时，执行了init文件的代码，把相应的模块加到了sys.modules
            from pages import pc
            import sys
            self.DEV = 'pc'
        elif dev.lower() == 'mobile':
            from pages import mobile
            self.DEV = 'mobile'
        else:
            raise InitError('Invalid dev, dev is \'pc\' or \'mobile\'')
        self.driver = Page(browser_type=browser, dev=dev)
        self.flow_list = flow_list

    def main(self, flow):
        for key in flow.keys():
            if key in urlpatterns.keys():
                n_self = self._get_ins(urlpatterns[key])
                if isinstance(flow[key], str):
                    if flow[key] == '':
                        urlpatterns[key](n_self, )
                    else:
                        urlpatterns[key](n_self, pubilc_utils.str_to_list(flow[key]))
                else:
                    urlpatterns[key](n_self, *flow[key])

    def _get_ins(self, func):
        m = __import__(name=func.__module__, fromlist=['pc', 'mobile'])
        for a in dir(m):
            attr = getattr(m, a)
            if type(attr) == type and issubclass(attr, MainTesting) and hasattr(attr, func.__name__):
                ins = attr(self.flow_list, self.driver.type, self.DEV).set_driver(self.driver)
                return ins
        # return self

    def set_driver(self, driver):
        self.driver = driver
        return self

    # 前置步骤，继承即可
    def pre_operation(self):
        pass

    # 后置步骤，继承即可
    def pos_operation(self):
        pass


if __name__ == '__main__':
    test = MainTesting(flow_list=pc_flow, browser='chrome', )
    print(urlpatterns)




