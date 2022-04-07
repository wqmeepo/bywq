import xlrd
from app.models import InterfaceFuncInfo


def siHardExcelPreview(file_path):
    list_hard = []
    df = xlrd.open_workbook(str(file_path))
    sheet_jyyf = df.sheet_by_index(1)
    for i in range(sheet_jyyf.nrows):
        if len(sheet_jyyf.row_values(i)) - sheet_jyyf.row_values(i).count('') > 1:
            list_hard.append(sheet_jyyf.row_values(i))
    return list_hard


def siSoftExcelPreview(file_path):
    list_soft = []
    df = xlrd.open_workbook(str(file_path))
    sheet_jyyf = df.sheet_by_index(0)
    for i in range(sheet_jyyf.nrows):
        if len(sheet_jyyf.row_values(i)) - sheet_jyyf.row_values(i).count('') > 1:
            list_soft.append(sheet_jyyf.row_values(i))
    return list_soft


def uf20InterfaceFileSearch(func_no, file_path):
    list_interface_search = []
    df = xlrd.open_workbook(file_path)
    func_list = df.sheet_by_name('功能接口-全部')
    func_position = int(InterfaceFuncInfo.query.filter_by(func_no=func_no).first().hyperlink_position)
    for i in range(func_position, func_list.nrows):
        if '修改记录' in func_list.row_values(i) or len(func_list.row_values(i)) == func_list.row_values(i).count(''):
            break
        list_interface_search.append(func_list.row_values(i)[1:])
    return list_interface_search
