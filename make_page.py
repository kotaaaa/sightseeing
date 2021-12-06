# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy as sp
import sklearn
import MeCab
import sys
import re
import os
from xml.sax.saxutils import *

fr=open('header.html','r')
fw=open('page_onsen50_it500.html','a')#作成したいhtmlファイル名をここに書く．上書きモードで動いているので，python実行前に毎回ファイルを消してから実行する．
fw.write(fr.read())
fr.close()

# df = pd.read_csv('../LDAsample/LDA_YN_50.csv',names=['Max_topic','Max_prob','Url','Text'])
df = pd.read_csv('../SS_contents/LDA_50_onsen_it500.csv',names=['Max_topic','Max_prob','Url','Text'])#分類データ
dfword = pd.read_csv('../SS_contents/LDA_words_50_onsen_it500.csv')#トピックごとの出現単語
count=1
each_topic_count=0
Topics=[]
for key,row in df.iterrows():
    if row[0] not in Topics:
        ft = open('topicbutton.html','r')
        topicbutton = ft.read()
        topword = ','.join(dfword['Topic # ' + '{:02d}'.format(int(row[0]))][:5].tolist())
        # fw.write(topicbutton.format(row[0],len(df[df['Max_topic']==row[0]])))
        fw.write(topicbutton.format(row[0],len(df[df['Max_topic']==row[0]]),topword))
        Topics.append(row[0])
        each_topic_count=0

    if each_topic_count >= 10:#各トピック10個ずつテキストを表示する．
        continue

    fc = open('column.html','r')
    html = fc.read()
    fw.write(html.format(key,row[0],row[1],row[3],row[2],count))
    count+=1
    each_topic_count+=1
    # exit()

fr=open('tailer1.html','r')
fw.write(fr.read())
fr.close()

insert=''
for i in Topics:
    insert += "$('.hide_area"+str(i)+"').hide();\n"
fw.write(insert)

fr=open('tailer2.html','r')
fw.write(fr.read())
fr.close()
