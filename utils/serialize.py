
import os

import xlrd
import xlwt
from xlrd import xldate_as_tuple
from xlutils.copy import copy
from datetime import date
from common.own_error import AlterSheetError


class ReadExcel(object):
    def __init__(self, path, ex):
        if ex:
            self.workbook = xlrd.open_workbook(path)
            self.sheets = {sheet_name: self.workbook.sheet_by_name(sheet_name) for sheet_name in
                           self.workbook.sheet_names()}
        self.path = path
        self.wt_workbook = None

    def _get_sheet(self, sheet):
        return self.sheets[sheet] if sheet in self.sheets else self.workbook.sheet_by_index(sheet)

    def get_rows_value(self, sheet):
        """返回页面每一行的数据"""
        table = self._get_sheet(sheet)
        for i in range(table.nrows):
            yield i, table.row_values(i)

    def get_cols_value(self, sheet):
        """返回页面每一列的数据"""
        table = self._get_sheet(sheet)
        for i in range(table.ncols):
            yield i, table.col_values(i)

    def write_xls(self, sheet, value):
        if self.workbook:
            self.wt_workbook = copy(self.workbook)
            wt_sheet = self.wt_workbook.get_sheet(sheet)
        else:
            self.wt_workbook = xlwt.Workbook()
            wt_sheet = self.wt_workbook.add_sheet(sheet)
        for i in range(0, len(value)):
            for j in range(0, len(value[i])):
                wt_sheet.write(i, j, value[i][j])
        self.wt_workbook.save(self.path)

    # def write_xls(self, sheet):


def x_date(date_str):
    """float -> date"""
    if 0x3c < float(date_str) < 0x2d2482:
        time_tup = xldate_as_tuple(date_str, 0)
        new_date_str = date(*time_tup[:3]).strftime("%Y-%m-%d")
        return new_date_str
    return date_str


class Serialize(object):

    def __init__(self, path):
        self.existing = os.path.exists(path)
        self.Excel = ReadExcel(path, self.existing)
        self.dict_key = None
        self._sheet = 0
        self._type = {}

    def _type_cast(self, data):
        # TODO 后续继续补充类型转换的逻辑
        for tp in self._type:
            if tp != self._type[tp]:
                now_type = eval(self._type[tp])
                data = [info if type(info) != eval(tp) else now_type(info) for info in data]
        return data

    def def_type(self, tp: str, new_tp: str):
        if new_tp in ['int', 'str', 'x_date', 'bool', 'float'] and tp in ['int', 'str', 'x_date', 'bool', 'float']:
            self._type[tp] = new_tp
        return self

    @property
    def get_sheet_data(self):
        """
        获取页面数据,默认返回第一页
        """
        if self.existing is False:
            raise AlterSheetError('sheet does not exist')
        for i, value in self.Excel.get_rows_value(self._sheet):
            if i == 0:
                self.dict_key = value
            else:
                result = self._type_cast(value)
                yield dict(zip(self.dict_key, result))

    def use(self, sheet):
        """切换excel表页,如果不切换默认使用第一页"""
        if isinstance(sheet, str) or isinstance(sheet, int):
            if self.existing:
                if sheet in self.Excel.sheets:
                    self._sheet = sheet
                elif 0 <= sheet < len(self.Excel.sheets):
                    self._sheet = sheet
                else:
                    raise AlterSheetError('sheet is should be sheet name or sheet index')
            else:
                self._sheet = sheet
            return
        raise AlterSheetError('sheet param type is str or int')

    def query(self, where, status='row'):
        """查询一行或者一列的数据"""
        if self.existing is False:
            raise AlterSheetError('sheet does not exist')
        if status == 'row':
            return self._query_row(where)
        elif status == 'col':
            return self._query_col(where)
        else:
            raise Exception("One row of data or one column of data? status is 'row' or 'col'")

    def _query_row(self, where):
        for i, value in self.Excel.get_rows_value(self._sheet):
            if i == 0:
                self.dict_key = value
            if where in value:
                result = self._type_cast(value)
                return dict(zip(self.dict_key, result))

    def _query_col(self, where):
        for i, value in self.Excel.get_cols_value(self._sheet):
            if where in value:
                result = self._type_cast(value)
                return {result.pop(0): result}

    def write_excel(self, value, append=False):
        if append and self.existing:
            # TODO 向Excel中追加数据
            pass
        else:
            self.Excel.write_xls(self._sheet, value)


if __name__ == '__main__':
    # for c in Serialize(Control_Panel_Path).def_type(ByTp.FLOAT, ByTp.INT).get_sheet_data:
    # for c in Serialize(User_Path).def_type(ByTp.FLOAT, ByTp.INT).get_sheet_data:
    # for c in Serialize(Control_Panel_Path).def_type(ByTp.FLOAT, ByTp.DATE).get_sheet_data:
    test_path = r'E:\new-ui-framework\data\excel\pc_flow.xls'
    for c in Serialize(test_path).def_type('float', 'int').get_sheet_data:
        print(c)