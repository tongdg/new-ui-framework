#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-27 Created by tongdg'


# 创建签名需要的字典
rpc_infp = {}
# in_: 接收传入类型，默认值为:()
# out: 接收返回类型，默认值为:(type(None),) 因为函数的返回值None，如果函数没有返回值
# 就不用传
# instance 判断是判断1个元素是不是2个元素的子类，第一个传的是对象，第二个传的是类型

urlpatterns = dict()


def xmlrpc(in_=(), out=(type(None),)):

    def _xmlrpc(function):
        # 注册签名
        func_name = function.__name__
        rpc_infp[func_name] = (in_, out)

        # 检查类型的子函数
        def _check_types(elements, types):
            if len(elements) != len(types):
                raise TypeError('argument count is wrong')
            typed = enumerate(zip(elements, types))
            # list(zip())->(1,2)(3,4)->[(1,3),(2,4)],要用list
            # print(list(zip(elements, types)))
            # print(list(typed)) 这里调试了过后要注释，不然回导致后续不能进入循环
            # list(enumerate(zip()))->(1,2)(3,4)->[(1,3),(2,4)]->[(0,(1,3)),(1,(2,4))]
            for index, couple in typed:
                arg, of_the_right_type = couple
                if isinstance(arg, of_the_right_type):
                    continue
                raise TypeError(
                    'arg #%d should be %s' % (index, of_the_right_type)
                )

        # 包装过的函数
        def __xmlrpc(*args):
            checkable_args = args[1:]
            _check_types(checkable_args, in_)
            res = function(*args)
            if not type(res) in (tuple, list):
                checkable_res = (res,)
            else:
                checkable_res = res
            _check_types(checkable_res, out)
            return res
        return __xmlrpc
    return _xmlrpc


