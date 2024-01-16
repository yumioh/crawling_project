import pandas as pd
import csvfile, cleaningData

#csv 파일 병합
stockfilepath = './Tesla_Project/data/merge/'
stockfileName = 'merge_news_data'
#csvfile.merge_csv(stockfilepath,stockfileName)

#파일 불려오기
df = csvfile.read_csv(stockfilepath, stockfileName)
print(f'원본 뉴스 dataframe shape : ', df.shape)

#결측치 제거
df = df.dropna(axis=0)
print(f'결측치 제거 후 dataframe shape : ', df.shape)

print("-------------------------불필요한 정보 제거--------------------------------")

#media(신문매체이름), Unnamed 열 제거
#df.drop(['media','Unnamed: 0'], axis=1, inplace = True)
#print(df.head(10))

#컬럼명 변경 (주식데이터와 merge 하기 위해)
#df = df.rename(columns={'date' : '날짜'})

#datetime으로 타입 변경
df['날짜'] = pd.to_datetime(df['날짜'])
#print(df[:10])

# NaN 값을 빈 문자열로 대체
df['content_data'] = df['content'].fillna('').astype(str)

# 공백 처리
df['content_data'] = cleaningData.trim_pattern_whitespace(df['content_data'])
#print(df[:10])

#불용어 처리
df['content_data'] = df['content_data'].map(cleaningData.clean_byline)
#print(df[:10])

#content 기사 길이가 140자 이하인 경우 제외
df = df.loc[df['content_data'].str.len() > 140]
print(f'길이가 140자 이하인 기사 제외 후 : ', df.shape)

#전처리 된 파일 저장
stockSavefilepath = './Tesla_Project/data/merge/'
stockSavefileName = 'telsa_preprosessing'
csvfile.save_file(df[['날짜','content_data']], stockSavefilepath, stockSavefileName)


