import pandas as pd
import re
import csvfile

stop_words = ['신년', '오바마']

def remove_korean_stopwords(nouns_list):
    return [word for word in nouns_list if word not in stop_words]

data = {'날짜': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04'],
        'pos_content': [['오바마','대통령1','대통령2', []], ['신년','년3','년4'], ['미국인', [],'미국인3','미국인'], ['오바마', '오바마',[]]]}
words_df = pd.DataFrame(data)

words_df['pos_content'] = words_df['pos_content'].map(remove_korean_stopwords)

print(words_df)