#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'2019-11-26 Created by tongdg'


class UnSupportBrowserTypeError(Exception):
    pass


class UnSupportDriverModeError(Exception):
    pass


class SendKeysNoneError(Exception):
    pass


class ClickElementTooMuchError(Exception):
    pass


class InitError(Exception):
    pass

class AlterSheetError(Exception):
    pass