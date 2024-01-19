import re
import pandas as pd
import csvfile

newsFilePath = './Tesla_Project/data/merge/'
newsFileName = 'tesla_news_cleaninngWords'

#관련없는 키워드 문서

#테슬라 뉴스 dataFrame
words_df = csvfile.read_csv(newsFilePath, newsFileName)
words_df = pd.DataFrame(words_df)

stock_keywords = ['주식', '주가', '주가지수', '증시', '종목명', '주식시장', '현대자동차', '닛산','네이버','카다시안'
                  '현대차', '기아', '도요타','제주','니콜라','이벤트','머니','논란','스톡옵션','항목','노조'
                  ,'세금','재산','대통령실','지수','자산','과세','아시아','부동산','미쓰','미쓰비시','클럽','오바마']
#tesla_keywords = ['테슬라','이차전지','트위터','엑스','자율주행','반도체','자율','주행','2차','전지']

# 관련 없는 키워드가 포함된 행 삭제하는 함수
def filter_rows_with_keywords(dataframe, keywords):
    pattern = '|'.join(keywords)
    mask = dataframe['nouns_content'].str.contains(pattern, case=False)
    filtered_df = dataframe[~mask]
    return filtered_df

# 주식 관련 키워드가 포함된 행 삭제
filtered_df = filter_rows_with_keywords(words_df, stock_keywords)

# 최종 필터링된 데이터프레임 확인
print(filtered_df[:40])
print(filtered_df.shape)

# 해당하는 토픽 제외된 csv 파일 저장 : 40990
savefilepath = './Tesla_Project/data/merge/'
savefileName = 'tesla_news_topics'
csvfile.save_file(filtered_df, savefilepath, savefileName)

