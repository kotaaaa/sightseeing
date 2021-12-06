# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import urljoin
import bs4
import re
import pandas as pd

for i in range(10):
    skip = [0,1,2,3]
    if i in skip:
        continue
    df = pd.read_table('Date_Url_'+str(i)+'.txt',names=['Date','Url','Title'])

    print(df.head())
    print(df.tail())
    print(df.shape)

    for key,row in df.iterrows():
        # row[1] = 'https://headlines.yahoo.co.jp/article?a=20180914-00179272-diamond-bus_all'
        # row[1] = 'https://headlines.yahoo.co.jp/hl?a=20180914-00000089-it_nlab-ent'
        article = ''
        # print(row[1])
        try:
            soup = bs4.BeautifulSoup(urllib.request.urlopen(row[1]).read(),'html.parser')
        except:
            continue
        # print('qq')
        # texts = soup.find_all('p',class_="ynDetailText yjDirectSLinkTarget")
        try:
            # texts = soup.find('p',class_="ynDetailText yjDirectSLinkTarget").contents
            # texts_All = soup.find_all('p',class_="ynDetailText yjDirectSLinkTarget").contents
            texts_All = soup.find_all('p',class_="ynDetailText yjDirectSLinkTarget")
            # texts_All = soup.select("p.ynDetailText.yjDirectSLinkTarget").contents
            # print(len(texts_All))
            # print(texts)
            # exit()
        except AttributeError:
            print(key, row[1])
            texts = ''
            continue
        for texts in texts_All:
            # print(texts_All,'\n')
            # print(texts,'\n')
            # print(key,len(texts))
            # print(str(texts),'\n')
            article += ' '.join(map(str,texts))
            # print(article,'\n')

        # texts = ' '.join(map(str,texts))
        # article += texts
        for j in range(10):
            try:
                soup = bs4.BeautifulSoup(urllib.request.urlopen(row[1]+'&p='+str(j+2)).read(),'html.parser')
                try:
                    # texts = soup.find('p',class_="ynDetailText yjDirectSLinkTarget").contents
                    texts_All = soup.find_all('p',class_="ynDetailText yjDirectSLinkTarget")#.contents
                except AttributeError:
                    texts = ''
                # print(texts)
                for texts in texts_All:
                    print(key,len(texts))
                    article += ' '.join(map(str,texts))
            except:
                break
        # exit()
        with open('./Ariticles_hakubas/'+str(key)+'article_'+str(i)+'.txt','w') as fw:
            fw.write(article)
        # for i in texts:
        #     # print(i.prettify())
        #     # print(i)
        #     print(i.string)
        #     # print(i.class_.string)
        #     # print(texts.p.string)
        # exit()
