# coding: UTF-8
import datetime
import pandas as pd
import numpy as np
import xlrd
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib as plt


'''プログラムの説明
SVMで用いた素性データから教師ラベルと各組成の関係性があるかどうか調べる．
入力>>縦軸:URL,横軸:離散化された素性が入った2次元のデータ
出力>>
1，縦軸:各素性の区切りの個数，横軸:正の相関の値としたときのヒストグラム
2，各素性の正の相関，負の相関等が入ったexcelファイル
'''

# pd.set_option("width", 80)

'''
ヒストグラム作成のための関数
入力：一次元の配列，グラフにつけたい名前(文字列)
出力：ヒストグラム
'''
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
    # exit()
#日付毎のディレクトリ，また，その下には時刻毎のディレクトリを置いて出力結果を管理しましょう
#各日付毎の直下のディレクトリの下に時刻のディレクトリが作成されます．
now = datetime.datetime.now()
datestamp = str(now.month)+'_'+str(now.day)
timestamp = str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)
print(datestamp)
print(timestamp)

'''区切られたレンジ幅のデータから各素性と全体評定の間に関係性があるかどうかを見る'''
# test_binary = pd.read_table('test_binary_data.txt')
test_binary = pd.read_csv('Associations_Homepages_List_7_11_2.csv',encoding='utf-8')
# print(test_binary.shape)
# print(test_binary.head())
# print(test_binary.columns)
test_binary = test_binary.drop(['Unnamed: 0','index_in_prefe','prefecture','rel_path_PF','full_path_PF',
       'layout','what_is _good','if_SS_site','if_go_or_not.1', 'reason'],axis=1)
# print(test_binary.head())
# test_binary = test_binary.astype(int)
# print(test_binary.columns)
test = test_binary[['if_go_or_not',
       '背景色が白を基調としている．', '綺麗な風景の写真がある．', 'メニューバーに食事，グルメに関する項目がある．',
       '現地のアクセス方法が載っている', '一定時間毎に，写真が切り替わる機能がある．', '現地で楽しめるアクティビティの写真がある',
       '美味しそうな食べ物の写真がある．', 'イベント，行事の写真がある．', 'インスタ映えする写真が5枚以上存在する．',
       'トップページの初めに映る部分の60%以上を写真が占めている．', 'サイト内の50%以上の写真に対して，その写真の説明が付けられている．',
       'メニューバーの項目に2色以上の異なる色が充てられている．', 'マウスを写真にかざすと，アクションが起こる写真が1枚以上ある．',
       '現地のおすすめ観光スポットを載せている．', '3名以下の人の笑顔が写った写真がある', '今日の天気の情報がある．',
       '夜景の写真がある', 'モデルコースの案内がある．', '現地のライブカメラの情報がある．', '春夏秋冬ごとに特集されたページがある．',
       'アクセスランキングが載せられている．', '月ごとに特集されたページが組まれている．', '観光地にまつわるコラムがある．']]
# print(test['if_go_or_not'].str.contains('no'))
# exit()
# test = test[test['if_go_or_not'].str.contains('no')]
# print(test.ix[:41,])
test = test.ix[:41,]
# print(test)
# print(test_binary.head())
# exit()
# print(test_binary.head())
# exit()
# test_binary = test_binary.set_column({})
# TRUE = test_binary['TRUE']
# id = test_binary['id']
# each_feature = test_binary.iloc[:,4:]
# features = list(each_feature.columns)
# feature_TRUE = pd.concat([id, TRUE, each_feature], axis=1)
# test_binary = test_binary.drop(['id','TRUE','predict','confidence'], axis=1)
test_T = test.T

test_binary_all = pd.DataFrame(index=test_T.index, columns=['1(Overall):1(feature)','1(Overall):0(feature)','0(Overall):1(feature)','0(Overall):0(feature)', 'Positive_Correlation', 'Negative_Correlation'])

features = list(test.columns)
# print(len(features))
features.remove('if_go_or_not')
# print(len(features))
test = test.drop([38,39,41])
# print(test)
test = test.dropna()
# test = test['if_go_or_not'].astype(int)
# exit()
# features = test.columns.toarray()
# exit()
test = test.astype(int)
print(test)
'''各素性の区切り幅毎に，分割表を作成'''
for feature in features:
    # print(feature)
    # print(test[feature])
    # print(test['if_go_or_not'] == 1.0)
    # print(test[feature] == 1.0)
    # print((test['if_go_or_not'] == 1.0) & (test[feature] == 1))
    # exit()
    a = ((test['if_go_or_not'] == 1.0) & (test[feature] == 1)).sum()#全体評定:良い，かつ，連続値素性がレンジ幅に収まる
    # print(a)
    # print(((test['TRUE'] == 1) & (test['index_0'] == 0)).sum())
    b = ((test['if_go_or_not'] == 1.0) & (test[feature] == 0)).sum()#全体評定:良い，かつ，連続値素性がレンジ幅に収まらない
    # print(b)
    # print(((test['TRUE'] == 0) & (test['index_0'] == 1)).sum())
    c = ((test['if_go_or_not'] == 0) & (test[feature] == 1)).sum()#全体評定:悪い，かつ，連続値素性がレンジ幅に収まる
    # print(c)
    # print(((test['TRUE'] == 0) & (test['index_0'] == 0)).sum())
    d = ((test['if_go_or_not'] == 0) & (test[feature] == 0)).sum()#全体評定:悪い，かつ，連続値素性がレンジ幅に収まらない
    # print(d)
    print(a,b,c,d)
    # exit()

    # Positive_Correlation = (a+d)*1.0/(a+b+c+d)#正の相関を算出
    # Negative_Correlation = (b+c)*1.0/(a+b+c+d)#負の相関を算出
    # print(Positive_Correlation)
    # print(Negative_Correlation)

    test_binary_all.at[feature,'1(Overall):1(feature)'] = a
    test_binary_all.at[feature,'1(Overall):0(feature)'] = b
    test_binary_all.at[feature,'0(Overall):1(feature)'] = c
    test_binary_all.at[feature,'0(Overall):0(feature)'] = d
    # test_binary_all.at[feature,'Positive_Correlation'] = Positive_Correlation
    # test_binary_all.at[feature,'Negative_Correlation'] = Negative_Correlation
    # '''正の相関が0.55以上であるかどうかを調べる'''
    # if(Positive_Correlation >= 0.55 or Positive_Correlation <= 0.45):
        # test_binary_all.at[feature,'Positive_Correlation>0.55'] = 1
    # else:
        # test_binary_all.at[feature,'Positive_Correlation>0.55'] = 0
print(test_binary_all)
test_binary_all.to_csv('conting.csv',encoding='utf-8')
exit()

'''正の相関順にソートを行う'''
test_binary_all = test_binary_all.sort_values(by=['Positive_Correlation'], ascending=False)#'Positive_Correlation'
'''indexの振り直し'''
test_binary_all_index = test_binary_all.reset_index()#dfの要素内に素性の名前が欲しかったので，indexを振り直す．


test_binary_all_index['feature_name'] = test_binary_all_index['index'].str.extract('(\D+)')#正規表現で欲しい文字列を取得する
test_binary_all_index['feature_name'] = test_binary_all_index['feature_name'].str.replace('_|-|over','')#正規表現で欲しい文字列を取得する


features_conti = list(set(test_binary_all_index['feature_name'].values))#連続値素性一覧が入った配列
excel_writer = pd.ExcelWriter('test_binary_correlation.xlsx')#保存するエクセルを作成
# excel_writer = openpyxl.Workbook()
'''連続値素性ごとにexcelシートを作成する'''
for feature_conti in features_conti:
    each_feature_conti = test_binary_all_index[test_binary_all_index['feature_name'] == feature_conti]
    each_feature_conti.to_excel(excel_writer, feature_conti)
    ws = excel_writer.sheets[feature_conti]
    ALFABET = ['B:B','C:C','D:D','E:E','F:F','G:G','H:H','I:I','J:J']#エクセルシートの幅を変更する
    for ALFA in ALFABET:
        ws.set_column(ALFA, 20)
    # each_feature_conti['Positive_Correlation'] = each_feature_conti['Positive_Correlation'].astype(np.float64)#float型に変換する．
    # each_feature_conti['Positive_Correlation'] = each_feature_conti['Positive_Correlation'].round(2)#小数点第2位で四捨五入する．
    # plot_hist(each_feature_conti[each_feature_conti['Positive_Correlation'] >= 0.5], feature_conti, 'orange')#ヒストグラムを作成
    # plot_hist(each_feature_conti[each_feature_conti['Positive_Correlation'] < 0.5], feature_conti, 'red')#ヒストグラムを作成
    plot_hist(each_feature_conti['Positive_Correlation'], feature_conti)#ヒストグラムを作成






#
