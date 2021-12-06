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
from matplotlib import pyplot as plt

#
data = pd.read_csv('cohe_sample.csv',names=['topic_num','mean_coherence'])
# #凡例のためにlabelキーワードで凡例名をつける
# plt.plot(data['topic_num'], data['mean_coherence'], label='sin')
#
# #グラフタイトル
# plt.title('mean_coherence')
#
# #グラフの軸
# plt.xlabel('X-Axis')
# plt.ylabel('Y-Axis')
# #グラフの凡例
# plt.legend()
# plt.save('cohe_topicnum.png')
# plt.show()

def main():
    data_x = data['topic_num'].tolist()
    data_y = data['mean_coherence'].tolist()

    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(data_x, data_y ,'-o')
    ax.set_xticks(data_x)
    #グラフタイトル
    plt.title('mean_coherence')

    #グラフの軸
    plt.xlabel('topic_num')
    plt.ylabel('mean_coherence')

    plt.savefig('cohe_topicnum.png')
    # plt.show()

if __name__ == '__main__':
    main()
