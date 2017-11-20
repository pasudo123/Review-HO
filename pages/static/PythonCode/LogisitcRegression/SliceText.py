
import os

# 1 : 긍정 , 0 : 부정
sentiment = 1
posN = 0
posfnum = 1
posf = open("D:\\Capstone\\posText\\posText" + str(posfnum) + ".txt", "w+", encoding="UTF-8")

negN = 0
negfnum = 1
negf = open("D:\\Capstone\\negText\\negText" + str(negfnum) + ".txt", "w+", encoding="UTF-8")

for root, dirs, files in os.walk("D:\\Capstone\\Movie_Comments"):

    for fileIdx, file in enumerate(files):

        with open(root + "\\" + file, "r", encoding="UTF-8") as f:

            # 영화 명
            print("영화명 : {}\n".format(file))

            lines = f.readlines()

            for lineIdx, line in enumerate(lines):
                # print("---------------------------------------")
                # print("{} : {}".format(lineIdx,line))

                if line.split().__len__() == 0 or line.split().__len__() == 1 or line.split().__len__() == 2:
                    continue

                text = line.split()
                try:
                    score = int(text[1].strip())
                except:
                    continue

                comment = ""

                # NEG : 0
                if score == 1 or score == 2 or score == 3:
                    sentiment = 0
                # POS : 1
                elif score == 8 or score == 9 or score == 10:
                    sentiment = 1
                else:
                    continue

                for i in range(2, len(text)):
                    if not i == len(text):
                        comment += text[i] + " "
                    else:
                        comment += text[i]

                comment = comment[:len(comment) - 1]

                # print("Movie Score : {}".format(score))
                # print("Movie Comment : {}".format(comment))

                # setLine : 긍정은 1 텍스트, 부정은 0 텍스트
                setLine = str(sentiment) + " $$ " + comment

                #########################
                # 긍정과 부정을 섞어서 넣기
                #########################

                # 긍정
                if sentiment == 1:
                    posf.write(setLine)
                    posf.write("\n")
                    posN = posN + 1

                    if (posN == 100000):
                        posfnum = posfnum + 1
                        posN = 0
                        posf = open("D:\\Capstone\\posText\\posText" + str(posfnum) + ".txt", "w+", encoding="UTF-8")
                # 부정
                elif sentiment == 0:
                    negf.write(setLine)
                    negf.write("\n")
                    negN = negN + 1

                    if (negN == 100000):
                        negfnum = negfnum + 1
                        negN = 0
                        negf = open("D:\\Capstone\\negText\\negText" + str(negfnum) + ".txt", "w+", encoding="UTF-8")

'''
Movie Score 1 ~ 3  : NEG 
Movie Score 8 ~ 10 : POS
'''