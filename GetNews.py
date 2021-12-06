# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import urljoin
import bs4
import re
import pandas as pd

# url = 'https://news.yahoo.co.jp/search/?p=%E8%A6%B3%E5%85%89&ei=utf-8&fr=news_sw'
# url = 'https://news.yahoo.co.jp/search/;_ylt=A2RiouZQgJRbgRwA4x0Pk.d7?p=%E8%A6%B3%E5%85%89%E3%80%80%E8%BB%BD%E4%BA%95%E6%B2%A2&aq=-1&oq=&ei=UTF-8'
url = 'https://news.yahoo.co.jp/search/;_ylt=A2RivbjSdZxbz3IAeRYPk.d7?p=%E8%BB%BD%E4%BA%95%E6%B2%A2&aq=-1&oq=&ei=UTF-8'
soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(),'html.parser')
# print(soup)
# print(soup.find_all('h2',class_="t"))
print(len(soup.find_all('h2',class_="t")))
print(len(soup.find_all('div',class_="txt")))
# print(soup.find_all('div',class_="txt").find_all('span'))#.find_all('span',class_='d'))
# print(soup.div.find_all('span'))#.find_all('span',class_='d'))
# exit()
'''#日付取得
for i in soup.find_all('div',class_="txt"):
    print(i.find_all('span',class_="d"))
    print(i.span.string)
    dt = re.findall('\d+',i.span.string)
    print(len(dt),dt)
'''
    # print(i.)
    # print(i.prettify())
# exit()
# for i,j in zip(soup.find_all('h2',class_="t"),soup.find_all('h2',class_="txt")):
    # print(i.prettify())
'''#URL取得
for i in soup.find_all('h2',class_="t"):
    print(i.a.get('href'))
    # print(i.prettify())
'''
dates = []
urls = []
for i,j in zip(soup.find_all('div',class_="txt"),soup.find_all('h2',class_="t")):
    # print(i.find_all('span',class_="d"))
    # print(i.span.string)
    dates.append(i.span.string)
    # print(j.a.get('href'))
    urls.append(j.a.get('href'))

df = pd.concat([pd.Series(dates),pd.Series(urls)],axis=1)
df.columns = ['Date','Url']
df.to_csv('Date_Url.txt',mode='a',sep='\t',header=None)

    # exit()
# # with open('SSUrls.txt','r') as f:
# #     Urls = f.readlines()
#
# for i,url in enumerate(Urls):
#     # url = 'https://otaru.gr.jp/'
#     # url='http://www.city.asahikawa.hokkaido.jp/kankou/index.html'
#     url = 'https://news.yahoo.co.jp/search/?p=%E8%A6%B3%E5%85%89&ei=utf-8&fr=news_sw'
#     # print(urllib.request.urlopen(url).read().decode('utf8'))
#     # exit()
#     try:
#         soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(),'html.parser')
#     except urllib.error.HTTPError:
#         continue
#     except urllib.error.URLError:
#         continue
#     print(i,url)
#     # print(soup)
#     # print(re.findall('//.\D*\.',url))
#     names = [i.replace('//','').replace('www','').replace('.','_').replace('/','_') for i in re.findall('//.\D*\.',url)]
#     name = ''.join(names)
#     # print(names)
#     # exit()
#     # Sitename = re.findall('www\..\D*\.',url)
#     with open('./0909Htmls/'+str(i)+str(name)+'Htmls.txt','w') as fw:
#         fw.write(str(soup))
#         # exit()
