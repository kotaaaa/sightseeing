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
    corpus=re.sub('▽|〕|〔|△', "", corpus)
    corpus=re.sub(r'[!-~]', "", corpus)#半角記号,数字,英字
    corpus=re.sub(r'[︰-＠]', "", corpus)#全角記号
    corpus=re.sub('\n', "", corpus)#改行文字
    corpus=re.sub('<br/>', "", corpus)#改行文字
    corpus=re.sub('<br>', "", corpus)#改行文字
    return corpus


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

print('Sub_SSs read start')
for i in range(2323):
# for i in range(3):
    try:
        Subs_SSs = os.listdir('../Htmls/0919_Htmls_links/subs/'+str(i)+'/')
    except:
        continue
    f_sub=open('../Htmls/0919_Htmls_links/subs/'+str(i)+'/SUBSLIST.txt','r')
    SUBSLIST = f_sub.readlines()
    SUBSLIST_idx={}
    for each in SUBSLIST:
        try:
            SUBSLIST_idx.update({each.split('\t')[0]:each.split('\t')[1]})
        except IndexError:
            print(SUBSLIST)
            print(each)
            continue

    # print(SUBSLIST_idx)
    for Sub_SS in Subs_SSs:
        if Sub_SS == 'SUBSLIST.txt':
            continue
        # sub_num = int(Sub_SS.split('_')[0])
        with open('../Htmls/0919_Htmls_links/subs/'+str(i)+'/'+Sub_SS) as f:
            # print(SUBSLIST)
            # exit()
            # print(i,Sub_SS,int(Sub_SS.split('_')[0]))#,len(SUBSLIST),SUBSLIST[9])
            # print(SUBSLIST[14])
            # print(SUBSLIST_idx[Sub_SS.split('_')[0]])
            try:
                urls.append(SUBSLIST_idx[Sub_SS.split('_')[0]].strip('\n|"'))
            except:
                print(SUBSLIST_idx)
                exit()
            # url += ','
            text = f.read()
            text = format_text(text)
            # text = url+text
            texts.append(text)
            text = ''
    f.close()
print('Sub_SSs read complete')

# data_text = pd.DataFrame(texts)
# data_text.columns = ['Text']
data_text = pd.concat([pd.Series(urls),pd.Series(texts)],axis=1)
data_text.columns = ['Url','Text']

print(data_text.shape)
print(data_text.head())
print(data_text.tail())
print(data_text.columns)

with open('./stopwords2.txt','r') as fr:
    stop = set(fr.readlines())
    stop = [i.strip('\n') for i in stop]

mecab = MeCab.Tagger("-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd/")#Mecabのインスタンスを作成する．
Parsed = pd.DataFrame(columns=['Text'],index=data_text.index)
for idx in range(len(data_text)):
    nodes=[]
    # mecab.parse(data_text.iloc[idx]['Text'])
    # print(pd.Series(data_text.Text)[idx])
    # print(data_text.Text[idx])
    # print(data_text.at[data_text.index[int(idx)],'Text'])
    # exit()
    mecab.parse(data_text.Text[idx])

    # data_text.iloc[idx]['Text'] = [word for word in mecab.parse(data_text.iloc[idx]['Text']).split() if word not in stop]
    # node = mecab.parseToNode(data_text.iloc[idx]['Text'])
    node = mecab.parseToNode(data_text.Text[idx])
    target_parts_of_speech = ('名詞', )
    while node:
        if node.feature.split(',')[0] in target_parts_of_speech:
            # print(node.surface)
            if node.surface not in stop:
                nodes.append(node.surface)
        node = node.next
    # data_text.iloc[idx]['Text'] = nodes
    Parsed.iloc[idx]['Text'] = nodes
    # print(data_text.iloc[idx]['Text'])
    # exit()

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
        print(max_topic,max_prob)
        # exit()
        df = df.append(pd.Series([max_topic,max_prob],index=df.columns),ignore_index=True)
    df['max_topic'] = df['max_topic'].astype(int)#.astype(int)
    return df

train_ = [value[0] for value in Parsed.iloc[0:].values]
# num_topics = 60
num_topics = [40, 50, 60]
#ここのトピック数をもう少し増やして
#トピック数ごとのget_coherenceの比較を取る．
for num_topic in num_topics:
    print(Parsed.shape)
    print(Parsed.head())
    print(Parsed.tail())
    print(Parsed.columns)

    id2word = gensim.corpora.Dictionary(train_)
    corpus = [id2word.doc2bow(text) for text in train_]
    lda = ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topic,iterations=50)

    df = get_lda_topics(lda, num_topic)
    print(df)
    # df.to_csv('df2_topic'+str(num_topic)+'.csv')

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
    data.to_csv('LDA_SS_D_topicsample2.csv',header=None)
    print(data.head())
    print(data.tail())
    print(data.shape)

    break
