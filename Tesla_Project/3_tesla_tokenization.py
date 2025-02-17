import pandas as pd
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from konlpy.tag import Mecab
import csvfile, cleaningData
from gensim import corpora 
import time

# 상위 10개 단어 추출
def word_counter(wordArr):
    all_word = [word for words in wordArr for word in words]
    word_count = Counter(all_word)
    most_commos_words = word_count.most_common(20)
    return most_commos_words

#mecab 실행
#existing_path = os.environ.get('PATH', '')
# 추가할 디렉토리를 설정
#new_path = r'C:\mecab\bin'
# PATH 환경변수에 새 디렉토리를 추가
#os.environ['PATH'] = new_path + os.pathsep + existing_path
# 변경된 PATH 값을 확인
#print(os.environ['PATH'])

print("---------------------Tokenization------------------------")

#전처리된 파일 읽어 오기 
filepath = './Tesla_Project/data/merge/'
prepro_fileName = 'telsa_preprosessing'
words_df = csvfile.read_csv(filepath, prepro_fileName)
#print(f'전처리한 날짜, 본문 shape : ', words_df.shape)

#공백기준으로 본문 내용 split
words_df['splitted_content'] = words_df['content_data'].str.split()
print("공백기준으로 content split :", words_df[:5])

start_time = time.time()
print("---------------------품사부착 (PoS Tagging)------------------------")
#명사만 추출 
#VSCODE시 Mecab에 dic path 넣어주기
def pos_nouns_tag(df) :
  mecab = Mecab('C:\mecab\share\mecab-ko-dic')
  return df.apply(lambda x: [mecab.nouns(word) for word in x]) #명사만 추출

words_df['pos_content'] = pos_nouns_tag(words_df['splitted_content'])
print("명사 pos taging : ", words_df[['날짜','pos_content']][:5])

#불용어 처리
words_df['pos_content'] = words_df['pos_content'].map(cleaningData.remove_korean_stopwords)

clean_words = words_df[['날짜','pos_content']]
print('불용어 제거 후 : ', clean_words[:10])

end_time = time.time()
execution_time = (end_time - start_time) / 60
print(f"걸린 시간: {execution_time} 분")

words_df['pos_content'] = words_df['pos_content'].apply(lambda x: list(filter(None, x)))
clean_words = words_df[['날짜', 'pos_content']]
print("빈 리스트 제거: ", clean_words[:5])

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = [word for tokens in clean_words['pos_content'] for word_list in tokens for word in str(word_list).split()]
most_common_words = Counter(most_common_tag).most_common(30)
print("최빈어 조회 : ", most_common_words)

#토큰화한 파일 저장
clean_fileName = 'tesla_news_tokenization'
csvfile.save_file_with(clean_words, filepath, clean_fileName)