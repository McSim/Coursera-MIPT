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
       
df_train_views = pd.DataFrame(counter_views.most_common(), columns=("goods_id","views"))
df_train_buys = pd.DataFrame(counter_buys.most_common(), columns=("goods_id","buys"))
df_freq_train = pd.merge(df_train_views, df_train_buys, on='goods_id', how='outer')
df_freq_train = df_freq_train.set_index("goods_id")
df_freq_train.sort_values('views', ascending=False, inplace=True)
del(df_train_views, df_train_buys, counter_views, counter_buys)

df_train = pd.DataFrame({'views' : train_views, 'buys' : train_buys})
df_train = df_train[df_train.buys != '']
srtd_views_by_views = []
for x in df_train.views:
    df_x = pd.DataFrame(np.unique(x), columns=["id"])
    df_x.loc[:,'order'] = list(range(len(np.unique(x))))
    df_x.loc[:,'freq'] = [df_freq_train.buys[y] for y in np.unique(x)]
    df_x.sort_values(['freq', 'order'], ascending=[False,True], inplace=True)
    srtd_views_by_views.append(list(df_x.id.values))
df_train['sorted_views'] = pd.Series(srtd_views_by_views, index=df_train.index)

# в результате имеем датафрейм с просмотрами, покупками и просмотрами отсортированными по частоте просмотров и порядку просмотра



#AveragePrecision_1
#AverageRecall_1
#AverageRecall_5
#AveragePrecision_5