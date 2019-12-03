# -*- coding:utf-8 -*-
# Author: 朱尧
# Group: 武汉测试中心
# email: zhuy@yuanian.com, zzyyhshs@163.com

import win32api
import win32con


def mouse_left(x, y):
    """
    模拟鼠标移动到指定位置左击
    """
    win32api.SetCursorPos((int(x), int(y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def mouse_right(x, y):
    """
    模拟鼠标移动到指定位置右击
    """
    win32api.SetCursorPos((int(x), int(y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def mouse_move(x, y):
    """
    只移动鼠标不进行点击
    """
    win32api.SetCursorPos((int(x), int(y)))


"""
键　　 键码　  　键　　 键码　　　 键　　 键码 　　  键　　　　      键码
A　　　65　　   0 　　  96 　　　　F1 　　112 　　  Backspace 　　　8
B　　　66　　   1　　   97 　　　　F2 　　113　　   Tab 　　　　　　9
C　　　67 　　  2 　　  98 　  　　F3 　　114　　   Clear 　　　　　12
D　　　68　　　 3　　   99 　　　　F4 　　115　　   Enter 　　　　　13
E　　　69 　　  4 　　  100　　　　F5 　　116　　   Shift　　　　　 16
F　　　70 　　  5 　　  101　　　　F6 　　117　　   Control 　　　　17
G　　　71 　　  6　　   102　　　　F7 　　118 　　  Alt 　　　　　　18
H　　　72 　　　7 　　  103　 　　 F8 　　119　　   Caps Lock 　　　20
I　　　73 　　　8 　　  104　　　　F9 　　120　　   Esc 　　　　　　 27
J　　　74 　　　9　　   105　　　　F10　　121　　   Spacebar　　　　 32
K　　　75 　　　* 　　  106　  　　F11　　122　　   Page Up　　　　  33
L　　　76 　　　+ 　　  107　　  　F12　　123　　   Page Down 　　　 34
M　　　77 　　　Enter   108　　　　-- 　　--　　　  End 　　　　　　 35
N　　　78 　　　-　　   109　　　　-- 　　-- 　　　 Home　　　　　　 36
O　　　79 　　　. 　　  110　　　　--　　 -- 　　 　Left Arrow　　　 37
P　　　80 　　　/ 　　  111　　　　--　　 -- 　　 　Up Arrow　　　　 38
Q　　　81 　　　-- 　　 --　　　 　--　　 -- 　　 　Right Arrow 　　 39
R　　　82 　　　-- 　　 --　　　　 --　　 -- 　　 　Down Arrow 　　  40
S　　　83 　　　-- 　　 --　　　　 -- 　　-- 　　   Insert 　　　　  45
T　　　84 　　　-- 　   --　　　 　--　　 -- 　　 　Delete 　　　　  46
U　　　85 　　　--  　  --　　　 　-- 　　-- 　　 　Help 　　　　　  47
V　　　86 　　　-- 　   --　　　　 -- 　　-- 　　 　Num Lock 　　　 144
W　　　87 　　　　　　　　　
X　　　88 　　　　　
Y　　　89 　　　　　
Z　　　90 　　　　　
0　　　48 　　　　　
1　　　49 　　　　　
2　　　50 　　　　　　
3　　　51 　　　　　　
4　　　52 　　　　　　
5　　　53 　　　　　　
6　　　54 　　　　　　
7　　　55 　　　　　　
8　　　56 　　　　　　
9　　　57 　
"""


def send_key(key):
    """
    模拟键盘按键
    :param key: 键码
    """
    win32api.keybd_event(key, 0, 0, 0)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def send_double_key(key1, key2):
    """
    组合按键,如 ctrl + c == send_double_key(17, 67)
    :param key1: 键码
    :param key2: 键码
    """
    win32api.keybd_event(key1, 0, 0, 0)
    win32api.keybd_event(key2, 0, 0, 0)
    win32api.keybd_event(key1, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(key2, 0, win32con.KEYEVENTF_KEYUP, 0)
