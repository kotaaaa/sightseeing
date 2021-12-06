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
import collections
from datetime import datetime
from extractcontent3 import ExtractContent

'''ExtractContent()のオブジェクト生成'''
extractor = ExtractContent()

# オプション値を指定する
opt = {"threshold":1}
extractor.set_option(opt)


'''ツイートの邪魔な文字列を削除する'''
def format_text(corpus):
    '''
    MeCabに入れる前のツイートの整形方法例
    '''
    corpus=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", corpus)
    # corpus=re.sub(u' [ぁ-ん]{1} ', "", corpus)
    # corpus=re.sub(u' [ぁ-ん]{2} ', "", corpus)
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
    # r = re.compile(u"[\uac00-\ud7af\u3200-\u321f\u3260-\u327f\u1100-\u11ff\u3130-\u318f\uffa0-\uffdf\ua960-\ua97f\ud7b0-\ud7ff]+[\\s\.,]*")
    # corpus = re.sub(r, u'', corpus)
    # japanese = re.compile('^[ぁ-んァ-ン一-龥]+')  # used in def clean(list):
    # corpus = re.sub(japanese, u'', corpus)
    return corpus

def preprocess(text):

    for key,row in text.iterrows():
        # text_temp = text
        # print('bbbb',text_temp,'aaaa')
        extractor.analyse(row[1])
        text_temp, title = extractor.as_text()
        # print(row[1][:100])#,text_temp)

        text.at[text.index[key],'Text'] = text_temp
        # if len(row[1]) <= 100:#100文字以内なら，そのテキストは使わない
        #     text_temp = text_temp.drop(index=key)
        #     break

        # for st in stopSS:
        #     if st in row[1]:#ストップワードが含まれていたら，その記事は使わない．
        #         text_temp = text_temp.drop(index=key)
        #         break
    # return text_temp
    # print(text)
    # exit()
    return text

def get_lda_topics(model,num_topic):
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

def topic_title(array,num):
    query_num = collections.Counter(array)
    return query_num.most_common(num)


def main():
    with open('./stopwords3.txt','r') as fr:
        stop = set(fr.readlines())
        stop = [i.strip('\n') for i in stop]

    with open('./stopSS.txt','r') as frSS:
        stopSS = set(frSS.readlines())
        stopSS = [i.strip('\n') for i in stopSS]


    texts=[]
    urls=[]
    print('onsen start reading')
    df_all = pd.read_csv('./save_df_onsen.csv')#,names=['idx_in_query','text_flag','query','topicID','url'])
    # df_all = pd.read_csv('./trip_site/onsen.txt',names=['url'])#,names=['idx_in_query','text_flag','query','topicID','url'])
    # print(df_all.shape)
    # print(df_all.head())
    # print(df_all.tail())
    for key,row in df_all.iterrows():
        # if not 'article' in row[0]:
        #     continue
        # print(key)
        # print(row[0])
        # print(df_all.shape)
        # exit()
        if df_all.at[df_all.index[key],'Textbool'] == 0:
            continue
        # print(key)
        # try:
        f=open('./text_onsen/'+str(df_all.at[df_all.index[key],'queryID'])+'/'+str(key)+'_'+str(df_all.at[df_all.index[key],'queryID'])+'_text.csv')
        # f=open('./trip_site/text_onsen/'+str(key)+'_text.txt')

        texts.append(f.read().split(',',6)[6])
        # texts.append(f.read())
        # print(f.read().split(',',2)[2])
        # exit()
        # except:
        #     continue
        # urls.append(row[0])
        urls.append(row[5])
    print('onsen finish reading')
    # exit()

    data_text = pd.concat([pd.Series(urls),pd.Series(texts)],axis=1)
    data_text.columns = ['Url','Text']

    # print(data_text.shape)
    # print(data_text.head())
    # print(data_text.tail())
    # print(data_text.columns)
    data_text = preprocess(data_text)
    data_text_orig = data_text.copy()

    print(data_text.shape)
    print(data_text.head())
    print(data_text.tail())
    print(data_text.columns)
    data_text = data_text.reset_index(drop=True)

    mecab = MeCab.Tagger("-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd/")#Mecabのインスタンスを作成する．
    # data_text_orig = pd.DataFrame(columns=['Text'],index=data_text.index)
    # data_text_orig = data_text
    Parsed = pd.DataFrame(columns=['Text'],index=data_text.index)
    for idx in range(len(data_text)):
        nodes=[]
        data_text.Text[idx] = format_text(data_text.Text[idx])
        # data_text.Text[idx] = data_text.Text[idx].encode('utf')
        # mecab.parse(data_text.Text[idx])
        node = mecab.parseToNode(data_text.Text[idx])
        target_parts_of_speech = ('名詞', )
        while node:
            if node.feature.split(',')[0] in target_parts_of_speech:#名詞のものだけ
                if node.surface not in stop:#stop単語リストにないもの
                    nodes.append(node.surface)
            node = node.next
        Parsed.iloc[idx]['Text'] = nodes

    train_ = [value[0] for value in Parsed.iloc[0:].values]
    # num_topics = 60
    num_topics = [50,10,20,30,40,50,60,70,80,90,100]#[50,60,70]
    #ここのトピック数をもう少し増やして
    #トピック数ごとのget_coherenceの比較を取る．
    f_co=open('coherence_FS_.txt','a')
    f_co.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    f_co.write('Topic,Coherence_Ave\n')

    for num_topic in num_topics:
        print('num_topic>>',num_topic)
        print(Parsed.shape)
        print(Parsed.head())
        print(Parsed.tail())
        print(Parsed.columns)

        id2word = gensim.corpora.Dictionary(train_)
        corpus = [id2word.doc2bow(text) for text in train_]
        lda = ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topic,iterations=500)

        id2word.save_as_text('dict_onsen_it500.txt')
        id2word = gensim.corpora.Dictionary.load_from_text('dict_onsen_it500.txt')

        gensim.corpora.MmCorpus.serialize('cop_onsen_it500.mm', corpus)
        corpus = gensim.corpora.MmCorpus('cop_onsen_it500.mm')

        lda.save('lda_onsen_it500.model')
        lda = gensim.models.ldamodel.LdaModel.load('lda_onsen_it500.model')

        df = get_lda_topics(lda, num_topic)
        # print(df)
        df.to_csv('LDA_words_'+str(num_topic)+'_onsen_it500.csv')
        cohsum=0
        for coherence in lda.top_topics(corpus=corpus):
            # print(coherence[1])
            cohsum+=coherence[1]
        print('topics coherence average:{}'.format(cohsum/num_topic))
        f_co.write(str(num_topic)+','+str(cohsum/num_topic)+'\n')

        df_topic_prob = document_topic(lda,corpus)
        print('data_text:',data_text.shape)
        print('data_text_orig:',data_text_orig.shape)
        print('df_topic_prob:',df_topic_prob.shape)
        print('Parsed:',Parsed.shape)
        # data = pd.concat([df_topic_prob,data_text],axis=1)#.to_csv('sample.csv',index=None)
        data = pd.concat([df_topic_prob,data_text_orig],axis=1)#.to_csv('sample.csv',index=None)
        data = data.sort_values(['max_topic','max_prob'], ascending=[True, False])
        data.to_csv('LDA_'+str(num_topic)+'_onsen_it500.csv',header=None)
        print(data.head())
        print(data.tail())
        print(data.shape)

        break

if __name__ == "__main__":
    main()
