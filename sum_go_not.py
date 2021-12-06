# coding: UTF-8
import datetime
import pandas as pd
import numpy as np
import xlrd
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
#

# df = openpyxl.load_workdf('Associations_Homepages_List_7_11_2.xlsx')
df = pd.read_csv('Associations_Homepages_List_7_11_2.csv',index_col=0)
# print(df['sum'])
# print(df.columns)
material = df[['if_go_or_not.1','sum']]
x = material[material['if_go_or_not.1']==1]['sum']
y = material[material['if_go_or_not.1']==0]['sum']
# print(material[material['if_go_or_not.1']==1]['sum'])
# print(len(material[material['if_go_or_not.1']==0]))

# plt.hist(material[material['if_go_or_not.1']==0]['sum'],color='red',rwidth=0.8)
# plt.hist(material[material['if_go_or_not.1']==1]['sum'],color='blue',rwidth=0.8)
labels = ['WannaGo', 'DontWannaGO']
tick = list(np.arange(19))[1:19]
# tick = [1:18]
print(tick)
# exit()

plt.xticks(tick)
plt.xlim(1, 18)
#'''
# exit()
# plt.hist([x, y], stacked=False,rwidth=0.7,label=labels,bins=18)
plt.hist([x, y], histtype="barstacked",rwidth=0.7,label=labels,bins=18,align="left")

plt.xlabel('The number of conditions')
plt.ylabel('Charming Label')
plt.legend()
plt.savefig('CharmByConditions.png')
plt.show()
print(material.ix[:43,1].value_counts())
#'''
exit()
plt.scatter(material.ix[:43,1], material.ix[:43,0],c='red')
plt.xlabel('The number of Satisfied conditions')
plt.ylabel('Charming Label')
plt.savefig('CharmByConditionscatter.png')
plt.show()

# active_sheet = df.active
# print(active_sheet)
# for row in active_sheet.rows:
#     print('----------------------------')
#     for cell in row:
#         print(cell.value)

#
# '''プログラムの説明
# SVMで用いた素性データから教師ラベルと各組成の関係性があるかどうか調べる．
# 入力>>縦軸:URL,横軸:離散化された素性が入った2次元のデータ
# 出力>>
# 1，縦軸:各素性の区切りの個数，横軸:正の相関の値としたときのヒストグラム
# 2，各素性の正の相関，負の相関等が入ったexcelファイル
# '''
#
# # pd.set_option("width", 80)
#
# '''
# ヒストグラム作成のための関数
# 入力：一次元の配列，グラフにつけたい名前(文字列)
# 出力：ヒストグラム
# '''
# def plot_hist(hist_data, which):
# # def plot_hist(hist_data, which, col_label):
#     hist_data_UNDER = []
#     hist_data_ABOVE = []
#     print(which)
#     print(len(hist_data))
#     division_number = len(hist_data)
#     Inlabel = which+', Division_number: '+str(division_number)
#     x_label = "Positive_correlation"
#     y_label = "number"
#     # print(hist_data.values[0])
#     # print(type(hist_data))
#     for i in range(len(hist_data)):
#         if(hist_data.values[i] >= 0.5):
#             hist_data_ABOVE.append(hist_data.values[i])
#         else:
#             hist_data_UNDER.append(hist_data.values[i])
#     print(hist_data_ABOVE)
#     print(hist_data_UNDER)
#     # exit()
#     plt.xlabel(x_label, fontsize = 13)#, FontProperties=fp)
#     plt.ylabel(y_label, fontsize = 13)
#
#     plt.xlim(0.38,0.62)
#     plt.ylim(0,6.1)
#     plt.xticks(np.arange(0.35,0.65,0.05))
#     plt.yticks(np.arange(0,6.1,1))
#     # plt.hist(hist_data_ABOVE,label=Inlabel+', Positive_Correlation>=0.5',bins=20,range=(0.35,0.65),rwidth=0.9,color='orange')#, bins=int(2*max/width))#, range(-max+50, max+50))
#     plt.hist(hist_data_ABOVE,label=Inlabel+', Positive_Correlation>=0.5',bins=20,range=(0.35,0.65),rwidth=0.9,color='orange')#, bins=int(2*max/width))#, range(-max+50, max+50))
#     plt.hist(hist_data_UNDER,label=Inlabel+', Positive_Correlation<0.5',bins=20,range=(0.35,0.65),rwidth=0.9,color='blue')#, bins=int(2*max/width))#, range(-max+50, max+50))
#     # plt.hist(hist_data,label=Inlabel,bins=20,range=(0.35,0.65),rwidth=0.9,color='orange')#, bins=int(2*max/width))#, range(-max+50, max+50))
#     # plt.hist(hist_data,bins=10)#,label=Inlabel,bins=20,range=(0.35,0.65),rwidth=0.9)#, bins=int(2*max/width))#, range(-max+50, max+50))
#     plt.legend()
#     plt.savefig('datas/hist_proba_'+str(which)+'.png')
#     plt.figure()
#     # exit()
# #日付毎のディレクトリ，また，その下には時刻毎のディレクトリを置いて出力結果を管理しましょう
# #各日付毎の直下のディレクトリの下に時刻のディレクトリが作成されます．
# now = datetime.datetime.now()
# datestamp = str(now.month)+'_'+str(now.day)
# timestamp = str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)
# print(datestamp)
# print(timestamp)
#
# '''区切られたレンジ幅のデータから各素性と全体評定の間に関係性があるかどうかを見る'''
# test_binary = pd.read_table('test_binary_data.txt')
# # print(test_binary.head())
# # exit()
# # test_binary = test_binary.set_column({})
# TRUE = test_binary['TRUE']
# id = test_binary['id']
# each_feature = test_binary.iloc[:,4:]
# features = list(each_feature.columns)
# feature_TRUE = pd.concat([id, TRUE, each_feature], axis=1)
# test_binary = test_binary.drop(['id','TRUE','predict','confidence'], axis=1)
# test_binary = test_binary.T
#
#
# # print(test_binary)
# # print(feature_TRUE.head())
# # print(feature_TRUE.shape)
# # exit()
#
#
# test_binary_all = pd.DataFrame(index=test_binary.index, columns=['1(zentai):1(feature)','1(zentai):0(feature)','0(zentai):1(feature)','0(zentai):0(feature)', 'Positive_Correlation', 'Negative_Correlation'])
#
#
# '''各素性の区切り幅毎に，分割表を作成'''
# for feature in features:
#     a = ((feature_TRUE['TRUE'] == 1) & (feature_TRUE[feature] == 1)).sum()#全体評定:良い，かつ，連続値素性がレンジ幅に収まる
#     # print(a)
#     # print(((feature_TRUE['TRUE'] == 1) & (feature_TRUE['index_0'] == 0)).sum())
#     b = ((feature_TRUE['TRUE'] == 1) & (feature_TRUE[feature] == 0)).sum()#全体評定:良い，かつ，連続値素性がレンジ幅に収まらない
#     # print(b)
#     # print(((feature_TRUE['TRUE'] == 0) & (feature_TRUE['index_0'] == 1)).sum())
#     c = ((feature_TRUE['TRUE'] == 0) & (feature_TRUE[feature] == 1)).sum()#全体評定:悪い，かつ，連続値素性がレンジ幅に収まる
#     # print(c)
#     # print(((feature_TRUE['TRUE'] == 0) & (feature_TRUE['index_0'] == 0)).sum())
#     d = ((feature_TRUE['TRUE'] == 0) & (feature_TRUE[feature] == 0)).sum()#全体評定:悪い，かつ，連続値素性がレンジ幅に収まらない
#     # print(d)
#
#     Positive_Correlation = (a+d)*1.0/(a+b+c+d)#正の相関を算出
#     Negative_Correlation = (b+c)*1.0/(a+b+c+d)#負の相関を算出
#     # print(Positive_Correlation)
#     # print(Negative_Correlation)
#
#     test_binary_all.at[feature,'1(zentai):1(feature)'] = a
#     test_binary_all.at[feature,'1(zentai):0(feature)'] = b
#     test_binary_all.at[feature,'0(zentai):1(feature)'] = c
#     test_binary_all.at[feature,'0(zentai):0(feature)'] = d
#     test_binary_all.at[feature,'Positive_Correlation'] = Positive_Correlation
#     test_binary_all.at[feature,'Negative_Correlation'] = Negative_Correlation
#     # '''正の相関が0.55以上であるかどうかを調べる'''
#     # if(Positive_Correlation >= 0.55 or Positive_Correlation <= 0.45):
#         # test_binary_all.at[feature,'Positive_Correlation>0.55'] = 1
#     # else:
#         # test_binary_all.at[feature,'Positive_Correlation>0.55'] = 0
#
# '''正の相関順にソートを行う'''
# test_binary_all = test_binary_all.sort_values(by=['Positive_Correlation'], ascending=False)#'Positive_Correlation'
# '''indexの振り直し'''
# test_binary_all_index = test_binary_all.reset_index()#dfの要素内に素性の名前が欲しかったので，indexを振り直す．
#
#
# test_binary_all_index['feature_name'] = test_binary_all_index['index'].str.extract('(\D+)')#正規表現で欲しい文字列を取得する
# # test_binary_all_index['feature_name'] = test_binary_all_index['feature_name'].str.replace('_|-|over','')#正規表現で欲しい文字列を取得する
# test_binary_all_index['feature_name'] = test_binary_all_index['feature_name'].str.replace('-|over','')#正規表現で欲しい文字列を取得する
#
#
# features_conti = list(set(test_binary_all_index['feature_name'].values))#連続値素性一覧が入った配列
#
#
# # print(features_conti)
# # print(list(feature_TRUE.columns))
# features_ranges_name = list(feature_TRUE.columns)
# # print(features_ranges_name)
# # print(features_conti)
# # print(len(features_ranges_name))
# # print(len(features_conti))
# features_conti_rm_ = []
# for feature_conti in features_conti:
#     # print(feature_conti[-1])
#     # exit()
#     if(feature_conti[-1] == '_'):
#         # print(feature_conti)
#         feature_conti = feature_conti[:-1]
#         # print(feature_conti)
#         features_conti_rm_.append(feature_conti)
#     else:
#         features_conti_rm_.append(feature_conti)
#         # exit()
# # print(features_conti_rm_)
# # print(len(features_conti_rm_))
# print('\n\n\n')
# features_conti = features_conti_rm_
# feature_conti = 0
# ranges = []
# # ranges = ['10','20','30','40','50','60','70','80','90','100']
# ranges = {'index':['10','20','30','40','50','60','70','80','90','100'],
#           'soudan':['1','2','3','4','5','10'],
#           'kanji':['30','60','90','120','150','180','210','240','270','300','330','360','390','420','450'],
#           'hiragana':['30','60','90','120','150','180','210','240','270','300','330','360','390','420','450','480'],
#           'katakana':['30','60','90','120','150','180','210','240','270','300','330'],
#           'kon_sum':['1','2','3','4','5','10','20'],
#           'rei_pattern_html_match':['1','2']}
# # print(ranges['kon_sum'][2:])
# # print(features_ranges_name)
# # print(len(feature_TRUE))
# # exit()
# for feature_range_name in features_ranges_name:#kon_sum_0-2等の離散化された素性で回す
#     for feature_conti in features_conti:#kon_sum等の連続値素性の名前で回す
#         # print(range_one.count(feature_conti) for range_one in features_ranges_name)
#         # print(range_one for range_one in features_ranges_name)
#         # exit()
#         if(feature_conti in feature_range_name):#連続値素性の名前kon_sumが離散化素性の名前の中に入っているか
#
#             if feature_conti != 'knowhow_num':#knowhow_numを'_'で分割したくない
#                 feature_r_n = feature_range_name.rsplit('_',1) #素性名とレンジ幅を後ろの'_'で分割する．
#                 if(len(feature_r_n) >= 2):
#                     if not (feature_r_n[1] == '0' or 'over' in feature_r_n[1]):#0かoverが含まれていたら，使わない
#                         # print(feature_conti)
#                         feature_r_n_num = feature_r_n[1].split('-')
#                         # print(feature_r_n[0],feature_r_n_num[1])
#                         if(feature_conti == feature_r_n[0]):
#                             # print(ranges[feature_r_n[0]])
#                             # ranges.append(feature_r_n_num[1])#あとでコメントアウトを外す
#                             # print(feature_r_n[0]+'_0-'+feature_r_n_num[1])
#                             f_name = feature_r_n[0]+'_0-'+feature_r_n_num[1]
#                             # print(f_name, feature_TRUE.at[1,f_name])
#
#                             # for pd_index in range(len(feature_TRUE)):
#                             # print(pd_index)
#                             # print(type(pd_index))
#                             # for pd_index in range(244):
#                             for pd_index in range(len(feature_TRUE)):
#                                 if(feature_TRUE.at[pd_index,f_name] == 1):
#                                     # print(ranges)
#                                     # print(ranges.index(feature_r_n_num[1]))
#                                     start = ranges[feature_r_n[0]].index(feature_r_n_num[1])
#                                     # print(start)
#                                     # exit()
#                                     for one_range in ranges[feature_r_n[0]][start+1:]:
#                                         # # print(feature_r_n[0]+'_0-'+range)
#                                         # print(range)
#                                         # print('s')
#                                         feature_TRUE.at[pd_index,feature_r_n[0]+'_0-'+one_range] = 0
#                                         # print(feature_r_n[0]+'_0-'+range, feature_TRUE.at[1,feature_r_n[0]+'_0-'+range])
#                                     # range = []
#                                         # print(feature_TRUE.index[1])
#                                     # exit()
#                                 # print(pd_index)
#                                 # exit()
#                             # print(ranges)
#                             # print(pd_index)
#                             # print(type(pd_index))
#                             # print(type(pd_index))
#                             # pd_index = 0
#                             # print(type(pd_index))
#                             # del pd_index
#                             # print('ooolsss')
#                             # ranges = []
#             # print(feature_conti)
#             # if(feature_conti != feature_conti):
#                 # print()
#                 # before_1_feature_conti = feature_conti
#             # print(before_1_feature_conti)
# # print(feature_TRUE)
# feature_TRUE.to_csv('./datas/0602/1bin.csv')
# exit()
#
# # print(feature_TRUE.head())
# # print(feature_TRUE.shape)
# # print(test_binary_all_index['index'].str.extract('(\D+)'))
# # print(test_binary_all_index['feature_name'].str.replace('_|-|over',''))
#
#
# # excel_writer = pd.ExcelWriter('test_binary_correlation_1bin.xlsx')#保存するエクセルを作成
# # # excel_writer = openpyxl.Workdf()
# # '''連続値素性ごとにexcelシートを作成する'''
# # for feature_conti in features_conti:
# #     each_feature_conti = test_binary_all_index[test_binary_all_index['feature_name'] == feature_conti]
# #     each_feature_conti.to_excel(excel_writer, feature_conti)
# #     ws = excel_writer.sheets[feature_conti]
# #     ALFABET = ['B:B','C:C','D:D','E:E','F:F','G:G','H:H','I:I','J:J']#エクセルシートの幅を変更する
# #     for ALFA in ALFABET:
# #         ws.set_column(ALFA, 20)
#     # each_feature_conti['Positive_Correlation'] = each_feature_conti['Positive_Correlation'].astype(np.float64)#float型に変換する．
#     # each_feature_conti['Positive_Correlation'] = each_feature_conti['Positive_Correlation'].round(2)#小数点第2位で四捨五入する．
#     # plot_hist(each_feature_conti[each_feature_conti['Positive_Correlation'] >= 0.5], feature_conti, 'orange')#ヒストグラムを作成
#     # plot_hist(each_feature_conti[each_feature_conti['Positive_Correlation'] < 0.5], feature_conti, 'red')#ヒストグラムを作成
#     # plot_hist(each_feature_conti['Positive_Correlation'], feature_conti)#ヒストグラムを作成
#
#
#
#
#
#
# #
