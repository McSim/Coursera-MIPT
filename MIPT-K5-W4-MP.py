# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 22:32:26 2016

@author: McSim
"""

import csv
import pandas as pd
import numpy as np

def answer(nn, ans):
    f = open('ans'+str(nn)+'.txt', 'w')
    f.write(str(ans))
    f.close()

train_views = []
train_buys = []
with open("coursera_sessions_train.txt", "r") as train_file:
    reader=csv.reader(train_file,delimiter=';')
    for a, b in reader:
        if b == "":
            train_buys.append('')
        else:
            train_buys.append([int(x) for x in b.split(',')])
        train_views.append([int(x) for x in a.split(',')])
del(a,b,x)        
train_file.close()

merged_train_views = []
for i in train_views:
    merged_train_views += i
    
merged_train_buys = []
for i in train_buys:
        merged_train_buys += i

del(i)
    
from collections import Counter
counter_views = Counter(merged_train_views)
counter_buys =  Counter(merged_train_buys)
#index=[x[0] for x in counter_views.most_common()]
del(merged_train_views, merged_train_buys)
       
df_train_views = pd.DataFrame(counter_views.most_common(), columns=("goods_id","views"))
df_train_buys = pd.DataFrame(counter_buys.most_common(), columns=("goods_id","buys"))
df_freq = pd.merge(df_train_views, df_train_buys, on='goods_id', how='outer')
df_freq = df_freq.set_index("goods_id")
df_freq.sort_values('views', ascending=False, inplace=True)
del(df_train_views, df_train_buys, counter_views, counter_buys)

df_train = pd.DataFrame({'views' : train_views, 'buys' : train_buys})
df_train = df_train[df_train.buys != '']
del(train_views, train_buys)

A = []
for x in df_train.views:
    df_x = pd.DataFrame(np.unique(x), columns=["id"])
    df_x.loc[:,'order'] = list(range(len(np.unique(x))))
    df_x.loc[:,'freq'] = [df_freq.views[y] for y in np.unique(x)]
    df_x.sort_values(['freq', 'order'], ascending=[False,True], inplace=True)
    A.append(list(df_x.id.values))
df_train['recomendations_by_views'] = pd.Series(A, index=df_train.index)
del(A, df_x, x, y)
# в результате имеем датафрейм с просмотрами, покупками и просмотрами отсортированными по частоте просмотров и порядку просмотра

AveragePrecision_1_by_views = np.mean([len(np.intersect1d(df_train.buys.values[i], df_train.recomendations_by_views.values[i][0])) for i in range(len(df_train))])
AveragePrecision_5_by_views = np.mean([len(np.intersect1d(df_train.buys.values[i], df_train.recomendations_by_views.values[i][:5]))/5.0 for i in range(len(df_train))])

AverageRecall_1_by_views = np.mean([len(np.intersect1d(df_train.buys.values[i], 
                                                       df_train.recomendations_by_views.values[i][0]))/len(df_train.buys.values[i])
                                                             for i in range(len(df_train))])
AverageRecall_5_by_views = np.mean([len(np.intersect1d(df_train.buys.values[i], 
                                                       df_train.recomendations_by_views.values[i][:5]))//len(df_train.buys.values[i])
                                                             for i in range(len(df_train))])

df_freq.sort_values('buys', ascending=False, inplace=True)
A = []
for x in df_train.views:
    df_x = pd.DataFrame(np.unique(x), columns=["id"])
    df_x.loc[:,'order'] = list(range(len(np.unique(x))))
    df_x.loc[:,'freq'] = [df_freq.buys[y] for y in np.unique(x)]
    df_x.sort_values(['freq', 'order'], ascending=[False,True], inplace=True)
    A.append(list(df_x.id.values))
df_train['recomendations_by_buys'] = pd.Series(A, index=df_train.index)
del(A, df_x, x, y)

AveragePrecision_1_by_buys = np.mean([len(np.intersect1d(df_train.buys.values[i], df_train.recomendations_by_buys.values[i][0])) for i in range(len(df_train))])
AveragePrecision_5_by_buys = np.mean([len(np.intersect1d(df_train.buys.values[i], df_train.recomendations_by_buys.values[i][0]))/5.0 for i in range(len(df_train))])
AverageRecall_1_by_buys = np.mean([len(np.intersect1d(df_train.buys.values[i], 
                                                       df_train.recomendations_by_buys.values[i][0]))/len(df_train.buys.values[i])
                                                             for i in range(len(df_train))])
AverageRecall_5_by_buys = np.mean([len(np.intersect1d(df_train.buys.values[i], 
                                                       df_train.recomendations_by_buys.values[i][:5]))//len(df_train.buys.values[i])
                                                             for i in range(len(df_train))])

del(i)

string = str(round(AverageRecall_1_by_views,2)) + " "
string += str(round(AveragePrecision_1_by_views,2)) + " "
string += str(round(AverageRecall_5_by_views,2)) + " "
string += str(round(AveragePrecision_5_by_views,2))
answer(1,string)

string = str(round(AverageRecall_1_by_buys,2)) + " "
string += str(round(AveragePrecision_1_by_buys,2)) + " "
string += str(round(AverageRecall_5_by_buys,2)) + " "
string += str(round(AveragePrecision_5_by_buys,2))
answer(3,string)

test_views = []
test_buys = []
with open("coursera_sessions_test.txt", "r") as test_file:
    reader=csv.reader(test_file,delimiter=';')
    for a, b in reader:
        if b == "":
            test_buys.append('')
        else:
            test_buys.append([int(x) for x in b.split(',')])
        test_views.append([int(x) for x in a.split(',')])
del(a,b,x)        
test_file.close()

df_test = pd.DataFrame({'views' : test_views, 'buys' : test_buys})
df_test = df_test[df_test.buys != '']
del(test_views, test_buys)

df_freq.sort_values('views', ascending=False, inplace=True)
A = []
for x in df_test.views:
    df_x = pd.DataFrame(np.unique(x), columns=["id"])
    df_x.loc[:,'order'] = list(range(len(np.unique(x))))
    df_x.loc[:,'freq'] = [df_freq.views[y] if y in df_freq.index else 0 for y in np.unique(x)]
    df_x.sort_values(['freq', 'order'], ascending=[False,True], inplace=True)
    A.append(list(df_x.id.values))
df_test['recomendations_by_views'] = pd.Series(A, index=df_test.index)
del(A, df_x, x, y)

AveragePrecision_1_by_views = np.mean([len(np.intersect1d(df_test.buys.values[i], df_test.recomendations_by_views.values[i][0])) for i in range(len(df_test))])
AveragePrecision_5_by_views = np.mean([len(np.intersect1d(df_test.buys.values[i], df_test.recomendations_by_views.values[i][:5]))/5.0 for i in range(len(df_test))])

AverageRecall_1_by_views = np.mean([len(np.intersect1d(df_test.buys.values[i], 
                                                       df_test.recomendations_by_views.values[i][0]))/len(df_test.buys.values[i])
                                                             for i in range(len(df_test))])
AverageRecall_5_by_views = np.mean([len(np.intersect1d(df_test.buys.values[i], 
                                                       df_test.recomendations_by_views.values[i][:5]))//len(df_test.buys.values[i])
                                                             for i in range(len(df_test))])

df_freq.sort_values('buys', ascending=False, inplace=True)
A = []
for x in df_test.views:
    df_x = pd.DataFrame(np.unique(x), columns=["id"])
    df_x.loc[:,'order'] = list(range(len(np.unique(x))))
    df_x.loc[:,'freq'] = [df_freq.buys[y] if y in df_freq.index else 0 for y in np.unique(x)]
    df_x.sort_values(['freq', 'order'], ascending=[False,True], inplace=True)
    A.append(list(df_x.id.values))
df_test['recomendations_by_buys'] = pd.Series(A, index=df_test.index)
del(A, df_x, x, y)

AveragePrecision_1_by_buys = np.mean([len(np.intersect1d(df_test.buys.values[i], df_test.recomendations_by_buys.values[i][0])) for i in range(len(df_test))])
AveragePrecision_5_by_buys = np.mean([len(np.intersect1d(df_test.buys.values[i], df_test.recomendations_by_buys.values[i][0]))/5.0 for i in range(len(df_test))])
AverageRecall_1_by_buys = np.mean([len(np.intersect1d(df_test.buys.values[i], 
                                                       df_test.recomendations_by_buys.values[i][0]))/len(df_test.buys.values[i])
                                                             for i in range(len(df_test))])
AverageRecall_5_by_buys = np.mean([len(np.intersect1d(df_test.buys.values[i], 
                                                       df_test.recomendations_by_buys.values[i][:5]))//len(df_test.buys.values[i])
                                                             for i in range(len(df_test))])
del(i)

string = str(round(AverageRecall_1_by_views,2)) + " "
string += str(round(AveragePrecision_1_by_views,2)) + " "
string += str(round(AverageRecall_5_by_views,2)) + " "
string += str(round(AveragePrecision_5_by_views,2))
answer(2,string)

string = str(round(AverageRecall_1_by_buys,2)) + " "
string += str(round(AveragePrecision_1_by_buys,2)) + " "
string += str(round(AverageRecall_5_by_buys,2)) + " "
string += str(round(AveragePrecision_5_by_buys,2))
answer(4,string)