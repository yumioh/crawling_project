import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import csvfile

# ldaFilePath = './Tesla_Project/data/merge/'
# ldaFileName = '2023_lda_topics'

# #lda 모델링 dataframe
# lda_df = pd.DataFrame()
# lda_df = csvfile.read_csv(ldaFilePath, ldaFileName)

mergeFilePath = './Tesla_Project/data/merge/'
stockFileName = 'merge_stock_data'

#테슬라 주식 dataFrame
stocks_df = pd.DataFrame()
stocks_df = csvfile.read_csv(mergeFilePath, stockFileName)

#datetime으로 타입 변환
stocks_df['날짜'] = pd.to_datetime(stocks_df['날짜'])
#stocks_date = stocks_df['날짜'].sort_values(['날짜'], ascending=False )

#거래량 M를 제외한 숫자로만 표기습을 진행함
stocks_df['거래량'] = pd.to_numeric(stocks_df['거래량'].str.replace('M', ''))

#날짜와 거래량 추출 : stock_df
stock_df = stocks_df[['날짜','거래량']]

filePath = './Tesla_Project/data/merge/'
fileName = 'stock_news_mergeData'

#테슬라 기사수와 거래량 dataFrame
data_df = pd.DataFrame()
data_df = csvfile.read_csv(filePath, fileName)

#datetime으로 타입 변환
data_df['날짜'] = pd.to_datetime(data_df['날짜'])

data_df.set_index('날짜', inplace=True)

print("---------------------1. 날짜별 뉴스 볼륨 그래프 ------------------------")
# 차트 위치
fig = plt.figure(figsize=(12, 6)) # 차트 생성 및 사이즈 설정
ax = fig.add_subplot(1,2,1) # subplot 생성

#x,y축 그래프 그리기 
ax.bar(data_df.index, data_df['기사갯수'], label='tesla Volume', color='skyblue') # 인덱스가 x축, 거래량이 y축인 그래프를 그려줍니다.

ax.set_title('News Volume Chart', fontsize=20) # 타이틀 설정
ax.set_ylabel('News Volume ', fontsize=14) # x축 설정
ax.set_xlabel('Date', fontsize=14) # y축 설정
#적절한 위치에 알아서 범례가 생김
ax.legend(fontsize=12, loc='best')

# x 축의 날짜 형식 설정
date_format = mdates.DateFormatter("%Y-%m")
ax.xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)
#월간격설정
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))

print("---------------------2. 날짜별 거래량 그래프 ------------------------")
# 차트 위치
ax = fig.add_subplot(1,2,2) # subplot 생성

#x,y축 그래프 그리기 
ax.bar(data_df.index, data_df['거래량'], label='tesla Volume', color='red') # 인덱스가 x축, 거래량이 y축인 그래프를 그려줍니다.

ax.set_title('Tesla Stock Volume Chart', fontsize=20) # 타이틀 설정
ax.set_ylabel('Stock Volume', fontsize=14) # x축 설정
ax.set_xlabel('Date', fontsize=14) # y축 설정
#적절한 위치에 알아서 범례가 생김
ax.legend(fontsize=12, loc='best')

# x 축의 날짜 형식 설정
date_format = mdates.DateFormatter("%Y-%m")
ax.xaxis.set_major_formatter(date_format)
#월간격설정
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))

plt.xticks(rotation=45)
plt.tight_layout() 
plt.savefig("./Tesla_Project/data/img/total_stock_daily_graph2.png", format="png")
#plt.show()

print("---------------------3. 날짜별 거래량과 주식량 그래프 ------------------------")
fig, ax = plt.subplots(figsize=(12, 6))

# 첫 번째 서브플롯
#x,y축 그래프 그리기 
ax.bar(data_df.index, data_df['기사갯수'], label='News Volume', color='skyblue')
# 두 번째 서브플롯 (오른쪽 y축)
#x,y축 그래프 그리기 
ax2 = ax.twinx()
ax2.bar(data_df.index, data_df['거래량'], label='Stock Volume', color='red')

# 서브플롯 설정
for axis in [ax, ax2]:
    axis.set_ylabel('Volume', fontsize=14)
    axis.legend(fontsize=12, loc='best')

ax.set_title('News Volume and Stock Volume Chart', fontsize=20)
ax.set_xlabel('Date', fontsize=14)

ax.set_ylabel('News Volume', fontsize=14)
ax2.set_ylabel('Stock Volume', fontsize=14)

#기울기
plt.xticks(rotation=45)
plt.tight_layout()
#그래프 출력
plt.savefig("./Tesla_Project/data/img/total_stock_news_graph.png", format="png")
plt.show()

print("---------------------3.주식, 관련없는 토픽 제외한 LDA 그래프 ------------------------")
#tesla analysis 코드에 있음 

plt.figure(figsize=(12, 6))
plt.plot(data_df.index, data_df['기사갯수'], label='News Volume', color='skyblue')
plt.plot(data_df.index, data_df['거래량'], label='Stock Volume', color='red')
plt.xlabel('Date', fontsize=14)
plt.ylabel('Stock Volume')
plt.ylabel('News Volume')
plt.title('News Volume and Stock Volume Chart', fontsize=20)
plt.legend()

#기울기
plt.xticks(rotation=45)
plt.tight_layout()
#그래프 출력
plt.savefig("./Tesla_Project/data/img/total_stock_news_graph2.png", format="png")
plt.show()