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

df_all = pd.DataFrame(columns=['query','url','Textbool'])

for i in range(110):
    if i < 30:#30から始める
        continue
    i_dir = os.listdir('./text3/')
    if not str(i) in i_dir:
        os.mkdir('./text3/'+str(i))

    df = pd.read_csv('./url3/'+str(i)+'_df.csv',names=['query','url'])#])
    df['Textbool'] = 0
    for key,row in df.iterrows():
        try:
            text = urllib.request.urlopen(row[1]).read().decode('utf-8')#appendする
            df.at[df.index[key],'Textbool'] = 1
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

        print(key,row[0],row[1])
        f = open('./Text3/'+str(i)+'/'+str(key)+'_'+str(i)+'_text.csv','w')
        f.write(str(key)+','+row[0]+','+row[1]+','+str(text))
        f.close()
    df_all = pd.concat([df_all,df])
    df_all.to_csv('save_df.csv')
        # exit()
