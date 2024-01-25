import pandas as pd
import re
import csvfile


# 예시 데이터프레임 생성
data = {'날짜': ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04'],
        'pos_content': [['대통령','대통령1','대통령2', []], ['년','년3','년4'], ['미국인', [],'미국인3','미국인'], ['오바마', '오바마',[]]]}
filtered_df = pd.DataFrame(data)
#print('삭제 전:', filtered_df)

# # 리스트의 각 요소를 문자열로 결합하는 함수 정의
# def join_list_to_string(lst):
#     return ', '.join(map(str, lst))

# # '날짜' 열을 문자열로 변환
# df['날짜'] = df['날짜'].apply(join_list_to_string)

# 'pos_content' 열의 빈 리스트 제거
filtered_df['pos_content'] = filtered_df['pos_content'].apply(lambda x: ', '.join(map(str, [i for i in x if i])))

print('---------------------------------------------------')

newsFilePath = './Tesla_Project/data/merge/'
newsFileName = 'tesla_news_tokenization'

# 테슬라 뉴스 DataFrame
words_df = csvfile.read_csv(newsFilePath, newsFileName)
words_df = pd.DataFrame(words_df)

#문자열로 저장된 데이터를 리스트로 변환
words_df['pos_content'] = words_df['pos_content'].apply(eval)

stock_keywords = ['주식', '주가', '주가지수', '증시', '종목명', '주식시장', '현대자동차', '닛산', '네이버', '카다시안', '협회', '거래', '현금', '테슬라',
                  '현대차', '기아', '도요타', '제주', '니콜라', '이벤트', '머니', '논란', '스톡옵션', '항목', '노조', '매출액', '공시', '세액',
                  '세금', '재산', '대통령실', '지수', '자산', '과세', '아시아', '부동산', '미쓰', '미쓰비시', '클럽', '오바마', '지분', '역대']

# 'pos_content' 열의 빈 리스트 제거
def filter_rows_with_keywords(dataframe, keywords):
    pattern = '|'.join(keywords)
    mask = dataframe.str.contains(pattern, case=False)
    #mask = dataframe.apply(lambda x: bool(re.search(pattern, ', '.join(map(str, [i for i in x if i])))) if x else False)
    filtered_df = dataframe[~mask]
    return filtered_df

# 주식 관련 키워드가 포함된 행 삭제
filtered_df = filter_rows_with_keywords(words_df['pos_content'], stock_keywords)

# 최종 필터링된 데이터프레임 확인
print(words_df[:10])
print(words_df.shape)

