# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 22:32:26 2016

@author: User
"""

import csv
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

def answer(nn, ans):
    f = open('ans'+str(nn)+'.txt', 'w')
    f.write(str(ans))
    f.close()

sms_marks=[]
sms_texts=[]
with open("SMSSpamCollection.txt", "r") as sms_file:
    reader=csv.reader(sms_file,delimiter='\t')
    for sms_mark,sms_text in reader:
        if sms_mark == "spam":
            sms_marks.append(1)
        else:
            sms_marks.append(0)
        sms_texts.append(sms_text)
        
sms_file.close()

sms_vectorizer = CountVectorizer()
t0 = time()
X = sms_vectorizer.fit_transform(sms_texts)
print("done in %0.3fs." % (time() - t0))

ans = cross_val_score(LogisticRegression(), X, sms_marks, cv=10, scoring='f1').mean()
answer(1,ans)
print ans

sms_lg = LogisticRegression()
sms_lg.fit(X, sms_marks)

sms_test = ["FreeMsg: Txt: CALL to No: 86888 & claim your reward of 3 hours talk time to use from your phone now! Subscribe6GB",
             "FreeMsg: Txt: claim your reward of 3 hours talk time",
             "Have you visited the last lecture on physics?",
             "Have you visited the last lecture on physics? Just buy this book and you will have all materials! Only 99$",
             "Only 99$"]
X_test = sms_vectorizer.transform(sms_test)

sms_predict = sms_lg.predict(X_test)
ans = str(sms_predict)[1:10]
answer(2,ans)
print(ans)

ans=[]
for ngram_range in [(2,2),(3,3),(1,3)]:
    sms_vectorizer = CountVectorizer(ngram_range=ngram_range)
    X = sms_vectorizer.fit_transform(sms_texts)
    ans1 = round(cross_val_score(LogisticRegression(), X, sms_marks, cv=10, scoring='f1').mean(),2)
    print ans1
    ans.append(ans1)
ans = ' '.join(str(i) for i in ans if i)
answer(3,ans)

ans=[]
for ngram_range in [(2,2),(3,3),(1,3)]:
    sms_vectorizer = CountVectorizer(ngram_range=ngram_range)
    X = sms_vectorizer.fit_transform(sms_texts)
    ans1 = round(cross_val_score(MultinomialNB(), X, sms_marks, cv=10, scoring='f1').mean(),2)
    print ans1
    ans.append(ans1)
ans = ' '.join(str(i) for i in ans if i)
answer(4,ans)

sms_vectorizer = TfidfVectorizer(ngram_range=(1,3))
X = sms_vectorizer.fit_transform(sms_texts)
#print dict(zip(sms_vectorizer.get_feature_names(), idf))
ans = round(cross_val_score(LogisticRegression(), X, sms_marks, cv=10, scoring='f1').mean(),2)
print ans
answer(5,-1)