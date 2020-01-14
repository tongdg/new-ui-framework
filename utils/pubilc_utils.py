#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-12-06 Created by tongdg'


def str_to_list(string):
    if string.startswith('[') and string.endswith(']'):
        string = string[1:-1]
        lis = [s for s in string.split(',')]
        return lis
    else:
        return string

