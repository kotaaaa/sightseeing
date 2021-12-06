# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import urljoin
import bs4
import re
import pandas as pd

# url = 'https://news.yahoo.co.jp/search/;_ylt=A2RivbjSdZxbz3IAeRYPk.d7?p=%E8%BB%BD%E4%BA%95%E6%B2%A2&aq=-1&oq=&ei=UTF-8'
for k in range(1,57):
    place = '軽井沢'
    place = urllib.parse.quote(place)
    url = 'https://news.yahoo.co.jp/search/?p='+place+'&oq=&ei=UTF-8&xargs=2&b='+str((k-1)*10+1)
    # print(url)
    # exit()
    # url = url.encode('utf-8')
    soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(),'html.parser')
    print(len(soup.find_all('h2',class_="t")))
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
    df.to_csv('Date_Url_karuizawa.txt',mode='a',sep='\t',header=None,index=None)
    # exit()
