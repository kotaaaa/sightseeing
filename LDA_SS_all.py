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
import gensim.corpora;
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import normalize
import pickle
import re
import os

'''ツイートの邪魔な文字列を削除する'''
def format_text(corpus):
    '''
    MeCabに入れる前のツイートの整形方法例
    '''
    corpus=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", corpus)
    corpus=re.sub(u' [ぁ-ん]{1} ', "", corpus)
    corpus=re.sub(u' [ぁ-ん]{2} ', "", corpus)
    corpus=re.sub('RT|#|、|。|「|」|【|】|・|…|★|☆|→|↓|←|↑|⇒|⇔|`|"|♡|-|〜|\\|①|●|×|　', "", corpus)
    corpus=re.sub('①|②|③|¥|《|》|÷|£°£²£¹£¶¡|»|£´£´¡|〒|ó|²¼º|◆|', "", corpus)
    corpus=re.sub(r'[!-~]', "", corpus)#半角記号,数字,英字
    corpus=re.sub(r'[︰-＠]', "", corpus)#全角記号
    corpus=re.sub('\n', "", corpus)#改行文字
    corpus=re.sub('<br/>', "", corpus)#改行文字
    corpus=re.sub('<br>', "", corpus)#改行文字
    return corpus


texts=[]
print('Top_SSs read start')
Top_SSs = os.listdir('../Htmls/0909Htmls/')
for Top_SS in Top_SSs:
    with open('../Htmls/0909Htmls/'+str(Top_SS),'r') as f:
        text = f.read()
        text = format_text(text)
        texts.append(text)
        text = ''
f.close()
print('Top_SSs read complete')
print('Sub_SSs read start')
for i in range(2323):
    try:
        Subs_SSs = os.listdir('../Htmls/0919_Htmls_links/subs/'+str(i)+'/')
    except:
        continue

    for Sub_SS in Subs_SSs:
        with open('../Htmls/0919_Htmls_links/subs/'+str(i)+'/'+Sub_SS) as f:
            text = f.read()
            text = format_text(text)
            texts.append(text)
            text = ''
    f.close()
print('Sub_SSs read complete')

data_text = pd.DataFrame(texts)
data_text.columns = ['Text']

print(data_text.shape)
print(data_text.head())
print(data_text.tail())
print(data_text.columns)

with open('./stopwords2.txt','r') as fr:
    stop = set(fr.readlines())
    stop = [i.strip('\n') for i in stop]

mecab = MeCab.Tagger("-Owakati")#Mecabのインスタンスを作成する．
for idx in range(len(data_text)):
    data_text.iloc[idx]['Text'] = [word for word in mecab.parse(data_text.iloc[idx]['Text']).split() if word not in stop]

train_ = [value[0] for value in data_text.iloc[0:].values]
num_topics = 50

print(data_text.shape)
print(data_text.head())
print(data_text.tail())
print(data_text.columns)

id2word = gensim.corpora.Dictionary(train_)
corpus = [id2word.doc2bow(text) for text in train_]
lda = ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics)

def get_lda_topics(model, num_topics):
    word_dict = {};
    for i in range(num_topics):
        words = model.show_topic(i, topn = 40);
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = [i[0] for i in words];
    return pd.DataFrame(word_dict)

df = get_lda_topics(lda, num_topics)
print(df)
df.to_csv('df_topic50_2323.csv')
