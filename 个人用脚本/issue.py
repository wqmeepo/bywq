# -*- coding: utf-8 -*-

import pandas as pd

file_path = r'F:/项目2018/O45/华夏基金/周报文件/python/'
file_issue1 = 'issue1.xlsx'
file_issue2 = 'issue2.xlsx'
file_need = 'need.xlsx'

df1 = pd.read_excel(file_path + file_issue1)
df2 = pd.read_excel(file_path + file_issue2)
df3 = pd.read_excel(file_path + file_need)

df2 = df2[~df2['处理结果'].isin(['不是缺陷'])]

df2_d = df2.loc[:, ['所属模块', '严重级别', '状态', '当前责任人', '处理结果']]
time1 = pd.to_datetime(df2['提交日期'])
df2_d.index = time1

df2_d1 = df2_d.resample('W').count().loc[:, ['状态']]

print(df2_d1)