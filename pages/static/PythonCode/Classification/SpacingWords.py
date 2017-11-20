from requests import put
from concurrent.futures import ThreadPoolExecutor
import os
import Complete.cohesion_probability as tool

cohesion = tool.CohesionProbability()

# textFile convert jsonFile
def text2json(text):
    data = {'sent':str(text)}
    return data


# for spaceWords
def text2spaceWords(text):
    spacingWords_URI = 'http://35.201.156.140:8080/spacing'
    spaced_text = put(spacingWords_URI, text).json()
    return spaced_text


# morpheme analysis
def useAnalysis(text):
    cohesion.train(text)
    cohesiontokenizer = tool.CohesionTokenizer(cohesion)
    cohesion_tokenized_text = [cohesiontokenizer.tokenize(t) for t in text]
    return cohesion_tokenized_text


# read&get Reviews > spaceWords > Analysis
def readReview(i, lines):

    #########################################################################################################
    #
    #
    #                                               이전 사용 코드
    #
    #
    #########################################################################################################
    # reviews = list()
    # with open("D:\\Capstone\\Movie_Comments_preprocessing\\all\\all.txt", "r", encoding="UTF-8") as file:
    #     lines = file.readlines()
    #
    #     for index, line in enumerate(lines):
    #         if (index + 1) % 1000 == 0:
    #             print(str(index + 1))
    #             # break
    #
    #         # getReviews
    #         # DeepLearning 기반, 한글 자동 API 이용.
    #         # http://freesearch.pe.kr/archives/4647
    #         text = line.split("$$")[1].strip()
    #         text_json = text2json(text)
    #         text_json2 = text2spaceWords(text_json)
    #         spaced_text = text_json2['sent']
    #         reviews.append(spaced_text)
    #
    # with open(os.path.join(os.getcwd(), "SaveFile", "reviewsData.txt"), 'w+', encoding="UTF-8") as f:
    #     for review in reviews:
    #         # print(review)
    #         f.write(review)
    #         f.write('\n')
    #########################################################################################################

    if (i + 1) % 100 == 0:
        print(str(i + 1))

    text = lines[i].split("$$")[1].strip()
    text_json = text2json(text)
    text_json2 = text2spaceWords(text_json)
    spaced_text = text_json2['sent']
    return spaced_text

file = open("D:\\Capstone\\Movie_Comments_preprocessing\\all\\all.txt", "r", encoding="UTF-8")
lines = file.readlines()
f = open(os.path.join(os.getcwd(), "SaveFile", "reviewsData.txt"), 'a', encoding="UTF-8")

def fetch(i):
    rdReview = readReview(i, lines=lines)
    # print(rdReview)
    f.write(rdReview)
    f.write('\n')


############################################################################################

path = "D:\\Users\\PASUDO\\workspace_Django\\Capstone\\pages\\static\\File\\Reviews"

def fetch2(i, subLines, fileName):
    text = subLines[i].strip()
    text_json = text2json(text)
    text_json2 = text2spaceWords(text_json)
    spaced_text = text_json2['sent']

    subFile = open(path + "\\" + fileName, "a", encoding="UTF-8")
    subFile.write(spaced_text)
    subFile.write("\n")


# 스레드 병렬처리.
def start_threadExecutor():
    # http://brownbears.tistory.com/292
    # executor 를 이용한 동시성 처리는 호출해야할 함수와 그에 전달될 인자들을 executor에 넘겨주는 것으로 시작


    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     for i in range(1702600, 2200000): # 0 ~ 1199999 : 인덱스로 접근하기 때문에.
    #         executor.submit(fetch, i)


    # Deep Learning 기반, 띄어쓰기 API 적용
    # for root, dirs, files in os.walk(path):
    #     for filepath in files:
    #
    #         fileName = filepath.split(".")[0] + "_space.txt"
    #
    #         with open(path + "\\" + filepath, "r", encoding="UTF-8") as fp:
    #             lines = fp.readlines()
    #             with ThreadPoolExecutor(max_workers=5) as executor:
    #                 for index, _ in enumerate(lines):
    #                     executor.submit(fetch2, index, lines, fileName)

    print()




'''
text = text2json('오늘 하루 어때요? 좋은하루 입니다.')
print(text)
text_json = text2spaceWords(text)
print(text_json)
print(text_json['sent'])
spaced_text = text_json['sent']


list = ['안녕하세요. 반갑습니다.', '오늘 하루 어때요? 좋은하루 입니다.', '영화보고 싶다. 그렇지 않니?']
cohesion_text = useAnalysis(list)
print(cohesion_text)

'''
