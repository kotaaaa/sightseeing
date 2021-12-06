# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import urljoin
import bs4
import re
import pandas as pd
import os
import time
from socket import timeout
import http

df_all = pd.DataFrame(columns=['query','url','queryID','Textbool'])

for i in range(878):#keyword_retrip内の上から878個のクエリ(URL取得済みを使う．)（クエリID）
    df = pd.read_csv('./url_onsen/'+str(i)+'_df.csv',names=['query','url'])#])
    df['Textbool'] = 0
    df['queryID'] = int(i)
    df_all = pd.concat([df_all,df])

df_all = df_all.drop_duplicates(subset='url')
df_all = df_all.reset_index()
df_all = df_all.rename(columns={'index':'idx_in_query'})


# past_textbool = pd.read_csv('save_df_onsen.csv',usecols=[2])#,dtype=int)#前回作成したsavedf#前回のテキスト取得の可否を引き継ぎたい
# df_all['Textbool'] = past_textbool['Textbool'].astype(int)#前回のテキスト取得の可否を引き継ぎたい
df_all['Textbool'] = df_all['Textbool'].fillna(0)
df_all['Textbool'] = df_all['Textbool'].astype(int)
print(df_all.head())
print(df_all.tail())
print(df_all.shape)
print(df_all['Textbool'].dtypes)

for key,row in df_all.iterrows():
    # if key < 6904:#6904から始める(記事ID)#途中から始めるとき
    #     continue#途中から始めるとき
    i_dir = os.listdir('./text_onsen/')
    print(key,row[1],row[2],row[3],row[4])
    if not str(df_all.at[df_all.index[key],'queryID']) in i_dir:
        os.mkdir('./text_onsen/'+str(df_all.at[df_all.index[key],'queryID']))
    try:
        text = urllib.request.urlopen(row[4],timeout=15).read().decode('utf-8')#appendする
        df_all.at[df_all.index[key],'Textbool'] = 1
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

    print(key,row[1],row[4],'Get Text!')
    f = open('./text_onsen/'+str(df_all.at[df_all.index[key],'queryID'])+'/'+str(key)+'_'+str(df_all.at[df_all.index[key],'queryID'])+'_text.csv','w')
    f.write(str(key)+','+str(row[0])+','+str(row[1])+','+row[2]+','+str(row[3])+','+row[4]+','+str(text))
    f.close()
    df_all.to_csv('save_df_onsen.csv')#今回作成するsavedf
