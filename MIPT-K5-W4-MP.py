# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 22:32:26 2016

@author: McSim
"""

import csv
import pandas as pd

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

del(i)

from collections import Counter
counter_views = Counter(merged_train_views)
counter_buys =  Counter(merged_train_buys)
#index=[x[0] for x in counter_views.most_common()]
       
df_train_views = pd.DataFrame(counter_views.most_common(), columns=("session_id","views"))
df_train_buys = pd.DataFrame(counter_buys.most_common(), columns=("session_id","buys"))
df_train = pd.merge(df_train_views, df_train_buys, on='session_id', how='outer')
df_train = df_train.set_index("session_id")
del(df_train_views, df_train_buys, counter_views, counter_buys)
#df_train.sort(['buys','views'], ascending=[False, False], inplace=True)
df_train.sort_values(['buys','views'], ascending=[False, False], inplace=True)

#AverageRecall_1
#AveragePrecision_1
#AverageRecall_5
#AveragePrecision_5