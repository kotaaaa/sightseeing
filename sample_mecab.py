import MeCab


mecab = MeCab.Tagger("-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd/")#Mecabのインスタンスを作成する．
a = 'ご家族一緒の温泉旅行をもっと楽しんでいただきたいとの思いで、2013年末に館内改装を完工させました。車椅子のままご利用いただける「客室」「お食事会場」「貸切露天風呂」「みんなのトイレ」が喜ばれています。西館の最上階・5階に「雲」「星」「月」の貸切露天風呂3室をご用意。「雲」は車椅子のまま洗い場に入れるバリアフリー対応。シャワーチェアーもご用意しております。ご利用時間'
print(a,'\n')
mecab.parse(a)
print(a,'\n')
node = mecab.parseToNode(a)
print(a,'\n')
target_parts_of_speech = ('名詞', )
