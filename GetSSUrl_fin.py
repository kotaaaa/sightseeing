#Python 3.6.1
'''使い方
1，作業ディレクトリに「output」というディレクトリを作成する
2，l24-l28,l31-l33のコメントアウトを外して，l34以降のコードをコメントアウトして
プログラムを実行し，県ごとのURLを持ってくる．結果は，'agency_url_'+datestamp+'.txt'として保存される．
3，
'''

import datetime
import re
import urllib.request
from urllib.parse import urljoin
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

'''いつでも時間を保存しましょう'''
now = datetime.datetime.now()
datestamp = str(now.month)+'_'+str(now.day)
timestamp = str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)
# print(datestamp)#5/22に取ってきたら5_22となる．
# print(timestamp)#12時00分に取ってきたら12_00_00となる

'''観光庁のページの各都道府県名とその県の観光協会のURLが一覧に載っている元のURL(0522)
(下のコードは取っておいてください)'''
agency_url = 'http://www.mlit.go.jp/kankocho/kanko_links_test.html'
# res = urllib.request.urlopen(agency_url)
# data = res.read()

# text = data.decode("utf-8")
# print(text)
'''0522に取ってきた観光庁のリンク集内の県名とそのURLの一覧ページを保存します
(0522)(下のコードは取っておいてください)'''
# f = open('output/agency_url_'+datestamp+'.txt', 'w')
# f.write(text)
# f.close()
'''0522に取ってきた観光庁の一覧ページ内の県名とその県のURLの一覧ページを使い回します'''
f = open('output/agency_url_5_22.txt')
text = f.read()
f.close()

'''HTMLの中の各県名，とその件名の観光協会がまとまったページのURLを取得'''
soup = BeautifulSoup(text, 'html.parser')
ending_prefec =['北海道','県','東京都','府']
pre_relative = []
for ending in ending_prefec:
    contents = soup.find_all("a",text=re.compile(ending))
    for i,a in enumerate(contents):
        # href = a.attrs["href"]
        href = a.get("href")
        text = a.string
        pre_relative.append([text,href])

'''データフレームに格納'''
pre_relative = pd.DataFrame(pre_relative)
pre_relative.columns = ['prefecture','rel_path_PF']#カラム名を'県名'，と'相対パス'に変更

'''各県名の相対パスのURLを絶対パスに変換する'''
pre_relative['full_path_PF'] = ''
for i in range(len(pre_relative.index)):
    full_path_PF = urljoin(agency_url, pre_relative.at[pre_relative.index[i],'rel_path_PF'])
    pre_relative.at[pre_relative.index[i],'full_path_PF'] = full_path_PF

print('pre_relativeにNANってある？？-> ', pre_relative.isnull().any().any())

'''0522に取ってきた，県ごとの観光協会のURLが載ったページから
そのURLの一覧ページを保存します(0522)(下のコードは取っておいてください)'''
# for i in range(len(pre_relative.index)):
#     res_AA = urllib.request.urlopen(pre_relative.at[pre_relative.index[i],'full_path_PF'])
#     data_AA = res_AA.read()
#     text_AA = data_AA.decode("utf-8")
#     print(text_AA)
#     f = open('output/prefectures/AA_list_page'+'No'+str(i)+'_'+datestamp+'.txt', 'w')
#     f.write(text_AA)
#     f.close()
'''0522に取ってきた，県ごとの観光協会のURLが載った一覧ページのHTMLを使い回します(0522時点にサーバーにアクセスしたもの)'''
each_association_array = []#ループ内で一時的に保存しておく配列を定義する
'''各市町村の相対パスと市町村名をそれぞれ各県のページ毎に取得'''
for i in range(len(pre_relative.index)):#47回のループを回す
    f = open('output/prefectures/AA_list_page'+'No'+str(i)+'_5_22.txt')#HTMLの入ったファイルを読み込む
    text_AA = f.read()
    f.close()
    soup_AA = BeautifulSoup(text_AA, 'html.parser')
    tac = soup_AA.select_one(".tac")#tacというclass属性に各観光協会のURLが記載されていたので，このように取得する

    contents_in_tac = tac.find_all("a")
    '''一つ一つの協会名の相対パス，観光協会の名称を取得'''
    for num,Associ in enumerate(contents_in_tac):
        href_AA = Associ.get("href")
        text_AA = Associ.string
        each_association_array.append([text_AA,href_AA])

    each_association = pd.DataFrame(each_association_array)
    each_association.columns = ['association_name','SS_Association_URL']#カラム名を'県名'，と'相対パス'に変更
    each_association['prefecture'] = pre_relative.at[pre_relative.index[i],'prefecture']#県名を新しいデータフレームに保存しておく
    each_association['rel_path_PF'] = pre_relative.at[pre_relative.index[i],'rel_path_PF']#相対パスを新しいデータフレームに保存しておく
    each_association['full_path_PF'] = pre_relative.at[pre_relative.index[i],'full_path_PF']#絶対パスを新しいデータフレームに保存しておく

    if(i==0):
        all_prefe_AA_df = each_association#ループの1回目は新しいデータフレームを作成
    else:
        all_prefe_AA_df = all_prefe_AA_df.append(each_association)#ループの2回目以降は作ったデータフレームに結合していく
    #temp(一時的に使った)配列の初期化
    each_association_array = []
    #tempのデータフレームを初期化
    each_association = pd.DataFrame(index=[])
all_prefe_AA_df = all_prefe_AA_df.reset_index()#データフレームのindexの振り直し
all_prefe_AA_df = all_prefe_AA_df.rename(columns = {'index':'index_in_prefe'})#元のindexの名前を変更
print('all_prefe_AA_dfにNANってある？？-> ', pre_relative.isnull().any().any())
print(all_prefe_AA_df.shape)

df = all_prefe_AA_df
df.to_csv('output/Associations_Homepages_List_'+datestamp+'.csv')
