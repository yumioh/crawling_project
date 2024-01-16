import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csvfile

# 전처리, 토큰화 된 테슬라 뉴스 데이터를 lda를 통해 추출한 토픽을 추출
# 해당하는 토픽의 일자찾기 
# 일자에 해당하는 거개량 찾기 

print("---------------------테슬라 뉴스 데이터 토픽별 날짜 추출 ------------------------")

fsilePath = './Tesla_Project/data/merge/'
newsFileName = 'tesla_news_topics'

#테슬라 뉴스 dataFrame
words_df = pd.DataFrame()
words_df = csvfile.read_csv(fsilePath, newsFileName)

#datetime으로 타입 변환
words_df['날짜'] = pd.to_datetime(words_df['날짜'])

# 해당하는 토픽 
top_topic = '엑'

# nouns_content에서 해당하는 토픽행만 추출
filtered_rows = words_df[words_df['nouns_content'].str.contains(top_topic, case=False, na=False)]

# nouns_content에서 토픽에 해당한 날짜만 추출
filtered_rows_date = filtered_rows['날짜'].dt.strftime('%Y-%m-%d').unique()
#print(filtered_rows_date)

print("---------------------해당하는 토픽의 테슬라 주식 거래량 추출 ------------------------")

# 토픽에 해당한 날짜의 거래량 추출 

fsilePath = './Tesla_Project/data/merge/'
stockFileName = 'merge_stock_data'

#테슬라 주식 dataFrame
stocks_df = pd.DataFrame()
stocks_df = csvfile.read_csv(fsilePath, stockFileName)

#datetime으로 타입 변환
stocks_df['날짜'] = pd.to_datetime(stocks_df['날짜'])
#print('주식 데이터 shape : ', stocks_df.shape)

#거래량 M를 제외한 숫자로만 표기
stocks_df['거래량'] = pd.to_numeric(stocks_df['거래량'].str.replace('M', ''))

topics_date = filtered_rows_date.tolist()

# nouns_content에서 해당하는 토픽행만 추출
filtered_stock_rows = stocks_df[stocks_df['날짜'].isin(topics_date)]

# nouns_content에서 토픽에 해당한 날짜만 추출
print(filtered_stock_rows[['날짜', '거래량']].shape)

print("---------------------테슬라 전체 주식 거래량 그래프 ------------------------")
# mergeFilePath = './Tesla_Project/data/merge/'
# stockFileName = 'merge_stock_data'

# #테슬라 주식 dataFrame
# stocks_df = pd.DataFrame()
# stocks_df = csvfile.read_csv(mergeFilePath, stockFileName)

# #datetime으로 타입 변환
# stocks_df['날짜'] = pd.to_datetime(stocks_df['날짜'])
# #stocks_date = stocks_df['날짜'].sort_values(['날짜'], ascending=False )

# #거래량 M를 제외한 숫자로만 표기습을 진행함
# stocks_df['거래량'] = pd.to_numeric(stocks_df['거래량'].str.replace('M', ''))


print("---------------------해당하는 토픽 날짜의 주식 거래량 그래프 ------------------------")
# 차트 위치
fig_total = plt.figure(figsize=(12, 6)) # 차트 생성 및 사이즈 설정

# 주식 거래량 전체 데이터 
ax = fig_total.add_subplot(1, 1, 1)
ax.bar(stocks_df['날짜'], stocks_df['거래량'], label='Stock Volume', color='black')
ax.set_title('Volume for Topic : X', fontsize=20)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('News Volume', fontsize=14)
ax.legend(fontsize=12, loc='best')

# 해당하는 토픽 거래량 ex. 테슬라
ax2 = ax.twinx()
ax2.bar(filtered_stock_rows['날짜'], filtered_stock_rows['거래량'], label='Tesla Topic', color='red')
ax2.set_ylabel('Tesla Topic', fontsize=14)

# x 축의 날짜 형식 설정
date_format = mdates.DateFormatter("%Y-%m")
ax.xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

# 범례 추가
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines, labels, fontsize=12, loc='upper left')
ax2.legend(lines2, labels2, fontsize=12, loc='upper right')

#그래프 파일 저장
plt.savefig("./Tesla_Project/data/img/X.png", format = 'png')

# 그래프 보기
plt.tight_layout() 
plt.show()
