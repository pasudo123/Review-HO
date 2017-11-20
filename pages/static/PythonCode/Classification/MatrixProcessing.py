import os
import csv
import pickle
import logging
import pprint
import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import pdist, squareform

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
embeddingFileName = 'embedding_model_100.'

def loadReview():
    reviews = list()
    with open(os.path.join(os.getcwd(), "SaveFile", "reviewsData.txt"), "r", encoding="UTF-8") as f:
       reviews = f.readlines()
    return reviews


# create word2vec model
def createW2V(tr):\
    # size : 단어벡터의 사이즈를 해당되는 파라미터의 값으로 변경한다.
    embedding_model = Word2Vec(tr, size=100, window=2, min_count=50, workers=4, iter=100, sg=1)
    pickle.dump(embedding_model, open(os.path.join("SaveFile", embeddingFileName + 'pkl'), 'wb'))


# convert word2vec_model by pkl to word2vec_model by txt
def pkl2txt():
    embedding_model = pickle.load(open(os.path.join(os.getcwd(), "SaveFile", embeddingFileName + 'pkl'), 'rb'))
    embedding_model.wv.save_word2vec_format("C:\\Users\\PASUDO\\PycharmProjects\\Capstone\\TextClassification\\SaveFile\\embedding_model_100.txt", fvocab=None, binary=None)


# convert word2vec_model by txt to word2vec_model by csv
def txt2csv():
    with open(os.path.join(os.getcwd(), "SaveFile", embeddingFileName + 'txt'), "r", encoding="UTF-8") as embedding_file:
        stripped = (line.strip() for line in embedding_file)
        lines = (line.split(" ") for line in stripped if line)
        with open(os.path.join(os.getcwd(), "SaveFile", embeddingFileName + 'csv'), "w+", encoding="UTF-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(lines)


# get csvFile & distance Matrix & weight Matrix
def process_Matrix():
    f = open(os.path.join(os.getcwd(), "SaveFile", "embedding_model_100.csv"), "r", encoding="UTF-8")
    rdr = csv.reader(f)

    # 윈도우의 경우 csv 모듈에 데이터를 쓸 때, 각 라인 뒤에 빈 라인이 추가되는 문제가 있어서 newline 옵션을 지정
    feature_csv = open(os.path.join(os.getcwd(), "SaveFile", "feature_raw_matrix.csv"), "w", encoding="UTF-8", newline='')
    feature_wr = csv.writer(feature_csv)

    rownames = list()
    wordvecs = list()

    # feature = ["스토리", "음악", "연기"]
    # feature = ["극본", "음향", "케미"] # 스토리, BGM, 연기
    feature = ["내용", "OST", "배우"]
    feature_query = list()
    feature_query_seq = list()

    for index, line in enumerate(rdr):
        if index == 0:
            continue

        rowname = line[0]
        wordvec = line[1:]
    
        # 해당 rowname 이 쿼리단어인 경우
        # csv 파일의 인덱스는 1부터 시작이기 때문에 헷갈림..
        if rowname in feature:
            feature_query.append(rowname)
            feature_query_seq.append(index-1) # index = 0, word2vec 단어벡터 사이즈이기 때문에 이후에 생략하기 위함.

        rownames.append(rowname)
        wordvecs.append(wordvec)

    array = np.array(wordvecs)
    
    ################################################################
    #
    #           word2vec 에 저장된 단어의 나열을 csv 로 저장.
    #
    ################################################################
    # words_csv = open(os.path.join(os.getcwd(), "SaveFile", "words_all.csv"), "w+", encoding="UTF-8", newline='')
    # wr = csv.writer(words_csv)
    # wr.writerow(rownames)


    ################################################################
    #
    #       유클리디언 방식으로 거리행렬, 정규분포 수식으로 가중치행렬
    #
    ################################################################
    # http://aikorea.org/cs231n/python-numpy-tutorial/#scipy-dist
    # d2 = squareform(pdist(array, 'euclidean'))
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.euclidean_distances.html
    # distance matrix 계산 : 유클리디안 방식 적용 (거리행렬)
    distance_matrix = euclidean_distances(array, array)

    # weight matrix 계산 : 정규분포 관련 수식 적용 (가중치 행렬)
    # weight_matrix = np.exp(-distance_matrix**2/2*1**2)
    weight_matrix = np.exp(-distance_matrix ** 2 / 100) # vector size 에 맞게.
    #####################################################################################################

    print(distance_matrix)
    print("------------------------")
    print(weight_matrix)
    print("------------------------")

    review_query_matrix = list()
    review_weight_matrix = list()

    # 해당 인덱스, feature_query_seq 의 해당 단어 col Index
    for index, seq in enumerate(feature_query_seq):
                                                # 가중치 행렬에서 해당쿼리 단어 추출
        print(feature_query[index])             # 해당쿼리의 인덱스가 무슨 단어인지 추출
        print(weight_matrix[seq])               # 해당쿼리에 대한 가중치 행렬
        print("===== \n")

        # 해당 쿼리에 맞는 가중치 행렬만 추출.
        review_query_matrix.append(feature_query[index])
        review_weight_matrix.append(weight_matrix[seq])

    # numpy save & load url
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.load.html
    np.save(os.path.join(os.getcwd(), "SaveFile", "weight_matrix"), np.array(review_weight_matrix))
    np.save(os.path.join(os.getcwd(), "SaveFile", "feature_matrix"), np.array(review_query_matrix))


# DTM Matrix
def process_Matrix2():
    wordsVocab = list()

    file = open(os.path.join(os.getcwd(), "SaveFile", "words_all.csv"), "r", encoding="UTF-8")
    rdr = csv.reader(file)
    for lines in rdr:
        for word in lines:
            wordsVocab.append(word)

    # 단어저장을 단어장으로 이용해서 TDM 구축. (binary 로 구축)
    vectorizer = CountVectorizer(vocabulary=wordsVocab)  # 단어사전을 미리 설정(Word2Vec에 있는 count를 기준으로 삼는다.)

    # return, Document-Term Matrix (DTM) 구성
    # matrix 가 sparse 해지기때문에, Memory Error 에 대해서 확인.

    Doc_Matrix = list()
    docFile = open(os.path.join(os.getcwd(), "SaveFile", "reviewsData_tkn.txt"), "r", encoding="UTF-8")
    sentences = docFile.readlines()

    for index, sentence in enumerate(sentences):
        sentence = sentence[:sentence.__len__()-1]  # 개행 제거
        Doc_Matrix.append(" ".join(sentence.split(",")))

        # DTM 구축시 크기가 크면 행렬 자체가 sparse 해지기 때문에,
        # 메모리 초과문제가 발생한다. 따라서, 부분집합으로 나누어서 DTM 을 구축한다. (블로그 내용)
        if index == 10000:
            break

    # for sen in Doc_Matrix:
    #     print(sen)

    # 해당 vocaburary 를 가지고 DTM 형성시, 희소행렬의 초과, 적당한 doc 개수만 적용
    X_array = vectorizer.fit_transform(Doc_Matrix).toarray()
    DTM = np.array(X_array)

    np.save(os.path.join(os.getcwd(), "SaveFile", "DTM_matrix"), DTM)


def textClassification():
    # 해당되는 리뷰 내용들.
    txtfile = open(os.path.join(os.getcwd(), "SaveFile", "reviewsData.txt"), "r", encoding="UTF-8")

    weight_matrix = np.load(os.path.join(os.getcwd(), "SaveFile", "weight_matrix.npy"))
    feature_matrix = np.load(os.path.join(os.getcwd(), "SaveFile", "feature_matrix.npy"))
    dtm_matrix = np.load(os.path.join(os.getcwd(), "SaveFile", "DTM_matrix.npy"))

    # for index, _ in enumerate(weight_matrix):
    #     print(weight_matrix[index])
    #     print(feature_matrix[index])
    #     print("-------------------")

    reviews = txtfile.readlines()

    doc_array = dtm_matrix.tolist()

    for index, doc in enumerate(doc_array):
        doc_np = np.array(doc)
        result = np.dot(weight_matrix, doc_np)
        round = np.argmax(result)

        #############################################################################################
        #
        #                       단어 수가 많을 수록 전체 스코어 값이 커지는 문제 발생
        #
        #############################################################################################
        #
        #  단어 전체의 가중치를 평균이 0 이 되도록 스케일링 혹은 문장별 스코어를 문장의 길이로 나누는 방식을 채택
        #
        #############################################################################################

        # print(doc_np)
        # input()

        # pprint.pprint(result)
        # print("분류 : {}".format(feature_matrix[round]))
        # print("결과 : {}".format(result[round]))
        # print("내용 : {}".format(reviews[index]))
        # input()

        if feature_matrix[round] == "OST":
            print("분류 : {}".format(feature_matrix[round]))
            print("내용 : {}".format(reviews[index]))
            input()
            

        if feature_matrix[round] == "배우":
            print("분류 : {}".format(feature_matrix[round]))
            print("내용 : {}".format(reviews[index]))
            input()





