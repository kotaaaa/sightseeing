# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import urljoin
import bs4
import re
import pandas as pd

# url = 'https://news.yahoo.co.jp/search/;_ylt=A2RivbjSdZxbz3IAeRYPk.d7?p=%E8%BB%BD%E4%BA%95%E6%B2%A2&aq=-1&oq=&ei=UTF-8'

places = ['白馬','安曇野','松本','小布施','長野','八ヶ岳','上田','上高地','戸隠','阿智村']
for pi,place in enumerate(places):
    for k in range(1,57):
        place_de = urllib.parse.quote(place)
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
        df.to_csv('Date_Url_'+str(pi)+'.txt',mode='a',sep='\t',header=None,index=None)
        # exit()
