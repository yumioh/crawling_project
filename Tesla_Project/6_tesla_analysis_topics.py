from gensim.corpora.dictionary import Dictionary
from gensim.models import TfidfModel, LdaMulticore
import pyLDAvis.gensim_models as gensimvis
import matplotlib.pyplot as plt
import pandas as pd
import csvfile
import time
import pyLDAvis

print("---------------------테슬라 주식 데이터 Dataframe ------------------------")

# 테슬라 주식 데이터 Dataframe
stockFilePath = './Tesla_Project/data/merge/'
stockFileName = 'merge_stock_data'

#테슬라 주식 dataFrame
stocks_df = pd.DataFrame()
stocks_df = csvfile.read_csv(stockFilePath, stockFileName)

#datetime으로 타입 변환
stocks_df['날짜'] = pd.to_datetime(stocks_df['날짜'])
#print('주식 데이터 shape : ', stocks_df.shape)

#거래량 M를 제외한 숫자로만 표기습을 진행함
stocks_df['거래량'] = pd.to_numeric(stocks_df['거래량'].str.replace('M', ''))

#날짜와 거래량 추출 : stock_df
stock_df = stocks_df[['날짜','거래량']]
#print(stock_df[:10])

print("---------------------토픽 처리된 테슬라 Dataframe ------------------------")

topicFilePath = './Tesla_Project/data/merge/'
topicFileName = 'tesla_news_topics'

#테슬라 뉴스 dataFrame
words_df = pd.DataFrame()
words_df = csvfile.read_csv(topicFilePath, topicFileName)

#datetime으로 타입 변환
words_df['날짜'] = pd.to_datetime(words_df['날짜'])

#기사 데이터 날짜별 기사 수 추출
news_cnt= words_df.groupby(words_df['날짜']).count()['nouns_content']
#print(news_cnt_daily)

news_count = news_cnt.reset_index()
news_count.columns = ['날짜', '기사갯수']
print(news_count.info())

print("---------------------토픽처리된 LDA 모델링------------------------")

# LDA 데이터를 csv 파일 저장
def save_topics_csv(lda, num_topics, save_result_to: str = './Tesla_Project/data/merge/lda_by_topics.csv'):
  # LDA 모델의 토픽 리스트를 csv파일로 저장
  topics = pd.Series(lda.print_topics(num_topics=num_topics, num_words=10))
  topics.to_csv(save_result_to, mode='w', encoding='utf-8', header=['list'], index_label='topic')

#딕셔너리 생성 : 다시하기 
dic = Dictionary()
#clean_words = words_df['nouns_content']
clean_words = words_df['nouns_content'].apply(lambda x: str(x).split())
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
                    workers=6)

  for t in lda.print_topics():
    print(t[0],":",t[1])

  #로그 혼란도(0에 가까울수록 성능이 높음)
  #lda.log_perplexity(corpus_TFIDF)

  #다양도(1에 가까울 수록 성능이 높음)
#   topn = 25
#   top_words = set()

#   for topic in range(lda.num_topics):
#       for word, prob in lda.show_topic(topic, topn=topn):
#           top_words.add(word)
#   len(top_words) / (lda.num_topics * topn)
  
  #csv 파일 저장
  save_topics_csv(lda, n)

  #LDA 시각화
  vis = gensimvis.prepare(lda, corpus_TFIDF, id2word)
  pyLDAvis.save_html(vis, './Tesla_Project/data/lda_visualization.html')

  end_time = time.time()
  execution_time = end_time - start_time
  print(f"실행 시간: {execution_time} 초")