import codecs
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix


xlsx = pd.read_excel('../../../../Desktop/Associations_Homepages_List_6_21_remake.xlsx')
# xlsx = pd.read_excel('../../../../Desktop/test_binary_correlation-2018May31-kawaguchi.xlsx')
# print(xlsx)


# conditions = ['condition1','condition2','condition3','condition4','condition5']
conditions = ['Visuality','Functionality','Usability','Uniqueness','Real-timeness']

df = pd.DataFrame(np.random.random([len(conditions), len(conditions)]), columns=conditions)
df_new = pd.DataFrame(index=conditions, columns=conditions)
# print(df_new)
# exit()
for num_base, base_condition in enumerate(conditions):
    print(base_condition,': 1=',len(xlsx[xlsx[base_condition]==1]),' 0=',len(xlsx[xlsx[base_condition]==0]),'充足率:',len(xlsx[xlsx[base_condition]==1])/(len(xlsx[xlsx[base_condition]==0])+len(xlsx[xlsx[base_condition]==1])))
    for num,i in enumerate(conditions):
        # print(num,i)
        # print(num_base,num)
        # exit()
        # print(i,': 1=',len(xlsx[xlsx[i]==1]),' 0=',len(xlsx[xlsx[i]==0]),'充足率:',len(xlsx[xlsx[i]==1])/(len(xlsx[xlsx[i]==0])+len(xlsx[xlsx[i]==1])))

        # teacher = pd.read_csv('~/Tsukuba/toolexrcise_a/SVM_04/libsvm-3.22/tools/6dim--Test-TeacherSignal.txt', header=None)
        # predict = pd.read_csv('~/Tsukuba/toolexrcise_a/SVM_04/libsvm-3.22/tools/Large-libsvm-Test.txt.predict', header=None)
        # print(len(teacher))
        # print(len(predict))
        # print(predict[0].value_counts())
        # print(predict)
        # if(num!=5):
        if(num_base!=num):
            a = confusion_matrix(xlsx[base_condition].dropna(),xlsx[conditions[num]].dropna())
        # else:
            # a = confusion_matrix(xlsx['condition1'].dropna(),xlsx[conditions[0]].dropna())
        # print(confusion_matrix(xlsx['condition1'].dropna(),xlsx['condition2'].dropna()))
            # print(base_condition,'と',conditions[num])
            # print(a)
            correlation = (a[0][0]+a[1][1])/(a[0][0]+a[1][1]+a[0][1]+a[1][0])
            # print(correlation)#縦軸:condition1，横軸:condition2
            df_new.at[base_condition,conditions[num]] = correlation
    # print('\n\n\n')

# print(df_new)
# conditions_name = ['Visuality','Functionality','Usability','Uniqueness','Real-timeness']

df_new.index = conditions#_name
df_new.columns = conditions#_name
print(df_new)
df_new.to_csv('cor_conditions.csv')
