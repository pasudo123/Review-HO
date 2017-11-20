import os

# 부정 >> 긍정 >> 부정 >> 긍정 >> 부정 >> 긍정 순으로
# 20 % >> 22 만개 (test)
# 80 % >> 88 만개 (train)

# 위에처럼 하지 않더라도 sklearn 에 텍스트 데이터를 학습데이터와 테스트데이터로 나누는 메소드가 존재한다.
# 따라서 부정과 긍정의 데이터를 모두 합친 다음에, all.txt 를 만들어주고 이후에 데이터를 훈련과 테스트 데이터로 나눈다.

trainFile = open("D:\\Capstone\\train.txt", "w+", encoding="UTF-8")
testFile = open("D:\\Capstone\\test.txt", "w+", encoding="UTF-8")
allFile = open("D:\\Capstone\\all.txt", "w+", encoding="UTF-8")

neg_n = 1
pos_n = 1

for seq in range(11):
    negFile = open("D:\\Capstone\\negText\\negText" + str(neg_n) + ".txt", "r", encoding="UTF-8")
    posFile = open("D:\\Capstone\\posText\\posText" + str(pos_n) + ".txt", "r", encoding="UTF-8")

    neg_lines = negFile.readlines()
    pos_lines = posFile.readlines()

    for idx in range(100000):
        neg = neg_lines[idx]
        pos = pos_lines[idx]

        # # train data
        # if seq <= 7 or ( seq <= 7 and idx <= 89999):
        #     trainFile.write(neg)
        #     trainFile.write(pos)
        # # test data
        # else:
        #     testFile.write(neg)
        #     testFile.write(pos)
        allFile.write(neg)
        allFile.write(pos)

    neg_n = neg_n + 1
    pos_n = pos_n + 1
    print("----")
