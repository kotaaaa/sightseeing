# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import urljoin
import bs4
import re
import pandas as pd

df = pd.read_table('Date_Url_karuizawa.txt',names=['Date','Url','Title'])

print(df.head())
print(df.tail())
print(df.shape)

for key,row in df.iterrows():
    # row[1] = 'https://headlines.yahoo.co.jp/article?a=20180914-00179272-diamond-bus_all'
    # row[1] = 'https://headlines.yahoo.co.jp/hl?a=20180914-00000089-it_nlab-ent'
    article = ''
    soup = bs4.BeautifulSoup(urllib.request.urlopen(row[1]).read(),'html.parser')
    # texts = soup.find_all('p',class_="ynDetailText yjDirectSLinkTarget")
    try:
        texts = soup.find('p',class_="ynDetailText yjDirectSLinkTarget").contents
    except AttributeError:
        texts = ''
    print(texts)
    print(key,len(texts))
    article += ' '.join(map(str,texts))
    # texts = ' '.join(map(str,texts))
    # article += texts
    for i in range(10):
        try:
            soup = bs4.BeautifulSoup(urllib.request.urlopen(row[1]+'&p='+str(i+2)).read(),'html.parser')
            try:
                texts = soup.find('p',class_="ynDetailText yjDirectSLinkTarget").contents
            except AttributeError:
                texts = ''
            # print(texts)
            print(key,len(texts))
            article += ' '.join(map(str,texts))

        except:
            break
    # exit()
    with open('./Ariticles/'+str(key)+'article_karuizawa.txt','w') as fw:
        fw.write(article)
    # for i in texts:
    #     # print(i.prettify())
    #     # print(i)
    #     print(i.string)
    #     # print(i.class_.string)
    #     # print(texts.p.string)
    # exit()
