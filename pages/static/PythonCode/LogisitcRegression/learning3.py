import os
import pickle
from time import time
from pprint import pprint
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X = pickle.load(open(os.path.join(os.getcwd(), "pickleM", 'X.pkl'), 'rb'))
y = pickle.load(open(os.path.join(os.getcwd(), "pickleM", 'y.pkl'), 'rb'))
tfidf_vectorize = pickle.load(open(os.path.join(os.getcwd(), "pickleM", 'tfidf_vectorizer.pkl'), 'rb'))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=44)

pprint(tfidf_vectorize.vocabulary_ )
print(X_train.shape)
print(y_train.shape)
print("-----------")
print(X_test.shape)
print(y_test.shape)

pickle.dump(X_train, open(os.path.join(os.getcwd(), "pickleM", 'X_train.pkl'), 'wb'))
pickle.dump(y_train, open(os.path.join(os.getcwd(), "pickleM", 'y_train.pkl'), 'wb'))
pickle.dump(X_test, open(os.path.join(os.getcwd(), "pickleM", 'X_test.pkl'), 'wb'))
pickle.dump(y_test, open(os.path.join(os.getcwd(), "pickleM", 'y_test.pkl'), 'wb'))

logreg = LogisticRegression(C=10.0, penalty='l2', random_state=0)

stime = time()
print("ML start")
logreg.fit(X_train, y_train)
print("ML end")
y_pred = logreg.predict(X_test)
print("ML time required : [%d]초" %(time() - stime))
print("정확도 : %.3f" %accuracy_score(y_test, y_pred)) # test 리뷰를, 분류기와 비교한 것과 실제 값과 오차 비교

print()

# 머신러닝 모델 저장
pickle.dump(logreg, open(os.path.join(os.getcwd(), "pickleM", 'logreg.pkl'), 'wb'), protocol=4)
print("ML SAVE")

'''
train data = 1638357 (75%)
test data = 546120   (25%)
accuracy 0.865 = 약 86%  (학습된 모델을 테스트 데이터로 평가한 결과)

'''