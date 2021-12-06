import pandas as pd

# df = pd.read_excel('sample.xlsx')

# df = pd.read_excel('Associations_List_0727_quesionnaire.xlsx',index=True)
df = pd.read_excel('AAlist_QAS.xlsx')
# print(df)
# print(df.columns)
print(df.ix[4:6,5:8])
# df.to_csv('sample.csv')
df.ix[4:6,5:8].to_csv('aaa.csv')
