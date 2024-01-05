import os
import pandas as pd
from konlpy.tag import Okt
from collections import Counter

# 기존 PATH 환경변수 값을 가져옵니다.
existing_path = os.environ.get('PATH', '')

#mecab = Mecab('C:\mecab\share\mecab-ko-dic')

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
#print(category)

reactivity.to_csv(saveReactivity)
category.to_csv(saveCategory)

#-------------------- 워드 클라우드 만들기 위한 불용어 처리  -----------------------------------
# 불용어 설정
stop_words = ['연합뉴스', 'yna', 'co', 'kr', 'DB', 'DB 금지', 'co.kr', '섹션', '분류', '서울', '(=)', '재판매', '기자', '구독', '금지' , '및', '또', '통해',
              '제공', '올해', '3일', '재배포', '및', '무단', 'reserved', 'right', '등', '특파원', '지난', '현지', '시간', '의', '최근', '현재', '뒤', '우리',
              '사람', '경우', '이', '은', '수', '더', '오전', '당시', '경우', '기존', '지금', '포함', '이유', '것 말', '때', '위해', '를', '국민', '힘', '도',
              '중', '내년', '그', '후','것 말', '다시', '대한', '대해', '불어', '과', '관련', '설명', '해', '위', '문', '내', '달', '시', '말', '인', '정']

stop_words2 = ['연합뉴스', 'yna', 'co', 'kr', 'DB', 'DB 금지', 'co.kr', '섹션', '분류', '서울', '(=)', '재판매', '기자', '구독', '금지' , '및', '또', '통해',
              '제공', '올해', '3일', '재배포', '및', '무단', 'reserved', 'right', '등', '특파원', '지난', '현지', '시간', '의', '최근', '현재', '뒤', '우리',
              '사람', '경우', '수', '있는', '있다', '하고', '있다', '바 있다', 'South Korea', '은', '있도록', '밝혔다', '16일', '16일', '이후', '오후', '이번', 
              '오전', '을', '위해', '는', '중', '이', '말했다', '에', '그', '한다', '했다', '를', '도', '해', '대한', '날', '가', 'DN', '것', '전', '들', '로', 'A씨']

# 1.단순 불용어처리 후 워드 클라우드 만들기
#'내용' 열의 각 행에 대해 키워드 제거
for keyword in stop_words2:
    newsData['내용'] = newsData['내용'].str.replace(keyword, '')

# 날짜 포함 파일 저장
newsData[['내용','날짜']].to_csv('./data/content.csv', encoding='utf-8')

# 2.형태소 분석을 이용한 워드 클라우드 만들기
#'내용' 열의 각 행에 대해 키워드 제거
# for keyword in stop_words:
#     newsData['내용'] = newsData['내용'].str.replace(keyword, '')

# #형태소 분석과 명사만 추출
# #okt를 사용하는 이유 : 속도가 빠르고 품사태그가 간단하며, 조사나 어미 등 필요한 정보를 쉽게 활용 가능
# okt = Okt()
# newsData['명사'] = newsData['내용'].apply(lambda x: ' '.join(okt.nouns(str(x))))

# #파일 저장
# newsData['명사'].to_csv('./data/okt.csv', index=False, header=False, encoding='utf-8')


