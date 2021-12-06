# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy as sp
import MeCab
import sys
import pickle
import re
import os
import chardet
from socket import timeout
import http
import urllib.request
from urllib.parse import urljoin

df = pd.DataFrame(columns=['Query','Url'])
print(df.shape)

for i in range(10):
    for j in range(18):
        df_temp = pd.read_csv('../../Deropy/sug_url_comp/'+str(i)+'_'+str(j)+'_df.csv',names=['Query','Url'])
        print(df_temp.shape)
        df = pd.concat([df,df_temp])

print(df.shape)
print(df.head())
print(df.tail())
df = df.drop_duplicates()
df = df.reset_index(drop=True)

print(df.shape)
print(df.head())
print(df.tail())
# df.to_csv('df8999_info.csv')
# exit()
# df = pd.read_csv('df8999_info.csv',names=['Query','Url','Text_flag'])
df['Text_flag'] = 0
for key,row in df.iterrows():
    if key < 1441:#1441から始める．
        continue

    print(key,row[0],row[1])
    try:
        text = urllib.request.urlopen(row[1],timeout=15).read()
        df.at[df.index[key],'Text_flag']=1
    except urllib.error.HTTPError:
        continue
    except urllib.error.URLError:
        continue
    except UnicodeEncodeError:
        continue
    except ConnectionResetError:
        continue
    except timeout:
        continue
    except ValueError:
        continue
    except http.client.IncompleteRead:
        continue
    except http.client.BadStatusLine:
        continue
    f=open('./Take2/'+str(key)+'_text.txt','w')
    # print(text.decode('shift_jis'))
    # エンコーディング判別
    guess = chardet.detect(text)
    # if guess == None:
    #     text = text.decode('utf8')
    # Unicode化
    try:
        text = text.decode(guess['encoding'],'ignore')
    except:
        text = text.decode('utf8','ignore')
    # print(type(text))
    f.write(str(key)+','+str(row[0])+','+str(row[1])+','+str(text))

    df.to_csv('./Take2/df8999_info.csv',header=None)
    # break
