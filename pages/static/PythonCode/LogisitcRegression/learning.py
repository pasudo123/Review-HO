
import os
import io
import chardet
import pickle
import codecs
import numpyTest as np
import pandas as pd
from pprint import pprint
from konlpy.tag import Twitter
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

pos = ["Noun", "Verb", "Adjective", "KoreanParticle"]   # 추출한 품사 리스트
posTagger = Twitter()                                   # 트위터 형태소 분석기

def twitter_token(text):
    # 배열값의 형태로 트위터 형태소 분석 돌림
    text_list = posTagger.pos(text, norm=True, stem=True)

    # enumerate 를 통해서, 형태소 단위로 잘라서 읽어들임
    # arr 에 이중저장  , arr : list

    arr = []
    reviews = []
    for idx, element in enumerate(text_list):
        # 해당 품사가 품사 리스트에 해당하고 있으면,
        if element[1] in pos:
            arr.append(element)

    pre_txt = arr
    line = ""

    # 품사가 아닌 텍스트를 얻어온다.
    for morph in pre_txt:
            line = line + morph[0] + " "

    # 공백 제거
    line.strip()
    return line

def read(path):

    for (root, dir, files) in os.walk(path):
        print("root : {}".format(root))
        print("dir : {}".format(dir))
        print("files : {}".format(files))
        print("-------------------------------")

        allF = open(os.path.join(root, "all_pre.txt"), "w+", encoding="UTF-8")

        # 해당 디렉토리의 하위 파일 읽어들이기
        for file in files:
            print("\ntarget file : {}".format(file))

            '''
            
            '''

            bytes = min(32, os.path.getsize(os.path.join(root, file)))
            raw = open(os.path.join(root, file), 'rb').read(bytes)

            if raw.startswith(codecs.BOM_UTF8):
                encoding = 'utf-8-sig'
            else:
                result = chardet.detect(raw)
                encoding = result['encoding']

            infile = io.open(os.path.join(root, file), "r", encoding=encoding)

            reviews_x = []
            reviews_Y = []

            lines = infile.readlines()

            for index, line in enumerate(lines):
                if (index+1) % 1000 == 0:
                    print(str(index+1))

                score = line.split("$$")[0].strip()
                text = line.split("$$")[1].strip()

                com_txt = twitter_token(text)

                if com_txt != '':
                    # 형태소 분석기 , 토크나이징 & 노멀라이징
                    allF.write(score + " $$ " + com_txt)
                    allF.write("\n")

        #             reviews_x.append(com_txt)
        #             reviews_Y.append(score)
        #
        #         if (index+1) == 5000:
        #             break
        #
        # infile.close()
        # return reviews_x, reviews_Y


train_path = "D:\\Capstone\\Movie_Comments preprocessing\\train\\"
test_path = "D:\\Capstone\\Movie_Comments preprocessing\\test\\"
all_path = "D:\\Capstone\\Movie_Comments preprocessing\\all\\"


path = os.getcwd()
dest = os.path.join(path, "pickleM")

if not os.path.exists(dest):
    os.makedirs(dest)

read(all_path)
# trainR_X, trainR_y = read(train_path)
# testR_X, textR_y = read(test_path)
#
# print(trainR_X)
# print(trainR_y)
#
# print("-------------")
# print(len(trainR_X))
# print(len(trainR_y))
# print(len(testR_X))
# print(len(textR_y))
# print("-------------")
#
# tfidf_vectorizer = TfidfVectorizer(min_df=0.02, max_df=0.9, max_features=300, use_idf=True, ngram_range=(1, 1), dtype=np.int64, lowercase=False)
#
# train_X = tfidf_vectorizer.fit_transform(trainR_X)
# train_y = np.array(trainR_y)
#
# # pprint(tfidf_vectorizer.vocabulary_)
#
# print(train_X.shape)
# print(train_y.shape)
# print(type(train_X))
# print(type(train_y))
#
# test_X = tfidf_vectorizer.fit_transform(testR_X)
#
# # pprint(tfidf_vectorizer.vocabulary_)
#
# test_y = np.array(textR_y)
#
# print(test_X.shape)
# print(test_y.shape)
# print(type(test_X))
# print(type(test_y))
#
# ################################################################################
# pickle.dump(train_X, open(os.path.join(dest, 'train_X.pkl'), 'wb'))
# pickle.dump(train_y, open(os.path.join(dest, 'train_y.pkl'), 'wb'))
# pickle.dump(test_X, open(os.path.join(dest, 'test_X.pkl'), 'wb'))
# pickle.dump(test_y, open(os.path.join(dest, 'test_y.pkl'), 'wb'))
#
# pickle.dump(tfidf_vectorizer, open(os.path.join(dest, 'tfidfVector.pkl'), 'wb'))
