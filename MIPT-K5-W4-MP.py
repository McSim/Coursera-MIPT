# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 22:32:26 2016

@author: McSim
"""

import csv
import pandas as pd
import numpy as np

train_views = []
train_buys = []
with open("coursera_sessions_train.txt", "r") as train_file:
    reader=csv.reader(train_file,delimiter=';')
    for a, b in reader:
        if b == "":
            train_buys.append([])
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

from collections import Counter
counter_views = Counter(merged_train_views)
counter_buys =  Counter(merged_train_buys)
#index=[x[0] for x in counter_views.most_common()]
       
df_train_views = pd.DataFrame(counter_views.most_common(), columns=("goods_id","views"))
df_train_buys = pd.DataFrame(counter_buys.most_common(), columns=("goods_id","buys"))
df_train = pd.merge(df_train_views, df_train_buys, on='goods_id', how='outer')
df_train = df_train.set_index("goods_id")
del(df_train_views, df_train_buys, counter_views, counter_buys)
df_train.sort_values('views', ascending=False, inplace=True)

train1views = df_train.index[:1]
train5views = df_train.index[:5]

df_train.sort_values('buys', ascending=False, inplace=True)
i = 1
while len(df_train.buys[:i].unique()) < 6 :
    i += 1
view_order = [merged_train_views.index(df_train.index[j]) for j in range(i-1)]
view_order = view_order + list(np.zeros(len(df_train)-j-1))
del(i,j)
df_train['view_order'] = pd.Series(view_order, index=df_train.index)
df_train.sort_values(['buys','view_order'], ascending=[False, True], inplace=True)

train1buys = df_train.index[:1]
train5buys = df_train.index[:5]

train_buys = filter(lambda a: a != [], train_buys)
AveragePrecision_1 = np.mean([x.count(train1buys) for x in train_buys])

#AverageRecall_1

#AverageRecall_5
#AveragePrecision_5