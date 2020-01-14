#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-30 Created by tongdg'

# 填写格式
# flow = {路由名称: 所需要的参数}


# 通用数据
login = ['tong', '123456', '多租户空库0814', '童定国']
invoice_path = r'C:\Users\Administrator\Desktop\发票\fapiao\火车票\IMG_20190115_095242.jpg'
enclosure_path = r'C:\timg (5).jpg'

# pc 流程
login_flow = {'login': login, }

# 更多应用----待办
wait_deal_flow = {'login': login, 'wait_deal': ''}
already_deal_flow = {'login': login, 'already_deal': ''}
cc_task_flow = {'login': login, 'cc_task': ''}
all_task_flow = {'login': login, 'all_task': ''}
at_me_flow = {'login': login, 'at_me': ''}
my_concern_flow = {'login': login, 'my_concern': ''}
message_reminder_flow = {'login': login, 'message_reminder': ''}

# 更多应用----费用报销
add_pay_record_flow = {'login': login, 'add_pay_record': [invoice_path, enclosure_path]}
creat_flex_apply_bill_flow = {'login': login, 'creat_flex_apply_bill': ''}

#
all_wait_deal_flow = {
    'login': login,
    'wait_deal': '',
    'cc_task': '',
    'already_deal': '',
    'all_task': '',
    'at_me': '',
    'my_concern': '',
    'message_reminder': '',
}

# mobile 流程
mobile_login_flow = {'mobile_login': login, }


# 组装流程
pc_flow = [
    # login_flow,
    # wait_deal_flow,
    # already_deal_flow,
    # cc_task_flow,
    # all_task_flow,
    # my_concern_flow,
    # message_reminder_flow,
    # all_wait_deal_flow,
    add_pay_record_flow,
    creat_flex_apply_bill_flow,

]

mobile_flow = [
    mobile_login_flow,
]

# 控制流程的跑动
flow = [
    {'pc_flow': False},
    {'mobile_flow': True}
]

# 获取流程列表的属性
flow_list_locals = locals()


def get_flow_list_locals():
    return flow_list_locals






