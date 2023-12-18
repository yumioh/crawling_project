import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from wordcloud import WordCloud, STOPWORDS
import os
from dotenv import load_dotenv

load_dotenv()
font_path = os.environ.get('FONT_PATH')

#파일 불려오기
saveMerge = './data/samsung_merge.csv'
saveReactivity = './data/reactivity.csv'
saveCategory = './data/category.csv'

mergeData = pd.read_csv(saveMerge)
reactivity = pd.read_csv(saveReactivity)
category = pd.read_csv(saveCategory)


#폰트 설정
font_path = font_path
font = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font)
plt.rcParams['font.size'] = 10

# 기사 버즈량 및 주가 비교 시각화
plt.figure(figsize=(8, 8))
plt.title("기사 버즈량 및 주가 비교", fontsize=20)
plt.xticks(rotation=75)

dates = list(map(lambda n: pd.to_datetime(n).strftime('%Y-%m-%d'), mergeData['날짜']))

#날짜
plt.plot(dates, mergeData['본문백분위'].values, label='버즈량', color ='dodgerblue')
plt.plot(dates, mergeData['삼성전자 주가백분위'].values, label='주가',color='darkorange')

#범례를 그래프의 오른쪽 상단
plt.legend(loc=1)
#plt.show()

#일자별 기사 관심도
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.xticks(rotation=75)

plt.plot(reactivity['날짜'], reactivity['반응갯수'].values, label='반응수', marker = 'o', linestyle = 'solid', color='limegreen')
plt.legend(loc=0)
plt.tight_layout() 

#카테고리별 기사량
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.bar(category['분야'], category['count'], color='lightskyblue')
plt.tight_layout() 

#결과 출력
plt.show()

wordcloud = WordCloud(max_font_size=200,
                      font_path=font_path,
                      #stopwords=STOPWORDS,
                      background_color='#FFFFFF',
                      width=1200,
                      height=800).generate_from_file('./data/result.txt')

plt.figure(figsize=(20,20))
plt.imshow(wordcloud)
plt.tight_layout(pad=0)
plt.axis('off')
plt.show()

  