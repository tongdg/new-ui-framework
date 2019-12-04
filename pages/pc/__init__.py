from .login_page import LoginPage
from .wait_deal_page import WaitDealPage
from .expanse_reimburse import ExpanseReimburse

# import os
# import sys
# base = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
# path = os.path.join(base, 'pc')
# lis = os.listdir(path)
# lis.remove('__init__.py')
# lis.remove('__pycache__')
# names = []
#
# __import__(name='pages.pc', fromlist=lis)
# for li in lis:
#     names.append('pages.pc.%s' % li.split('.')[0])
# for name in names:
#     pc_module = sys.modules[name]
#     for pc_dir in dir(pc_module):
#         pc_attr = getattr(pc_module, pc_dir)
#         if type(pc_attr) == type and pc_attr != getattr(pc_module, 'MainTesting'):
#             __import__(name=name, fromlist=['pc', pc_dir])
#
#
# print(locals())










