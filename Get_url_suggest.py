# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys,os
sys.path.append('/Users/kotakawaguchi/PythonProjects/kaggle/Deropy/')
import g_search
import time

ggl = g_search.Google()
# exit()
query = pd.read_csv('suggest_onsen.csv',names=['query'])
count=1
for key,row in query.iterrows():
    if key != 30:
        continue
    # if key < 629:#629から始める
        # continue
    f = open('Log_onsen.txt','a')
    print(key,row[0])
    # print(row[1])
    # exit()
    df = pd.DataFrame(columns=['query','url'])#,'Search_Volume'])
    result = ggl.Search(row[0], type='text', maximum=20)
    # if len(result) == 0:
    f.write(str(row[0])+'\t'+str(len(result))+'\n')
    # Volume = ggl.Value(a+'　'+b+'　'+c)
    # urls.extend(result)
    for i in result:
        df = df.append(pd.Series([row[0],i],index=df.columns),ignore_index=True)

    df = df.drop_duplicates(subset='url')
    print(df)
    print(df.shape)
    df.to_csv('./url_onsen/'+str(key)+'_df.csv',index=None,header=None)
    if count % 10 ==0:
        time.sleep(3600)
    count+=1

    # exit()
