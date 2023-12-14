import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from wordcloud import WordCloud, STOPWORDS

#기사 및 주식 데이터 불려오기
stockFilePath = './data/samsung_stocks_2308.csv'
newsFilePath = './data/samsung_2308.csv'

#뉴스 데이터(header가 없어 추가)
newsData = pd.read_csv(newsFilePath, header = None, names= ['날짜','제목','분야','반응갯수','내용'])

#주식 데이터
stocksData = pd.read_csv(stockFilePath)

#-------------------- 뉴스 데이터 정리 -----------------------------------

#문자열을 날짜타입으로 변경
newsData['날짜'] = pd.to_datetime(newsData['날짜'], format="YYYY.mm.dd")
print(newsData['날짜'])

#전체기사 일자별로 카운트하여 데이터프레임으로 만들기
news_total_count = pd.DataFrame(newsData.groupby(['날짜']).count()['내용'])

#본문 결측지 제거:
newsData = newsData.dropna(axis=0)

#기사 본문 중에 '삼성'이 들어간 기사만 추출
samsungNews = newsData[newsData['내용'].str.contains('삼성')]

#삼성뉴스만 날짜별로 개수 뽑음
samsung_cnt = pd.DataFrame(samsungNews.groupby(['날짜']).count()['내용'])

#-------------------- 주식 데이터 정리 -----------------------------------

#문자열을 날짜타입으로 변경
stocksData['날짜'] = pd.to_datetime(stocksData['날짜'], format='%Y-%m-%d')

#삼성뉴스 데이터와 삼성 주식 데이터 합치기
samsungStocks = pd.DataFrame(stocksData[['날짜','종가','거래량']])

#날짜별로 정렬
samsungStocks = samsungStocks.sort_values(by='날짜')


#주가와 뉴스 데이터 합치기
mergeData = pd.merge(samsungStocks, samsung_cnt, on='날짜')


#-------------------- 데이터 통계 -----------------------------------

#본문시가별 백분위
mergeData['본문백분위']= (mergeData['내용'] / mergeData['내용'].sum()) * 100
#삼성전자 주가백분위
mergeData['삼성전자 주가백분위'] = (mergeData['종가'] / mergeData['종가'].sum()) * 100

#인덱스 날짜로 변경
#mergeData = mergeData.set_index('날짜')

#-------------------- 관심도, 카테고리 데이터 통계 -----------------------------------
#삼성전자 날짜별 반응갯수
reactivity = pd.DataFrame(samsungNews.groupby(['날짜']).count()['반응갯수'])

#카테고리별 갯수
category = pd.DataFrame(samsungNews['분야'].value_counts())

#-------------------- 데이터 시각화 -----------------------------------

# 기사 버즈량 및 주가 비교 시각화
plt.rcParams.update({'font.size': 10, 'font.family': 'NanumGothicBold'})
plt.figure(figsize=(8, 8))
plt.title("기사 버즈량 및 주가 비교", fontsize=20)
plt.xticks(rotation=75)

dates = list(map(lambda n: pd.to_datetime(n).strftime('%Y-%m-%d'), mergeData['날짜']))

#날짜
plt.plot(dates, mergeData['본문백분위'].values, label='버즈량', color ='dodgerblue')
plt.plot(dates, mergeData['삼성전자 주가백분위'].values, label='주가',color='darkorange')

#범례를 그래프의 오른쪽 상단
plt.legend(loc=1)
plt.show()

#일자별 기사 관심도
plt.rcParams.update({'font.size': 10, 'font.family': 'NanumGothicBold'})
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.xticks(rotation=75)
#날짜
dates = list(map(lambda n: pd.to_datetime(n).strftime('%Y-%m-%d'), reactivity.index))

plt.plot(dates, reactivity['반응갯수'].values, label='반응수', marker = 'o', linestyle = 'solid', color='limegreen')
plt.legend(loc=0)
plt.tight_layout() 
plt.show()

#카테고리별 기사량
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.bar(category.index, category['분야'], color='lightskyblue')
plt.tight_layout() 
plt.show()


# wordcloud = WordCloud(max_font_size=200,
#                       font_path='/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
#                       stopwords=STOPWORDS,
#                       background_color='#FFFFFF',
#                       width=1200,
#                       height=800).generate(''.join(samsungNews[samsungNews['날짜']=='2023-08-03']['내용'].values))

# plt.figure(figsize=(20,20))
# plt.imshow(wordcloud)
# plt.tight_layout(pad=0)
# plt.axis('off')
# plt.show()

