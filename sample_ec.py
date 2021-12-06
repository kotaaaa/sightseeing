from extractcontent3 import ExtractContent
extractor = ExtractContent()

# オプション値を指定する
opt = {"threshold":1}
extractor.set_option(opt)

# html = open("../SS_content/trip_site/text_onsen/333/5533_333_text.csv ").read() # 解析対象HTML
# html = open("../SS_contents/text_onsen/289/4829_289_text.csv").read() # 解析対象HTML
html = open("./sample_text.txt").read() # 解析対象HTML

for i in range(200):
    # html = open('../SS_contents/trip_site/text_sotoasobi/'+str(i)+'_text.txt').read() # 解析対象HTML
    extractor.analyse(html)
    text, title = extractor.as_text()
    html, title = extractor.as_html()
    title = extractor.extract_title(html)
    print('text',len(text),text)#,text[:30])
    # print('html',html)
    # print('title',title)
    break
