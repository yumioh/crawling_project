import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from wordcloud import WordCloud, STOPWORDS

#파일 불려오기
saveMerge = './data/samsung_merge.csv'
saveReactivity = './data/reactivity.csv'
saveCategory = './data/category.csv'

mergeData = pd.read_csv(saveMerge)
reactivity = pd.read_csv(saveReactivity)
category = pd.read_csv(saveCategory)

print(mpl.matplotlib_fname())

# 기사 버즈량 및 주가 비교 시각화
plt.rcParams['font.family'] = 'NanumGothicCoding'
plt.rcParams.update({'font.size': 10, 'font.family': 'NanumGothicBold'})
plt.figure(figsize=(8, 8))
plt.title("기사 버즈량 및 주가 비교", fontsize=20)
plt.xticks(rotation=75)

dates = list(map(lambda n: pd.to_datetime(n).strftime('%Y-%m-%d'), mergeData['날짜']))

#날짜
plt.plot(dates, mergeData['본문백분위'].values, label='버즈량', color ='dodgerblue')
plt.plot(dates, mergeData['삼성전자 주가백분위'].values, label='주가',color='darkorange')

#범례를 그래프의 오른쪽 상단
plt.legend(loc=1)
plt.show()

#일자별 기사 관심도
plt.rcParams.update({'font.size': 10, 'font.family': 'NanumGothicBold'})
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.xticks(rotation=75)
#날짜
dates = list(map(lambda n: pd.to_datetime(n).strftime('%Y-%m-%d'), reactivity.index))

plt.plot(dates, reactivity['반응갯수'].values, label='반응수', marker = 'o', linestyle = 'solid', color='limegreen')
plt.legend(loc=0)
plt.tight_layout() 
plt.show()

#카테고리별 기사량
plt.figure(figsize=(10, 10))
plt.title("일자별 기사 관심도", fontsize=20)
plt.bar(category.index, category['분야'], color='lightskyblue')
plt.tight_layout() 
plt.show()


# wordcloud = WordCloud(max_font_size=200,
#                       font_path='/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
#                       stopwords=STOPWORDS,
#                       background_color='#FFFFFF',
#                       width=1200,
#                       height=800).generate(''.join(samsungNews[samsungNews['날짜']=='2023-08-03']['내용'].values))

# plt.figure(figsize=(20,20))
# plt.imshow(wordcloud)
# plt.tight_layout(pad=0)
# plt.axis('off')
# plt.show()

  