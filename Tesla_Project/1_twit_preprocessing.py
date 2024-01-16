import pandas as pd
import csvfile, cleaningData

#csv 파일 병합
filepath = './Tesla_Project/data/'
savepath = './Tesla_Project/data/merge/'
fileName = 'merge_twit_data'
#csvfile.twit_merge_csv(filepath,savepath,fileName)

#파일 불려오기 
df = csvfile.read_csv(savepath, fileName)
#실 데이터 19906
print(f'트위터 shape : ', df.shape)

#결측치 제거
df = df.dropna(axis=0)
#print(f'결측치 제거 후 dataframe shape : ', df.shape)

print("-------------------------불필요한 정보 제거--------------------------------")

#id제거
df.drop(['id'], axis=1, inplace = True)
#print(df.head(10))

#컬럼명 변경 
df = df.rename(columns={'write_date' : '날짜', 'text' : 'content'})

#datetime으로 타입 변경
df['날짜'] = pd.to_datetime(df['날짜'])
#print(df[:10])

# NaN 값을 빈 문자열로 대체
df['content_data'] = df['content'].fillna('').astype(str)
df['content_data'] = df['content_data'].map(cleaningData.clean_tweet)

# 공백 처리
df['content_data'] = cleaningData.trim_pattern_whitespace(df['content_data'])
print(df[:40],df.shape)

#content 기사 길이가 10자 이하인 경우 제외
df = df.loc[df['content_data'].str.len() > 1]
print(f'길이가 1자 이하인 기사 제외 후 : ', df.shape)

#전처리 된 파일 저장
prepro_fileName = 'twit_Preprosessing'
savepath = './Tesla_Project/data/merge/'
csvfile.save_file(df[['날짜','content_data']], savepath, prepro_fileName)