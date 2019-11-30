#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-30 Created by tongdg'

# 填写格式
# flow = {路由名称: 所需要的参数}
#
#

# 通用数据
login = ['tong', '123456', '多租户空库0814', '童定国']


# pc 流程
login_flow = {'login': login, }
wait_deal_flow = {'login': login, 'wait_deal': ''}
already_deal_flow = {'login': login, 'already_deal': ''}


# mobile 流程
mobile_login_flow = {'mobile_login': login, }


# 组装流程
pc_flow = [
    login_flow,
    wait_deal_flow,
    already_deal_flow,
]

mobile_flow = [
    mobile_login_flow,
]

# 控制流程的跑动
flow = [
    {'pc_flow': True},
    {'mobile_flow': True}
]

# 获取流程列表的属性
flow_list_locals = locals()


def get_flow_list_locals():
    return flow_list_locals






