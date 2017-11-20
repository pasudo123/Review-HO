import os
import numpy as np
import csv
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import Complete.cohesion_probability as tool
from konlpy.tag import Twitter

cohesion = tool.CohesionProbability()

# morpheme analysis
def useAnalysis(text):
    cohesion.train(text)
    cohesiontokenizer = tool.CohesionTokenizer(cohesion)
    cohesion_tokenized_text = [cohesiontokenizer.tokenize(t) for t in text]
    return cohesion_tokenized_text

def loadReview():
    path = "D:\\Users\\PASUDO\\workspace_Django\\Capstone\\pages\\static\\File\\Reviews"

    reviews = list()

    for root, dirs, files in os.walk(path):
        for file in files:
            with open(path + "\\" + file, "r", encoding="UTF-8") as f:
                reviews = f.readlines()

            tokenized_reviews = list()

            for r in reviews:
                tokenized_reviews.append(r[:(r.__len__()-1)]) # 가장 뒤에 개행 제거.

            analysised_text = useAnalysis(tokenized_reviews)

            f = open(os.path.join(os.getcwd(), "SaveFile", file.split(".")[0] + "_tkn.txt"), "w+", encoding="UTF-8")
            for analysised in analysised_text:
                print(analysised)
                f.writelines(','.join(analysised))
                f.writelines("\n")


def processMatrix():
    wordsVocab = list()

    file = open(os.path.join(os.getcwd(), "SaveFile", "words_all.csv"), "r", encoding="UTF-8")
    rdr = csv.reader(file)
    for lines in rdr:
        for word in lines:
            wordsVocab.append(word)

    # 단어저장을 단어장으로 이용해서 TDM 구축. (binary 로 구축)
    vectorizer = CountVectorizer(vocabulary=wordsVocab)  # 단어사전을 미리 설정(Word2Vec에 있는 count를 기준으로 삼는다.)

    path = os.path.join(os.getcwd(), "SaveFile")
    for root, dirs, files in os.walk(path):
        for file in files:

            extens = file.split(".")[1]
            Doc_Matrix = list()

            # 확장자 .txt
            if extens == "txt":
                docFile = open(os.path.join(path, file), "r", encoding="UTF-8")
                sentences = docFile.readlines()

                for index, sentence in enumerate(sentences):
                    sentence = sentence[:sentence.__len__() - 1]  # 개행 제거
                    Doc_Matrix.append(" ".join(sentence.split(",")))

            # 해당 vocaburary 를 가지고 DTM 형성시, 희소행렬의 초과, 적당한 doc 개수만 적용
            X_array = vectorizer.fit_transform(Doc_Matrix).toarray()
            DTM = np.array(X_array)

            np.save(os.path.join(os.getcwd(), "SaveFile", file.split(".")[0]+ "_DTM"), DTM)


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

logreg = pickle.load(open(os.path.join("C:\\Users\\PASUDO\\PycharmProjects\\Capstone\\Complete\\pickleM", "logreg.pkl"), "rb"))
tfidfVec = pickle.load(open(os.path.join("C:\\Users\\PASUDO\\PycharmProjects\\Capstone\\Complete\\pickleM", 'tfidf_vectorizer.pkl'), 'rb'))
label = {0:'부정', 1:'긍정'}

# 구축된 DTM 을 가지고, 문장이 분류된 내용을 넣는다.
def textClassification():
    weight_matrix = np.load(os.path.join(os.getcwd(), "Matrix", "weight_matrix.npy"))
    feature_matrix = np.load(os.path.join(os.getcwd(), "Matrix", "feature_matrix.npy"))

    reviews = list()
    doc_array = list()

    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "SaveFile")):
        for file in files:
            
            # txt 파일
            if file.split(".")[1] == "txt":
                with open(root + "\\" + file, "r", encoding="UTF-8") as f:
                    reviews = f.readlines()
                continue

            # DTM 파일
            if file.split(".")[1] == "npy":
                f = np.load(os.path.join(root + "\\" + file))
                doc_array = f.tolist()

            for index, doc in enumerate(doc_array):
                doc_np = np.array(doc)
                result = np.dot(weight_matrix, doc_np)
                round = np.argmax(result)

                ############################################################
                #
                #
                #                 1 : 긍정          0 : 부정
                #
                #
                ############################################################
                if feature_matrix[round] == "내용":
                    print("분류 : {}".format(feature_matrix[round]))
                    print("내용 : {}".format(reviews[index]))

                    txt = format(reviews[index])
                    # 해당 내용이 긍정인지 혹은 부정인지 분류
                    pretxt = preprocessText(txt)
                    tfTxt = tfidfVec.transform([pretxt])
                    senti = logreg.predict(tfTxt)[0]

                    with open(os.path.join(os.getcwd(), "Classification", file.split(".")[0]+"&&내용.txt"), "a", encoding="UTF-8") as f:
                        f.writelines(str(senti) + "$$" + reviews[index])

                if feature_matrix[round] == "OST":
                    print("분류 : {}".format(feature_matrix[round]))
                    print("내용 : {}".format(reviews[index]))

                    txt = format(reviews[index])
                    # 해당 내용이 긍정인지 혹은 부정인지 분류
                    pretxt = preprocessText(txt)
                    tfTxt = tfidfVec.transform([pretxt])
                    senti = logreg.predict(tfTxt)[0]

                    with open(os.path.join(os.getcwd(), "Classification", file.split(".")[0]+"&&OST.txt"), "a", encoding="UTF-8") as f:
                        f.writelines(str(senti) + "$$" + reviews[index])

                if feature_matrix[round] == "배우":
                    print("분류 : {}".format(feature_matrix[round]))
                    print("내용 : {}".format(reviews[index]))

                    txt = format(reviews[index])
                    # 해당 내용이 긍정인지 혹은 부정인지 분류
                    pretxt = preprocessText(txt)
                    tfTxt = tfidfVec.transform([pretxt])
                    senti = logreg.predict(tfTxt)[0]

                    with open(os.path.join(os.getcwd(), "Classification", file.split(".")[0]+"&&배우.txt"), "a", encoding="UTF-8") as f:
                        f.writelines(str(senti) + "$$" + reviews[index])
    


if __name__ == "__main__":
    print()
    # loadReview()
    # processMatrix()
    # textClassification()