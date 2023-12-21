import os
import pandas as pd
from konlpy.tag import Mecab

# 기존 PATH 환경변수 값을 가져옵니다.
existing_path = os.environ.get('PATH', '')

# 추가할 디렉토리를 설정합니다.
new_path = 'C:/mecab/bin'

# PATH 환경변수에 새 디렉토리를 추가합니다.
# os.environ['PATH'] = new_path + os.pathsep + existing_path
print(os.environ['PATH'] )

mecab = Mecab('C:\mecab\share\mecab-ko-dic')

#기사 및 주식 데이터 불려오기
newsFilePath = './data/samsung_2308.csv'
stockFilePath = './data/samsung_stocks_2308.csv'
saveMerge = './data/samsung_merge.csv'
saveReactivity = './data/reactivity.csv'
saveCategory = './data/category.csv'

#뉴스 데이터(header가 없어 추가)
newsData = pd.read_csv(newsFilePath, header = None, names= ['날짜','제목','내용','분야','반응갯수'])

#주식 데이터
stocksData = pd.read_csv(stockFilePath)

#-------------------- 뉴스 데이터 정리 -----------------------------------

#문자열을 날짜타입으로 변경
newsData['날짜'] = pd.to_datetime(newsData['날짜'], format='%Y.%m.%d.')

#전체기사 일자별로 카운트하여 데이터프레임으로 만들기
news_total_count = pd.DataFrame(newsData.groupby(['날짜']).count()['내용'])

# #본문 결측지 제거:
newsData = newsData.dropna(axis=0)
#print(newsData['내용'])

# #기사 본문 중에 '삼성'이 들어간 기사만 추출
samsungNews = newsData[newsData['내용'].str.contains('삼성')]
#print(samsungNews)

#삼성뉴스만 날짜별로 개수 뽑음
samsung_cnt = pd.DataFrame(samsungNews.groupby(['날짜']).count()['내용'])

#-------------------- 주식 데이터 정리 -----------------------------------

#문자열을 날짜타입으로 변경
stocksData['날짜'] = pd.to_datetime(stocksData['날짜'], format='%Y-%m-%d')
#print(stocksData['날짜'])

#삼성뉴스 데이터와 삼성 주식 데이터 합치기
samsungStocks = pd.DataFrame(stocksData[['날짜','종가','거래량']])
# print(samsungStocks)

#날짜별로 정렬
samsungStocks = samsungStocks.sort_values(by='날짜')

#주가와 뉴스 데이터 합치기
mergeData = pd.merge(samsungStocks, samsung_cnt, on='날짜')

#-------------------- 데이터 통계 -----------------------------------

#본문시가별 백분위
mergeData['본문백분위']= (mergeData['내용'] / mergeData['내용'].sum()) * 100
#삼성전자 주가백분위
mergeData['삼성전자 주가백분위'] = (mergeData['종가'] / mergeData['종가'].sum()) * 100

# #인덱스 날짜로 변경
mergeData = mergeData.set_index('날짜')

mergeData.to_csv(saveMerge)

#-------------------- 관심도, 카테고리 데이터 통계 -----------------------------------
#삼성전자 날짜별 반응갯수
reactivity = pd.DataFrame(samsungNews.groupby(['날짜']).count()['반응갯수'])

#카테고리별 갯수
category = pd.DataFrame(samsungNews['분야'].value_counts())
print(category)

reactivity.to_csv(saveReactivity)
category.to_csv(saveCategory)

#-------------------- 워드 클라우드 만들기 위한 불용어 처리  -----------------------------------
# '내용' 열의 각 행에 대해 키워드 제거
# for keyword in stop_words:
#     newsData['내용'] = newsData['내용'].str.replace(keyword, '')
# newsData['내용']

# nltk의 punkt 데이터 다운로드
#nltk.download('punkt')

# 불용어 설정
stop_words = ['연합뉴스', 'yna', 'co', 'kr', 'DB', 'DB 금지', 'co.kr', '섹션', '분류', '서울', '(=)', '재판매', '기자', '구독', '금지' , '및',
              '제공', '올해', '3일', '재배포', '및', '무단', 'reserved', 'right', '등']

# newsData의 '내용' 컬럼에서 텍스트 가져오기
text = ' '.join(newsData['내용'].astype(str))

mecab = Mecab()
print(mecab.pos(newsData['내용']))


#'내용' 열의 각 행에 대해 키워드 제거
# for keyword in stop_words:
#     newsData['내용'] = newsData['내용'].str.replace(keyword, '')
# newsData['내용']

# 단어 토큰화
# word_tokens = word_tokenize(text)

# # 불용어 제거
# result = [word for word in word_tokens if word not in stop_words]
        
# print(word_tokenize, "/n")
# print(result)

# 결과를 파일로 저장
# with open('./data/result.txt', 'w', encoding='utf-8') as file:
#     file.write(' '.join(result))