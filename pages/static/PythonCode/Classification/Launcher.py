from TextClassification.SpacingWords import *
from TextClassification.MatrixProcessing import *
from pprint import pprint


# Embedding Words Print()
def word2vecPrint():
    embedding_model = pickle.load(open(os.path.join(os.getcwd(), "SaveFile", 'embedding_model_100.pkl'), 'rb'))
    pprint(embedding_model.most_similar(positive=["스토리"], topn=50))


if __name__ == '__main__':

    #################################
    #
    #   멀티 스레드, 띄어쓰기 API 적용
    #
    #################################
    # start_threadExecutor()


    ##########################################
    #
    #   CohesionProbability 형태소 분석기 이용
    #
    #   토크나이징된 텍스트 데이터 텍스트 파일 저장
    #
    ##########################################
    # reviews = loadReview()
    # tokenized_reviews = list()
    #
    # for r in reviews:
    #     tokenized_reviews.append(r[:(r.__len__()-1)]) # 가장 뒤에 개행 제거.
    #
    # analysised_text = useAnalysis(tokenized_reviews)


    # f = open(os.path.join(os.getcwd(), "SaveFile", "reviewsData_tkn.txt"), "w+", encoding="UTF-8")
    # for analysised in analysised_text:
    #     print(analysised)
    #     f.writelines(','.join(analysised))
    #     f.writelines("\n")
    

    #########################################################
    # 
    # (1) Word2Vec 단어벡터 형성 후 저장
    # 
    # (2) pkl 파일 txt 파일로 변경 후 저장
    #
    # (3) txt 파일 csv 파일로 변경 후 저장
    #
    # * Word2Vec Parameter window 사이즈 조정 (100, 300, 500)
    #########################################################
    # createW2V(analysised_text)    # 1 단계
    # pkl2txt()                     # 2 단계
    # txt2csv()                     # 3 단계




    ######################################################
    #
    # (1) 특정 쿼리 단어만으로 단어 벡터 추출 이후 csv 파일 저장 (특정 쿼리 변경시 여기를 건든다.)
    #     + Distance Matrix & Weight Matrix 구한다.
    #
    # (2) word2vec 의 단어를 전체 가지고 와서, DTM 구축
    #
    #
    # (3) 해당 리뷰가 어느 쿼리에 해당하는 리뷰인지 분류한다.
    #
    ######################################################
    # process_Matrix()

    # process_Matrix2()

    # textClassification()

    # Test Method :
    word2vecPrint()
