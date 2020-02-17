# from .login_page import MobileLoginPage
import os
import sys


def __get_module_info():
    pc_module_path = os.path.dirname(os.path.abspath(__file__))
    pc_module_file = os.listdir(pc_module_path)
    pc_module_file.remove('__init__.py')
    pc_module_file.remove('__pycache__')
    m = __import__('pages.mobile', fromlist=pc_module_file)
    return m, pc_module_file, pc_module_path


for pmf in __get_module_info()[1]:
    __pmp = __get_module_info()[2].split('\\')
    __m = sys.modules['%s.%s.%s' % (__pmp[2], __pmp[3], pmf.split('.')[0])]
    __main_class = getattr(__m, 'MainTesting')
    for d in dir(__m):
        if type(getattr(__m, d)) == type and getattr(__m, d) != __main_class:
            exec('from %s import %s' % ('pages.mobile.' + pmf.split('.')[0], d))

