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


def uf20InterfaceFileParse(file_path):
    df = xlrd.open_workbook(file_path)
    df_func_list = df.sheet_by_name('功能列表')
    for i in range(1, df_func_list.nrows):
        data = df_func_list.row_values(i)
        interface_func_Info = InterfaceFuncInfo(
            
        )
