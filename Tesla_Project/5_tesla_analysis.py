from gensim.corpora.dictionary import Dictionary
from gensim.models import TfidfModel, LdaMulticore
import pyLDAvis.gensim_models as gensimvis
import pandas as pd
import csvfile, modeling
import time
import pyLDAvis

print("---------------------테슬라 주식 데이터 Dataframe ------------------------")

# 테슬라 주식 데이터 Dataframe
# 전체 날짜
#테슬라 주식 병합 (2020 ~ 20203.09)
stockfilepath = './Tesla_Project/data/'
stockSaveFilepath = './Tesla_Project/data/merge/'
stockFileName = 'merge_stock_data'
#csvfile.stock_merge_csv(stockfilepath, stockSaveFilepath, stockFileName)

mergeFilePath = './Tesla_Project/data/merge/'

#테슬라 주식 dataFrame
stocks_df = pd.DataFrame()
stocks_df = csvfile.read_csv(mergeFilePath, stockFileName)

#datetime으로 타입 변환
stocks_df['날짜'] = pd.to_datetime(stocks_df['날짜'])
#print('주식 데이터 shape : ', stocks_df.shape)

#거래량 M를 제외한 숫자로만 표기습을 진행함
stocks_df['거래량'] = pd.to_numeric(stocks_df['거래량'].str.replace('M', ''))

#날짜와 거래량 추출 : stock_df
stock_df = stocks_df[['날짜','거래량']]
#print(stock_df[:10])

print("---------------------테슬라 기사 데이터 Dataframe ------------------------")

newsFilePath = './Tesla_Project/data/merge/'
newsFileName = 'tesla_news_topics'
#tesla_news_topics

#테슬라 뉴스 dataFrame
words_df = pd.DataFrame()
words_df = csvfile.read_csv(newsFilePath, newsFileName)

#주식 데이터와 열 이름 통일
words_df = words_df.rename(columns={'date' : '날짜'})

#datetime으로 타입 변환
words_df['날짜'] = pd.to_datetime(words_df['날짜'])

#기사 데이터 날짜별 기사 수 추출 : 1291
news_cnt_daily = words_df.groupby(words_df['날짜']).count()['pos_content']
print("기사 데이터 날짜별 기사 수", news_cnt_daily.shape)

daily_news_count = news_cnt_daily.reset_index()
daily_news_count.columns = ['날짜', '기사갯수']
print("daily_news_count : ", daily_news_count.info())

print("---------------------기사와 주식 병합 Dataframe ------------------------")
# 주식 데이터와 기사 데이터를 병합
data_df = pd.merge(stock_df, daily_news_count, how='outer', on='날짜')
#print(data_df.info())

#결측지 제거 : 주가가 없는 날짜 제거 (주말)
data_df = data_df.dropna()
print(data_df.info())

#날짜별 기사개수/주식거래량 수
stock_daily_volume = data_df['거래량']
news_daily_cnt = data_df['기사갯수']

#총 기사개수/거래량 수
#stock_volume = data_df['거래량'].sum()
#news_cnt = data_df['기사갯수'].sum()
#print('2023년 기사 개수 :', news_cnt)

print('날짜별 기사개수 : {}, 날짜별 주식 거래양 수 : {}'.format(news_daily_cnt, stock_daily_volume))

print("---------------------라쏘 회귀 ------------------------")
# 라쏘 회귀 : 선형 회귀으로 비용함수인 mse를 최소하하는 방향으로 머신러닝 모델이 학습을 진행
# TF-IDF는 단어의 빈도수(TF)와 단어가 들어있는 문서 수의 반비례 하는 수(IDF)를 곱한값
# 기사 수(news_cnt) : X, 주식거래량(stock_volume) : y
# 각 데이터를 StandardScaler/MinMaxS1caler로 표준화하여 모델링

X = data_df['기사갯수'].values.reshape(-1,1)
y = data_df['거래량'].values.reshape(-1,1)
n_splits = 5
alphas = [0.001, 0.005, 0.01, 0.1, 1, 10, 100]

# 최적의 alpha 찾기
#modeling.optimize_alpha(X, y, alphas, n_splits)

alpha = 0.001 # K-FOLD로 구한 alpha값

#TODO : 라쏘회귀 그래프 그림 그리기
#라쏘회귀 실행
modeling.LASSO_KFold(X, y, alpha, n_splits)
#modeling.LASSO(X, y, n_splits)
#modeling.new_lasso(X, y, n_splits)

print("---------------------LDA 모델링------------------------")

#딕셔너리 생성 : 다시하기 
dic = Dictionary()
clean_words = words_df['nouns_content']
print('clean dataframe', clean_words[:10])
clean_words = words_df['nouns_content'].apply(lambda x: str(x).split())
id2word = Dictionary(clean_words)
print("id2word 처리후 : ", list(id2word.items())[:10])


for key, value in id2word.items():
    if isinstance(value, list):
        # 리스트 안에 있는 경우 리스트의 첫 번째 요소를 사용
        id2word[key] = value[0]

# 수정된 id2word 출력
print("id2word 처리후 : ", list(id2word.items())[:10])

corpus_TDM = []
for doc in clean_words:
  #print(doc)
  result = id2word.doc2bow(doc)
  corpus_TDM.append(result)

#tfidf로 벡터화 적용
tfidf = TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]

#LDA 모델링
def save_topics_csv(lda, num_topics, save_result_to: str = './Tesla_Project/data/lda.csv'):
  # LDA 모델의 토픽 리스트를 csv파일로 저장
  topics = pd.Series(lda.print_topics(num_topics=num_topics, num_words=10))
  topics.to_csv(save_result_to, mode='w', encoding='utf-8', header=['list'], index_label='topic')

# if __name__ == '__main__':
#   start_time = time.time()
#   n = 30 #토픽의 개수
#   #worker(프로세스 수),토픽수.passes(매개변수) 수를 조정하여 
#   #속도를 높일 수 있음
#   lda = LdaMulticore(corpus=corpus_TFIDF,
#                     id2word=id2word,
#                     num_topics=n,
#                     random_state=100,
#                     passes=15,
#                     workers=6)

#   for t in lda.print_topics():
#     print(t[0],":",t[1])

#   #로그 혼란도(0에 가까울수록 성능이 높음)
#   lda.log_perplexity(corpus_TFIDF)

#   #다양도(1에 가까울 수록 성능이 높음)
#   topn = 25
#   top_words = set()

#   for topic in range(lda.num_topics):
#       for word, prob in lda.show_topic(topic, topn=topn):
#           top_words.add(word)
#   len(top_words) / (lda.num_topics * topn)

#   #LDA 시각화
#   vis = gensimvis.prepare(lda, corpus_TFIDF, id2word)
#   pyLDAvis.save_html(vis, './Tesla_Project/data/lda_visualization_before.html')
  
#   #csv 파일 저장
#   save_topics_csv(lda, n)
#   end_time = time.time()

  # # execution_time = end_time - start_time
  # print(f"실행 시간: {execution_time} 초")