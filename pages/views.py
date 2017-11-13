import pickle 
import jpype
from threading import Thread
from konlpy.tag import Twitter 
from django.shortcuts import render
from django.http import JsonResponse
from collections import OrderedDict
from django.views.decorators.csrf import csrf_exempt

import os
import re
import bs4
import json
import time
import urllib
import urllib.request
import urllib.parse
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from django.core import serializers
from concurrent.futures import ThreadPoolExecutor

def show_main(request):
    return render(request, 'pages/MainPage.html', {})

def show_intro(request):
    return render(request, 'pages/Intro.html', {})

def show_demo(request):
    return render(request, 'pages/Demo.html', {})

def show_movie(request):
    return render(request, 'pages/MovieGuide.html', {})

def show_slide(request):
    return render(request, 'pages/Slide.html', {})

class PreProcess:
    def __init__(self):
        self.posList = ["Noun", "Verb", "Adjective", "KoreanParticle"]  # 추출한 품사 리스트
        self.postagger = Twitter()                                      # 트위터 형태소 분석기

    def preprocess_text(self, text):
        jpype.attachThreadToJVM()
        textList = self.postagger.pos(text, norm=True, stem=True)
        
        line = ""
        linearr = []
        arr = []

        # self.pos 에 해당하는 품사만 수집
        for idx, element in enumerate(textList):
            if element[1] in self.posList:
                arr.append(element)

        # 수집된 품사/텍스트 에서 품사 제거
        for morph in arr:
            linearr.append(morph[0])
        
        result = " ".join(linearr)

        return result

# 전처리 클래스
process = PreProcess()

# # 로지스틱 함수 & tfidf 모델
logreg = pickle.load(open(os.path.join(os.getcwd(), "pages", "model", "logreg.pkl"), "rb"))
tfidfvec = pickle.load(open(os.path.join(os.getcwd(), "pages", "model", "tfidf_vectorizer.pkl"), "rb"))

# sklearn 에서 logisticRegression 이용, tfidf 로 변환해서 감성분석. 
def getAnalyze_senti(request):
    get_txt = request.GET.get('text', None)
    print("\n-------------- python --------------")
    print("get_txt (처리 이전) : ", get_txt)

    pre_txt = process.preprocess_text(get_txt)
    tfidf_txt = tfidfvec.transform([pre_txt])

    print("pre_txt (처리 이후) : ", pre_txt)
    print("tfidf_txt : ", tfidf_txt)

    result = "-1";    
    result = str(logreg.predict(tfidf_txt)[0])
    print("result : ", result)

    data = {'result' : result}
    return JsonResponse(data)


class MovieRank:
    def __init__(self):
        self.b_office = BeautifulSoup(requests.get('http://movie.naver.com/movie/sdb/rank/rboxoffice.nhn').text, "html.parser")
    
    
    # 영화 순위 List 추출
    def get_movieRanking(self):
        b_table = self.b_office.find("table", class_="list_ranking list_ranking2")
        b_body = b_table.find("tbody")
        a_href = b_body.find_all("a")

        rank = []
        rank_num = 0

        # rank = [ [영화코드 , 영화순위, 영화제목], ... ]

        for href in a_href:
            mc = ''
            if(href.has_attr("title")): # 타이틀 속성을 지니고 있는 것들만.
                mc = href.attrs['href']

                code = mc.split('=')[1] # 영화 코드
                rank_num = rank_num + 1
                title = href.text       # 영화 제목

                rank.append([code, rank_num, title])

        # List
        return rank

    # 영화코드에 해당하는 영화 포스터 추출
    def get_moviePoster(self, code):
        b_photo = BeautifulSoup(requests.get('http://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + code).text, "html.parser")
        try:
            img = b_photo.find('img')
            return img['src'] + "?type=m203_290_2", img['alt']
        except:
            return 'http://static.naver.net/movie/2012/06/dft_img203x290.png', ''
    
    # 영화코드에 해당하는 영화 상세 내용 크롤
    def get_movieDetail(self, code):

        ###################################
        #      영화 상세 정보 수집 내용
        #   장르 | 국가 | 러닝타임 | 개봉날짜
        #   감독 | 등급 | 
        #   누적관객 | 줄거리
        ###################################
        data = urllib.request.urlopen('http://movie.naver.com/movie/bi/mi/basic.nhn?code=' + code).read().decode('UTF-8')
        page = bs4.BeautifulSoup(re.sub("&#(?![0-9])", "", data), "html.parser")
        info_spec = page.find('dl', class_='info_spec')
        story_Area = page.find('div', class_='story_area')
        
        # dd 태그
        # print(info_spec)
        ddList = info_spec.select("dd")
        
        # 영화정보 dict
        movie_info_dict = {
            'overview':'',
            'nation':'',
            'runningTime':'',
            'open':'',
            'director':'',
            'grade':'',
            'count':'',
            'h_area':'',
            'p_area':''
        }

        infoList = list()

        
        # 개요 나라 시간 날짜 등급 관객
        ov = ddList[0].select('span:nth-of-type(1)')[0].select('a')  # 개요
        nt = ddList[0].select('span:nth-of-type(2)')[0].get_text().strip()  # 나라
        rt = ddList[0].select('span:nth-of-type(3)')[0].get_text().strip()  # 시간
        year = ddList[0].select('span:nth-of-type(4)')[0].select('a:nth-of-type(1)')[0].get_text().strip()
        month = ddList[0].select('span:nth-of-type(4)')[0].select('a:nth-of-type(2)')[0].get_text().strip()
        directer = ddList[1].get_text().strip()
        grade = ddList[3].select('a')[0].get_text()
        mCnt = ddList[4].select('p.count')[0].get_text().strip()
        
        ntStr = str()
        check = nt.find(",")
        if check != -1:
            ntList = nt.split(",")
        
            for index, nt_e in enumerate(ntList):
                nt_e = nt_e.replace("\r", "")
                nt_e = nt_e.replace("\t", "")
                nt_e = nt_e.replace("\n", "")
                ntStr = ntStr + nt_e.strip()
                if index != ntList.__len__()-1:
                    ntStr = ntStr + ","

            ntStr = ntStr.replace(",", " ")
        
        else:
            ntStr = nt
        
        # 콤마로 구분되는 영화 개요
        ovStr = str()
        for index, ov_e in enumerate(ov):
            ovStr = ovStr + ov_e.get_text().strip()
            if index != ov.__len__()-1:
                ovStr = ovStr + ","
        
        ovStr = ovStr.replace(",", " ")

        movie_info_dict['overview'] = ovStr
        movie_info_dict['nation'] = ntStr
        movie_info_dict['open'] = year + month
        movie_info_dict['director'] = directer
        movie_info_dict['grade'] = grade
        movie_info_dict['runningTime'] = rt
        movie_info_dict['count'] = mCnt

        # pprint(movie_info_dict)
        # print(story_Area.select('h5.h_tx_story')[0].get_text())
        area_data = str(story_Area.select('p.con_tx')[0]).replace("\xa0", "")
        area_data = area_data.replace("<br>"," ")
        area_soup = bs4.BeautifulSoup(re.sub("&#(?![0-9])", "", area_data), "html.parser")
        # print(area_soup.get_text())

        try:
            movie_info_dict['h_area'] = story_Area.select('h5.h_tx_story')[0].get_text()
        except IndexError:
            movie_info_dict['h_area'] = "-"

        movie_info_dict['p_area'] = area_soup.get_text()

        # 영화정보 dict 반환
        return movie_info_dict

        
mr = MovieRank()                # 영화정보 크롤관련 클래스 객체
ranks = mr.get_movieRanking()   # 영화순위 메소드

##############################################################################
#
#
#               ajax 를 통한, 영화 정보 크롤링 및 Json 형식 파일 저장
#
#
##############################################################################
def getMovieInfo(request):
    JSONData = OrderedDict()

    # 파일 존재.
    if (os.path.isfile(os.path.join(os.getcwd(), "pages", "static", "File", "movieInfo.json"))) == True:
        with open(os.path.join(os.getcwd(), "pages", "static", "File", "movieInfo.json"), encoding='UTF-8') as jFile:
            loadData = json.load(jFile)

            for index in range(1, 11):
                movieData = OrderedDict()
                JSONData[loadData[str(index)]["ranking"]] = movieData
                movieData["code"] = loadData[str(index)]["code"]
                movieData["title"] = loadData[str(index)]["title"]
                movieData["ranking"] = loadData[str(index)]["ranking"]
                movieData["posterUrl"] = loadData[str(index)]["posterUrl"]
    # 파일 미존재.
    else:       
        for rank in ranks:
            movieData = OrderedDict()
            JSONData[str(rank[1])] = movieData
            movieData["code"] = int(rank[0])
            movieData["title"] = rank[2]
            movieData["ranking"] = int(rank[1])
            movieData["posterUrl"] = mr.get_moviePoster(rank[0])[0]
            
        # 파일쓰기.
        with open(os.path.join(os.getcwd(), "pages", "static", "File", "movieInfo.json"), 'w', encoding='UTF-8') as jFile:
            json.dump(JSONData, jFile, ensure_ascii=False, indent="\t")
    
    # JSON 변환.
    movieJson = json.dumps(JSONData)
    return JsonResponse(movieJson, safe=False)


##############################################################################
#
#
#              ajax 를 통한, 영화 리뷰 크롤링 및 Json 형식 파일 저장
#
#
##############################################################################
def getComments(code):

    def makeArgs(code, page):
        params = {
            'code': code,           # 영화코드
            'type': 'after',
            'isActualPointWriteExecute': 'false',
            'isMileageSubscriptionAlready': 'false',
            'isMileageSubscriptionReject': 'false',
            'page': page            # 페이지
        }

        return urllib.parse.urlencode(params)

    def innerHTML(s, sl=0):
        ret = ''
        for i in s.contents[sl:]:
            if i is str:
                ret += i    .strip()
            else:
                ret += str(i)
        return ret 
    
    def fText(s):
        if len(s):
            return innerHTML(s[0]).strip()
        return ''
    
    retList = []
    colSet = set()
    page = 1

    while 1:
        try:
            # 아이프레임의 영역으로 접근
            f = urllib.request.urlopen("http://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?" + makeArgs(code, page))
            data = f.read().decode('utf-8')

        # 에러뜨면 종료
        except Exception as e:
            print(e)
            break

        soup = bs4.BeautifulSoup(re.sub("&#(?![0-9])", "", data), "html.parser")

        # 한줄 평점 li 을 list 형태로 가지고 있는다.
        cs = soup.select(".score_result li")

        # 평점 내용이 없으면, 삭제
        if not len(cs):
            break

        # <li> ~ </li> 내용들을 for 구문으로 하나씩 접근
        for link in cs:
            try:
                url = link.select('.score_reple em a')[0].get('onclick')
            except:
                print(page)
                print(data)
                raise ""

            m = re.search('[0-9]+', url)

            if m:
                url = m.group(0)
            else:
                url = ''

            if url in colSet:
                return retList
            
            # 집합에 url 추가
            colSet.add(url)
            cont = fText(link.select('.score_reple p'))             # 리뷰쪽 태그 추출
            cont = re.sub('<span [^>]+>.+?</span>', '', cont)       # 리뷰만 추출
            retList.append(cont)                                    # 리뷰 append
        page += 1

    return retList

def fetch(param):
    rank = int(param.split("&")[0])
    code = int(param.split("&")[1])

    rs = getComments(code)

    # TXT 파일 저장
    path = os.path.join(os.getcwd(), "pages", "static", "File", "Review", "movie_" + rank + ".txt")
    reviewFile = open(path, "w", encoding="UTF-8")

    for index, comment in enumerate(rs):
        reviewFile.write("{}".format(comment.replace("'", "''").replace("\\", "\\\\")))

    reviewFile.write('\n')
    reviewFile.close()
    time.sleep(1)
    
# ajax 로 리턴값이 존재하야 함...
def getMovieReviews(request):
    path = os.path.join(os.getcwd(), "pages", "static", "File", "Review", "movie_1.txt")
    
    # Json 파일이 존재
    if os.path.isfile(path) == True:
        print()
    # Json 파일이 미존재
    else:
        movieInfo_PATH = os.path.join(os.getcwd(), "pages", "static", "File", "movieInfo.json")
        mif = open(movieInfo_PATH, encoding='UTF-8')
        mif_json = json.load(mif)

        # 스레드 병렬처리, 해당 코드값으로 리뷰내용 크롤
        with ThreadPoolExecutor(max_workers=4) as executor:
            for index in range(1, 11):
                rank = mif_json[str(index)]["ranking"]
                code = mif_json[str(index)]["code"]
                param = str(rank) + "&" + str(code)
                executor.submit(fetch, param)
    
    return JsonResponse({}, safe=False)

@csrf_exempt
def getStory(request):
    # 해당 넘버 가지고옴, (= 박스오피스 순위, rank)
    rank = request.GET.get('number', None)
    case = request.GET.get('case',None)
    
    dtm_case = str()

    if case == 'story':
        dtm_case = '내용'

    elif case == 'sound':
        dtm_case = 'OST'

    elif case == 'act':
        dtm_case = '배우'

    title = str()
    reviews = dict()

    # rank 에서 타이틀을 들고온다.
    with open(os.path.join(os.getcwd(), "pages", "static", "File", "movieInfo.json"), encoding='UTF-8') as jFile:
        loadData = json.load(jFile)

        for index in range(1, 11):
            if str(loadData[str(index)]["ranking"]) == str(rank):
                title = str(loadData[str(index)]["title"])
                break
    
    # 해당 리뷰 문장들을 들고온다.
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "pages", "static", "File", "Classification")):
        for f in files:
            if f.split("_DTM")[0] == title:
                if f.split("&&")[1].split(".")[0] == dtm_case:
                    with open(root + "\\" + f, "r", encoding="UTF-8") as rf:
                        lines = rf.readlines()

                        for index, line in enumerate(lines):  
                            reviewNSenti = OrderedDict()
                            reviews[index+1] = reviewNSenti

                            senti = line.split("$$")[0]
                            txt = line.split("$$")[1]
                            txt = txt[:len(txt)-1]

                            reviewNSenti['text'] = txt
                            reviewNSenti['senti'] = senti

    return JsonResponse(reviews)

def getMovieDetailInfo(requests):
    code = requests.GET.get('code', None)
    m_info = mr.get_movieDetail(code)
    # pprint(m_info)

    return JsonResponse(m_info, safe=False)