# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys,os
sys.path.append('/Users/kotakawaguchi/PythonProjects/kaggle/Deropy/')
import g_search
import time
import collections

retrip = pd.read_csv('keyword_retrip.txt',names=['query'])
# df = retrip
colocal = pd.read_csv('keyword_colocal.txt',names=['query'])
# df = colocal
jalan = pd.read_csv('keyword_jalan.txt',names=['query'])
# df = jalan
y_travel = pd.read_csv('keyword_yahootravel.txt',names=['query'])
# df = y_travel


df = pd.concat([retrip,colocal,jalan,y_travel],axis=0)
df = df.reset_index(drop=True)

print(df.shape)
# print(df.head())
# print(df.tail())
# exit()
querys=[]
for key,row in df.iterrows():
    row[0] = row[0].strip('\t|の|お')
    # print(row[0])
    for i in row[0].split(' '):
        querys.append(i)

query_num = collections.Counter(querys)
print(query_num.most_common(30))

    # exit()
