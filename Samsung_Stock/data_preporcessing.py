import pandas as pd

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

# #-------------------- 관심도, 카테고리 데이터 통계 -----------------------------------
#삼성전자 날짜별 반응갯수
reactivity = pd.DataFrame(samsungNews.groupby(['날짜']).count()['반응갯수'])

#카테고리별 갯수
category = pd.DataFrame(samsungNews['분야'].value_counts())

reactivity.to_csv(saveReactivity)
category.to_csv(saveCategory)