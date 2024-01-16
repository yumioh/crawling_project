from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel, TfidfModel
from gensim.models import LdaMulticore
import pandas as pd
import numpy as np
import csvfile, modeling
import time

print("--------------------- 트위터 데이터 Dataframe ------------------------")

filepath = './Tesla_Project/data/merge/'
fileName = 'twit_cleaninngWords'

#twit dataFrame
twit_df = pd.DataFrame()
twit_df = csvfile.read_csv(filepath, fileName)
print(f'처리 전 : ', twit_df.shape)

# 'nouns' 열에 대해 빈 리스트를 제거
# twit_df = twit_df[twit_df['nouns'].apply(lambda x: len(x) > 0)]
# print(f'nouns 열에 공백 제거 후 : ', twit_df.shape)


#기사 데이터 날짜별 기사 수
twit_cnt = twit_df.groupby(twit_df['날짜']).count()['nouns']
#print(twit_cnt[:10])

twit_cnt = twit_cnt.reset_index()
twit_cnt.columns = ['날짜', 'twit수']

twit_cnt['날짜'] = pd.to_datetime(twit_cnt['날짜'])

print(twit_cnt.info())

print("---------------------테슬라 기사 데이터 Dataframe ------------------------")
stockFilePath = './Tesla_Project/data/merge/'
stockFileName = 'merge_stock_data'

#테슬라 주식 dataFrame
stocks_df = pd.DataFrame()
stocks_df = csvfile.read_csv(stockFilePath, stockFileName)

#datetime으로 타입 변환
stocks_df['날짜'] = pd.to_datetime(stocks_df['날짜'])

#거래량 M/B를 제외한 숫자로만 표기습을 진행함
stocks_df['거래량'] = pd.to_numeric(stocks_df['거래량'].str.replace('M', ''))
#print(news_cnt_daily)

#날짜와 거래량 추출 : stock_df
stock_df = stocks_df[['날짜','거래량']]
print(stock_df[:10])

print("---------------------트위터와 주식 병합 Dataframe ------------------------")
# 주식 거래량과 twit 데이터 병합
print(twit_cnt[:10])
data_df = pd.merge(twit_cnt, stock_df , how='outer', on='날짜')
#print(data_df[:50])

#결측지 제거 : 주가가 없는 날짜 제거 (주말)
data_df = data_df.dropna()
print(data_df.info())

#날짜별 기사개수/주식거래량 수
stock_volume = data_df['거래량']
twit_cnt = data_df['twit수']

print("---------------------라쏘 회귀 ------------------------")

X = data_df['거래량'].values.reshape(-1,1)
y = data_df['twit수'].values.reshape(-1,1)
alpha = 0.001
n_splits = 5
alphas = [0.001, 0.01, 0.1, 1, 10, 100]

#라쏘회귀 실행
print(modeling.LASSO_KFold(X, y, alpha, n_splits))

# 최적의 alpha 찾기
print(modeling.optimize_alpha(X, y, alphas, n_splits))

print("---------------------LDA 모델링------------------------")
#딕셔너리 생성 : 다시하기 
dic = Dictionary()
#clean_words = words_df['nouns_content']
clean_words = twit_df['nouns'].apply(lambda x: x.split())
id2word = Dictionary(clean_words)
#print(id2word)

corpus_TDM = []
for doc in clean_words:
  #print(doc)
  result = id2word.doc2bow(doc)
  corpus_TDM.append(result)

#tfidf로 벡터화 적용
tfidf = TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]

#LDA 모델링
if __name__ == '__main__':
  start_time = time.time()
  n = 30 #토픽의 개수
  #worker(프로세스 수),토픽수.passes(매개변수) 수를 조정하여 
  #속도를 높일 수 있음
  lda = LdaMulticore(corpus=corpus_TFIDF,
                    id2word=id2word,
                    num_topics=n,
                    random_state=100,
                    passes=15,
                    workers=10)

  for t in lda.print_topics():
    print(t[0],":",t[1])

  #로그 혼란도(0에 가까울수록 성능이 높음)
  lda.log_perplexity(corpus_TFIDF)
  #print("로그 혼란도", lda.log_perplexity(corpus_TFIDF))

  #다양도(1에 가까울 수록 성능이 높음)
  topn = 5
  top_words = set()

  for topic in range(lda.num_topics):
      for word, prob in lda.show_topic(topic, topn=topn):
          top_words.add(word)
  #print(len(top_words) / (lda.num_topics * topn))
  
  end_time = time.time()
  execution_time = end_time - start_time
  print(f"실행 시간: {execution_time} 초")
