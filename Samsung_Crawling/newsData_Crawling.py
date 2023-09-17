import csv
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

# 8월달만 추출
prams = {
    'mode':'LPOD',
    'mid':'sec',
    'oid':'001', #연합뉴스 001
    'date' : '20230801',
    'page': 3
}

#연합뉴스 기사리스트
newsList_response = requests.get("https://news.naver.com/main/list.naver", headers=headers, params=prams)
newsList_bs = BeautifulSoup(newsList_response.text, 'html.parser')


for elements in newsList_bs.select('div.list_body.newsflash_body > ul li'):
    #print(elements)
    url = elements.select_one('a').attrs['href']
    article_response = requests.get(url , headers=headers)
    article_bs = BeautifulSoup(article_response.text, 'html.parser')
    
    title = ''
    content = ''
    #날짜, 제목, 본문내용, 카테고리, 반응

    if article_bs.select_one('h2#title_area') != None:
        print('일반기사')
        title = article_bs.select_one('h2#title_area').getText()
        article_datetime = article_bs.select_one('span.media_end_head_info_datestamp_time._ARTICLE_MODIFY_DATE_TIME').getText()
        article_date = article_datetime.split()[0] #날짜
        contents = article_bs.select_one('article#dic_area')
        print(contents)
        print(title)
    elif article_bs.select_one('div.news_headline h4.title') != None:
        print('스포츠기사')
        title = article_bs.select_one('div.news_headline h4.title').getText()
        #print(title)
    elif article_bs.select_one('h2.end_tit') != None:
        print('연예기사')
        title = article_bs.select_one('h2.end_tit').getText()
        #print(title)
    else:
        print('Something is worong : {}', url)

          
