import re
import pandas as pd
import csvfile

newsFilePath = './Tesla_Project/data/merge/'
newsFileName = 'tesla_news_tokenization'

#테슬라 뉴스 dataFrame
words_df = csvfile.read_csv(newsFilePath, newsFileName)
words_df = pd.DataFrame(words_df)

stock_keywords = ['주식', '주가', '주가지수', '증시', '종목명', '주식시장', '현대자동차', '닛산','네이버','카다시안','협회', '거래', '현금', '테슬라' 
                  '현대차', '기아', '도요타','제주','니콜라','이벤트','머니','논란','스톡옵션','항목','노조', '매출액', '공시', '세액'
                  ,'세금','재산','대통령실','지수','자산','과세','아시아','부동산','미쓰','미쓰비시','클럽','오바마', '지분', '역대']
#tesla_keywords = ['테슬라','이차전지','트위터','엑스','자율주행','반도체','자율','주행','2차','전지']

# 관련 없는 키워드가 포함된 행 삭제 및 빈리스트에 대한 처리
def filter_rows_with_keywords(dataframe, keywords):
    pattern = '|'.join(keywords)
    mask = dataframe.str.contains(pattern, case=False)
    #mask = dataframe.apply(lambda x: bool(re.search(pattern, ', '.join(map(str, [i for i in x if i])))) if x else False)
    filtered_df = dataframe[~mask]
    return filtered_df

# 주식 관련 키워드가 포함된 행 삭제
filtered_df = filter_rows_with_keywords(words_df['pos_content'], stock_keywords)

# # 'pos_content' 열의 빈 리스트 제거
# filtered_df['pos_content'] = filtered_df['pos_content'].apply(lambda x: ', '.join(map(str, [i for i in x if i])))

# 최종 필터링된 데이터프레임 확인
print(filtered_df[:10])
print(filtered_df.shape)

# 해당하는 토픽 제외된 csv 파일 저장 : 23515
savefilepath = './Tesla_Project/data/merge/'
savefileName = 'tesla_news_topics'
csvfile.save_file(filtered_df, savefilepath, savefileName)