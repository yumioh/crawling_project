import re
import pandas as pd
import csvfile

newsFilePath = './Tesla_Project/data/merge/'
newsFileName = 'tesla_news_tokenization'

#테슬라 뉴스 dataFrame
words_df = csvfile.read_csv(newsFilePath, newsFileName)
words_df = pd.DataFrame(words_df)

print(words_df[:10])

words_df['pos_content'] = words_df['pos_content'].apply(eval)

print(words_df['pos_content'][:5])