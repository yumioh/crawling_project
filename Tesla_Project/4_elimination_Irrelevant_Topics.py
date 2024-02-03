import re
import pandas as pd
import csvfile

newsFilePath = './Tesla_Project/data/merge/'
newsFileName = 'tesla_news_tokenization'

#테슬라 뉴스 dataFrame
words_df = csvfile.read_csv(newsFilePath, newsFileName)
words_df = pd.DataFrame(words_df)

stock_keywords = ['주식', '주가', '주가지수', '증시', '종목명', '주식시장', '현대자동차', '닛산', '네이버', '협회', '거래', '현금',
                  '제주','니콜라', '이벤트', '머니', '논란', '스톡옵션', '노조', '매출액', '공시', '세액',
                  '세금', '재산', '지수', '자산', '과세', '아시아', '미쓰', '미쓰비시', '클럽', '지분', '카다시안']
#tesla_keywords = ['테슬라','이차전지','트위터','엑스','자율주행','반도체','자율','주행','2차','전지']

# 관련 없는 키워드가 포함된 행 삭제 및 빈리스트에 대한 처리
def filter_rows_with_keywords(dataframe, keywords):
    pattern = '|'.join(keywords)
    mask = dataframe.str.contains(pattern, case=False)
    filtered_df = dataframe[~mask]
    return filtered_df

# 따옴표를 제거하는 함수 정의
def remove_quotes(value):
    return value.replace("'", "")

# 주식 관련 키워드가 포함된 행 삭제
filtered_df = filter_rows_with_keywords(words_df['pos_content'], stock_keywords)

# '날짜'와 'pos_content' 열만 선택
filtered_df_with_date = words_df[['날짜', 'pos_content']].loc[filtered_df.index]

# 최종 필터링된 데이터프레임 확인
print(filtered_df_with_date[:10])
print(filtered_df_with_date.shape)

# 'pos_content' 열에 있는 각 셀에 함수 적용
filtered_df_with_date['pos_content'] = filtered_df_with_date['pos_content'].apply(remove_quotes)
print(filtered_df_with_date[:5])

# 해당하는 토픽 제외된 csv 파일 저장 : 29278
savefilepath = './Tesla_Project/data/merge/'
savefileName = 'tesla_news_topics'
csvfile.save_file_with(filtered_df_with_date, savefilepath, savefileName)