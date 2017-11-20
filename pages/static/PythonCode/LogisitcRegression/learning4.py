import os
import pickle
import numpy as np
import pandas as pd
from pprint import pprint
from konlpy.tag import Twitter

pos = ["Noun", "Verb", "Adjective", "KoreanParticle"]   # 추출한 품사 리스트
posTagger = Twitter()  # 트위터 형태소 분석기


def preprocessText(text):
    textList = posTagger.pos(text, norm=True, stem=True)

    arr = []
    line = ""

    # 해당품사들만 수집
    for idx, element in enumerate(textList):
        if element[1] in pos:
            arr.append(element)

    lineArr = []

    # 품사 제거
    for morph in arr:
        lineArr.append(morph[0])

    result = " ".join(lineArr)
    return result

logreg = pickle.load(open(os.path.join(os.getcwd(), "pickleM", "logreg.pkl"), "rb"))
tfidfVec = pickle.load(open(os.path.join(os.getcwd(), 'pickleM', 'tfidf_vectorizer.pkl'), 'rb'))

label = {0:'부정', 1:'긍정'}

while True:
    txt = input("작성 : ")

    if txt == "":
        break

    pretxt = preprocessText(txt)
    print([pretxt])
    tfTxt = tfidfVec.transform([pretxt])

    print(tfidfVec)
    print("TFIDF VOCABULARY", tfidfVec.vocabulary_)
    print("TFIDF COUNT NON-ZERO Vocaburary", np.count_nonzero(tfidfVec))
    print('-----------------------------------------------------------')
    print("TFIDF TEXT SHAPE", tfTxt.shape)
    print("TFIDF TEXT TOARRAY", tfTxt.toarray())

    print("TFIDF SENTIMENT : {}".format(logreg.predict(tfTxt)))
    print(logreg.predict(tfTxt)[0])