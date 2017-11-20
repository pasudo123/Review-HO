import os
import pickle
import pandas
import numpyTest as np
import pandas as pd
from time import time
from pprint import pprint
from konlpy.tag import Twitter
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


review_x = []
review_y = []


with open("D:\\Capstone\\Movie_Comments preprocessing\\all\\all_pre.txt", "r", encoding="UTF-8") as f:
    lines = f.readlines()

    for index, line in enumerate(lines):
        if (index + 1) % 1000 == 0:
            print(str(index + 1))

        score = line.split("$$")[0].strip()
        text = line.split("$$")[1].strip()

        review_x.append(text)
        review_y.append(score)


tfidf_vectorizer = TfidfVectorizer(min_df=0.00003, max_df=0.9, max_features=10000, use_idf=True, ngram_range=(1, 1), dtype=np.int64, lowercase=False)

X = tfidf_vectorizer.fit_transform(review_x)
y = np.array(review_y)

print(X.shape)
print(y.shape)
curDir = os.getcwd()
pickle.dump(X, open(os.path.join(os.getcwd(), "pickleM", 'X.pkl'), 'wb'))
pickle.dump(y, open(os.path.join(os.getcwd(), "pickleM", 'y.pkl'), 'wb'))
pickle.dump(tfidf_vectorizer, open(os.path.join(os.getcwd(), "pickleM", 'tfidf_vectorizer.pkl'), 'wb'))

'''
(2184477, 10000)
(2184477,)
'''

# train_X = pickle.load(open(os.path.join(curDir, 'pickleM', 'train_X.pkl'), 'rb'))
# train_y = pickle.load(open(os.path.join(curDir, 'pickleM', 'train_y.pkl'), 'rb'))
# test_X = pickle.load(open(os.path.join(curDir, 'pickleM', 'test_X.pkl'), 'rb'))
# test_y = pickle.load(open(os.path.join(curDir, 'pickleM', 'test_y.pkl'), 'rb'))
#
# # tfidf_vectorizer = pickle.load(open(os.path.join(dest, 'tfidfVector.pkl'), 'rb'))
#
# print(train_X.shape)
# print(train_y.shape)
# print(test_X.shape)
# print(test_y.shape)
#
# logreg = LogisticRegression(C=10.0, penalty='l2', random_state=0)
#
# stime = time()
# print("ML start")
# logreg.fit(train_X, train_y)
# print("ML end")
# y_pred = logreg.predict(test_X)
# print("ML time required : [%d]초" %(time() - stime))
# print("정확도 : %.3f" %accuracy_score(test_y, y_pred)) # test 리뷰를, 분류기와 비교한 것과 실제 값과 오차 비교
#
# print()
#
# # 머신러닝 모델 저장
# pickle.dump(logreg, open(os.path.join(curDir, 'pickleM', 'logreg.pkl'), 'wb'), protocol=4)
# print("ML SAVE")