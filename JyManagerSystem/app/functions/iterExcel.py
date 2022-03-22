import os
import xlrd


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