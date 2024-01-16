import pandas as pd
from collections import Counter
from konlpy.tag import Mecab
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import csvfile, cleaningData
import time

# 상위 10개 단어 추출
def word_counter(wordArr):
    all_word = [word for words in wordArr for word in words]
    word_count = Counter(all_word)
    most_commos_words = word_count.most_common(20)
    return most_commos_words

print("---------------------Tokenization------------------------")

#전처리된 파일 읽어 오기 
filepath = './Tesla_Project/data/merge/'
prepro_fileName = 'twit_Preprosessing'
words_df = csvfile.read_csv(filepath, prepro_fileName)
print(f'전처리한 날짜, 본문 shape : ', words_df.shape)

#공백으로 본문 내용 split
words_list = words_df['content_data'].str.split()
print("상위 10개 단어 추출", word_counter(words_list))

#각 텍스트에 대한 토큰화 수행
#words_df['content_data'] = words_df['content_data'].apply(lambda x: word_tokenize(x))
#print(words_df[:20])

#불용어 처리 
#nltk 불용어 리스트 데이터 설치
#설치 위치 C:\Users\aline\AppData\Roaming\nltk_data
#nltk.download()
#nltk.download('stopwords')

#불용어/ 토큰화 처리
words_df['content_data'] = words_df['content_data'].apply(cleaningData.remove_stopwords_and_tokenize)
print('불용어/ 토큰화 처리 : ', words_df[:30], words_df.shape)

print("---------------------품사부착 (PoS Tagging)------------------------")
#nltk.download('averaged_perceptron_tagger')
#content_data 열의 토큰에 대한 품사 태깅 수행
taggedTokens = words_df['content_data'].apply(lambda x: pos_tag(x))

# 명사만 추출
words_df['nouns'] = taggedTokens.apply(lambda x: [word for word, tag in x if tag.startswith('NN')])
print(words_df[:20])

# # 최빈어를 조회
# clean_words = words_df['nouns']
# most_common_tag = []
# for token in clean_words:
#   most_common_tag += token
# print(Counter(most_common_tag).most_common(30))

clean_fileName = 'twit_cleaninngWords'
csvfile.save_file(words_df[['날짜','nouns']], filepath, clean_fileName)