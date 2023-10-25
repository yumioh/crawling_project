import twitter
import numpy as np
import pandas as pd
import itertools
import snscrape.modules.twitter as sntwitter
import pandas as pd


start_day = "2022-10-01"
end_day = "2020-10-14"
search_word = "테슬라"
query = search_word + ' since:'+ start_day + ' until:' + end_day


#지정한 기간에서 검색하고자 하는 단어를 포함한 tweet를 가져오기
scraped_twwets = sntwitter.TwitterSearchScraper(query).get_items()
#100개 tweets를 가져오기
sliced_scraped_tweets = itertools.islice(scraped_twwets, 100)
#데이터에 맞게 컬럼명 지정
df = pd.DataFrame(sliced_scraped_tweets)
print(df) 
df.to_csv('python.csv', encoding='utf-8-sig') 