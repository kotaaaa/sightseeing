# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import urljoin
import bs4
import re
import pandas as pd
import time
# url = 'https://news.yahoo.co.jp/search/;_ylt=A2RivbjSdZxbz3IAeRYPk.d7?p=%E8%BB%BD%E4%BA%95%E6%B2%A2&aq=-1&oq=&ei=UTF-8'

# places=[]
# with open('./citys.txt','r') as f:
#     lines = f.readlines()
#     for i in lines:
#         i = i.strip('\n')
#         if i=='' or '【' in i or '】' in i:
#             continue
#         places.append(i)
#
# print(places)
# print(len(places))
# citys = pd.DataFrame(places,columns=['citys'])
# citys.to_csv('citys_index.txt',header=None,sep='\t')
# exit()
citys = pd.read_table('citys_index.txt',names=['citys'])
# places = ['白馬','安曇野','松本','小布施','長野','八ヶ岳','上田','上高地','戸隠','阿智村']
# for pi,place in enumerate(places):
for pi,place in citys.iterrows():
    # print(pi,'a',place[0],'b',place)
    # exit()
    if pi < 248:#(数字)から実行
        continue
    if pi % 90 ==0:
        time.sleep(3600)

    for k in range(1,101):
        place_de = urllib.parse.quote(place[0])
        url = 'https://news.yahoo.co.jp/search/?p='+place_de+'&oq=&ei=UTF-8&xargs=2&b='+str((k-1)*10+1)
        print(url)
        soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(),'html.parser')
        # print(soup)
        # if '条件に一致する検索結果はありません。' in soup:
            # break
        # exit()
        print(len(soup.find_all('h2',class_="t")))
        if len(soup.find_all('h2',class_="t")) == 0:
            break
        print(len(soup.find_all('div',class_="txt")))
        dates = []
        urls = []
        titles = []
        # print(url)
        # print(soup.find_all('div',class_="hdLogoWrap"))
        # exit()
        for i,j in zip(soup.find_all('div',class_="txt"),soup.find_all('h2',class_="t")):
            dates.append(i.span.string)
            urls.append(j.a.get('href'))
            titles.append(j.string)
            # exit()
        df = pd.concat([pd.Series(dates),pd.Series(urls),pd.Series(titles)],axis=1)
        df.columns = ['Date','Url','Title']
        df.to_csv('./Date_Url/Date_Url_'+str(pi)+'.txt',mode='a',sep='\t',header=None,index=None)#0928次からはindex=Trueでやりましょう．
        # exit()
