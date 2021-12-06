# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy as sp
import sklearn
import MeCab
import sys
from nltk.corpus import stopwords
import nltk
from gensim.models import ldamodel
import gensim.corpora
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import normalize
import pickle
import re
import os
from datetime import datetime


'''ツイートの邪魔な文字列を削除する'''
def format_text(corpus):
    '''
    MeCabに入れる前のツイートの整形方法例
    '''
    corpus=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", corpus)
    corpus=re.sub(u' [ぁ-ん]{1} ', "", corpus)
    corpus=re.sub(u' [ぁ-ん]{2} ', "", corpus)
    corpus=re.sub('RT|#|、|。|「|」|【|】|・|…|★|☆|→|↓|←|↑|⇒|⇔|`|"|♡|-|〜|\\|①|●|×|　', "", corpus)
    corpus=re.sub('①|②|③|¥|《|》|÷|£°£²£¹£¶¡|»|£´£´¡|〒|ó|²¼º|◆|[|]|※', "", corpus)
    corpus=re.sub('¤|ã|é|ñ|¡|ê|æ|Î|ãƒ|ç|Ë|å|Þ|¼|Ç|¹|Ê|´|Ä|Æ|è|¸|¾|È|°|ë|³|¶¾|ì|²|á|à|À|±|ò|½|¶|â|─', "", corpus)
    corpus=re.sub('า|·|น|่|เ|관광|한국어|ร|ง|อ|ท|ก|ม|ี|ั|일|由|•|  | |□', "", corpus)
    corpus=re.sub('€||▲|©|\\t', "", corpus)
    corpus=re.sub('▽|〕|〔|△', "", corpus)
    corpus=re.sub(r'[!-~]', "", corpus)#半角記号,数字,英字
    corpus=re.sub(r'[︰-＠]', "", corpus)#全角記号
    corpus=re.sub('\n', "", corpus)#改行文字
    corpus=re.sub('<br/>', "", corpus)#改行文字
    corpus=re.sub('<br>', "", corpus)#改行文字
    r = re.compile(u"[\uac00-\ud7af\u3200-\u321f\u3260-\u327f\u1100-\u11ff\u3130-\u318f\uffa0-\uffdf\ua960-\ua97f\ud7b0-\ud7ff]+[\\s\.,]*")
    corpus = re.sub(r, u'', corpus)
    return corpus

def get_lda_topics(model, num_topic):
    word_dict = {};
    for i in range(num_topic):
        words = model.show_topic(i, topn = 40);
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words];
    return pd.DataFrame(word_dict)

def find_max(topics_per_document):
    list_A = []
    list_B = []
    for q in topics_per_document:
        list_A.append(q[0])
        list_B.append(q[1])
    max_prob  = max(list_B)
    max_index = list_B.index(max_prob)
    max_topic = list_A[max_index]
    # print(str(max_topic)+','+str(max_prob))
    # print('___________________________')
    return max_topic+1,max_prob

def document_topic(model,corpus):
    df = pd.DataFrame(columns=['max_topic','max_prob'])#,'Search_Volume'])

    # for topics_per_document in model[corpus]:
    for topics_per_document in model[corpus]:
        max_topic,max_prob = find_max(topics_per_document)
        # print(corpus[i])
        # print(max_topic,max_prob)
        # exit()
        df = df.append(pd.Series([max_topic,max_prob],index=df.columns),ignore_index=True)
    df['max_topic'] = df['max_topic'].astype(int)#.astype(int)
    return df


with open('./stopwords3.txt','r') as fr:
    stop = set(fr.readlines())
    stop = [i.strip('\n') for i in stop]

with open('./stopSS.txt','r') as frSS:
    stopSS = set(frSS.readlines())
    stopSS = [i.strip('\n') for i in stopSS]


texts=[]
urls=[]

# print('Top_SSs read start')
# Top_SSs = os.listdir('../Htmls/0909Htmls/')
# for Top_SS in Top_SSs:
#     with open('../Htmls/0909Htmls/'+str(Top_SS),'r') as f:
#         text = f.read()
#         text = format_text(text)
#         texts.append(text)
#         text = ''
# f.close()
# print('Top_SSs read complete')

# print('Sub_SSs read start')
# for i in range(2323):
# # for i in range(5):
#     # i+=323
#     try:
#         Subs_SSs = os.listdir('../Htmls/0919_Htmls_links/subs/'+str(i)+'/')
#     except:
#         continue
#     f_sub=open('../Htmls/0919_Htmls_links/subs/'+str(i)+'/SUBSLIST.txt','r')
#     SUBSLIST = f_sub.readlines()
#     SUBSLIST_idx={}
#     for each in SUBSLIST:
#         try:
#             SUBSLIST_idx.update({each.split('\t')[0]:each.split('\t')[1]})
#         except IndexError:
#             continue
#
#     for Sub_SS in Subs_SSs:
#         if Sub_SS == 'SUBSLIST.txt':
#             continue
#         with open('../Htmls/0919_Htmls_links/subs/'+str(i)+'/'+Sub_SS) as f:
#             try:
#                 urls.append(SUBSLIST_idx[Sub_SS.split('_')[0]].strip('\n|"'))
#             except:
#                 continue
#             text = f.read()
#             text = format_text(text)
#             texts.append(text)
#             text = ''
#     f.close()
# print('Sub_SSs read complete')

#YNewsの関東圏の市区町村IDは117~321

# for num in range(117,321):
#     Y_url_title = pd.read_table('../YNews/Citys_URL/Date_Url_'+str(num)+'.txt',names=['date','url','title'])
#     for key,row in Y_url_title.iterrows():
#         try:
#             f=open('../YNews/Ariticles_citys/'+str(num)+'/'+str(key)+'article_'+str(num)+'.txt','r')
#             texts.append(f.read())
#             f.close()
#             # print(texts,key)
#             # exit()
#
#         except:
#             continue
#         urls.append(Y_url_title.iloc[key]['url'])

print('From suggest start reading')
# for j in range(6000):
df8999 = pd.read_csv('../html_from_suggest/df8999_info.csv',names=['query','url','text_flag'])
for key,row in df8999.iterrows():
    # print(key)
    try:
        f=open('../html_from_suggest/Take2/'+str(key)+'_text.txt')
        texts.append(f.read().split(',',2)[2])
        print(f.read().split(',',2)[2])
        exit()
    except:
        continue
    urls.append(row[1])
print('From suggest finish reading')

data_text = pd.concat([pd.Series(urls),pd.Series(texts)],axis=1)
data_text.columns = ['Url','Text']

print(data_text.shape)
print(data_text.head())
print(data_text.tail())
print(data_text.columns)

data_text_temp = data_text
for key,row in data_text.iterrows():
    if len(row[1]) <= 100:#100文字以内なら，そのテキストは使わない
        data_text_temp = data_text_temp.drop(index=key)
        break
    for st in stopSS:
        if st in row[1]:#ストップワードが含まれていたら，その記事は使わない．
            data_text_temp = data_text_temp.drop(index=key)
            break


data_text = data_text_temp
print(data_text.shape)
print(data_text.head())
print(data_text.tail())
print(data_text.columns)
data_text = data_text.reset_index(drop=True)

# exit()


mecab = MeCab.Tagger("-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd/")#Mecabのインスタンスを作成する．
Parsed = pd.DataFrame(columns=['Text'],index=data_text.index)
for idx in range(len(data_text)):
    nodes=[]
    mecab.parse(data_text.Text[idx])
    node = mecab.parseToNode(data_text.Text[idx])
    target_parts_of_speech = ('名詞', )
    while node:
        if node.feature.split(',')[0] in target_parts_of_speech:
            if node.surface not in stop:
                nodes.append(node.surface)
        node = node.next
    Parsed.iloc[idx]['Text'] = nodes
    # exit()


train_ = [value[0] for value in Parsed.iloc[0:].values]
# num_topics = 60
num_topics = [50,60,70]#[30,40,50,60,70]
#ここのトピック数をもう少し増やして
#トピック数ごとのget_coherenceの比較を取る．
f_co=open('coherence_FS_.txt','a')
f_co.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
f_co.write('Topic,Coherence_Ave\n')

for num_topic in num_topics:
    print(Parsed.shape)
    print(Parsed.head())
    print(Parsed.tail())
    print(Parsed.columns)

    id2word = gensim.corpora.Dictionary(train_)
    corpus = [id2word.doc2bow(text) for text in train_]
    lda = ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topic,iterations=50)

    df = get_lda_topics(lda, num_topic)
    # print(df)
    df.to_csv('df_FS_'+str(num_topic)+'.csv')
    cohsum=0
    for coherence in lda.top_topics(corpus=corpus):
        # print(coherence[1])
        cohsum+=coherence[1]
    print('topics coherence average:{}'.format(cohsum/num_topic))
    f_co.write(str(num_topic)+','+str(cohsum/num_topic)+'\n')

    df_topic_prob = document_topic(lda,corpus)
    print(data_text.shape)
    print(df_topic_prob.shape)
    print(Parsed.shape)
    # print(pd.concat([df_topic_prob,data_text],axis=1).head())
    # print(pd.concat([df_topic_prob,data_text],axis=1).tail())
    # print(pd.concat([df_topic_prob,data_text],axis=1).shape)
    # pd.concat([df_topic_prob,data_text],axis=1).to_csv('sample.csv',index=None)
    data = pd.concat([df_topic_prob,data_text],axis=1)#.to_csv('sample.csv',index=None)
    data = data.sort_values(['max_topic','max_prob'], ascending=[True, False])
    data.to_csv('LDA_FS_'+str(num_topic)+'.csv',header=None)
    print(data.head())
    print(data.tail())
    print(data.shape)

    break
