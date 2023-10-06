import csv
import re
import requests
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

#날짜만 뽑기
def extract_date(datetime) -> str:
    x = re.findall('[0-9]{4}\.[0-9]{2}\.[0-9]{2}\.', datetime)
    if x:
        return x[0]
    return None

#이메일 처리
def email_reg(content) -> str:
    result = re.sub('[\w.+-]+@[\w-]+\.[\w.-]+', '', content)
    return result

#일반 기사 내용 전처리 
def cleanup_content(text) :
    content = ''
    if text.select_one('strong') :
       text.select_one('strong').decompose()
    if text.select_one('span.end_photo_org > em') :
        for emTag in text.select('span.end_photo_org') :
            if emTag.select_one('em') :
                emTag.select_one('em').decompose()
            else : emTag
    if len(text.getText().split('연합뉴스)')) == 2 : #연합누스) 기준으로 본문 나눔
       content = text.getText().split('연합뉴스)')[1]
    else:
        content = text.getText()
    result = re.sub(' +', ' ', content).replace('\n','').replace('\t','').strip()
    return(email_reg(result.replace('\n','').strip()))

#스포츠 기사 내용 전처리
def sports_cleanup_content(text) :
    for pTag in text.select('p') :
        pTag.decompose()
    for divTag in text.select('div'):
        divTag.decompose()
    if text.select_one('span.end_photo_org em') :
        for emTag in text.select('span.end_photo_org') :
            if emTag.select_one('em'):
                emTag.select_one('em').decompose()
            else : emTag
    if len(text.getText().split('연합뉴스)')) == 2 : #연합누스) 기준으로 본문 나눔
       content = text.getText().split('연합뉴스)')[1]
    else:
        content = text.getText()
    result = re.sub(' +', ' ', content).replace('\n','').replace('\t','').strip()
    return(email_reg(result.replace('\n','').strip()))

#연예 기사 내용 전처리
def enter_cleanup_content(text) :
    content = ''
    if text.select_one('strong') :
       text.select_one('strong').decompose()
    if text.select_one('span.end_photo_org > em') :
       for emTag in text.select('span.end_photo_org') :
            if emTag.select_one('em'):
                emTag.select_one('em').decompose()
            else : emTag
    if len(text.getText().split('연합뉴스)')) == 2 : #연합누스) 기준으로 본문 나눔
       content = text.getText().split('연합뉴스)')[1]
    else:
        content = text.getText()
    result = re.sub(' +', ' ', content).replace('\n','').replace('\t','').strip()
    return(email_reg(result.replace('\n','').strip()))

def get_news_reactions(url) :
    react_response = requests.get(url, headers=headers)
    json_data = react_response.json()
    all_count = 0
    for data in json_data['contents']:
        for reaction in data['reactions']:
            all_count += reaction['count']
    return all_count

#최종 데이터 저장
rows = []

# 8월달만 추출
for date in range(20230831,20230830,-1) :
    #8월 한달간 데이터 추출
    page = 1
    print('page : ', page)

    while True:
        prams = {
            'mode': 'LPOD',
            'mid': 'sec',
            'oid': '001',
            'date' : date,  #연합뉴스 001
            'page': 1 #str(page)
        }

        print("수집날짜: {} ".format(date))



        #연합뉴스 전체 기사리스트
        newsList_response = requests.get("https://news.naver.com/main/list.naver", headers=headers, params=prams)
        #print('리스트 url : {}'.format(newsList_response.url))
        newsList_bs = BeautifulSoup(newsList_response.text, 'html.parser')

        #현재 페이지
        now_page = int(newsList_bs.select_one('div.paging strong').text.strip())
        
        if page != now_page:
            break
        
        for elements in newsList_bs.select('div.list_body.newsflash_body > ul li'):
            url = elements.select_one('a').attrs['href']
            article_response = requests.get(url , headers=headers)
            article_bs = BeautifulSoup(article_response.text, 'html.parser')
            print(url) #수집하는 뉴스 url

            row = []
            if article_bs.select_one('h2#title_area') != None:
                print('일반기사')
                title_text = article_bs.select_one('h2#title_area').text.strip()
                title = re.sub(r'["“”‘’`]','',title_text)
                article_datetime = article_bs.select_one('span.media_end_head_info_datestamp_time._ARTICLE_MODIFY_DATE_TIME').getText().replace("\n", "")
                article_date = extract_date(article_datetime)
                #본문내용
                contents = article_bs.select_one('article#dic_area')
                #카테고리
                t_category = article_bs.select_one('em.media_end_categorize_item') 
                #수집 항목 row에 저장 (카테고리가 없는 경우 미분류로 저장)
                row.extend([article_date, title, cleanup_content(contents), t_category.getText() if t_category else '미분류'])
                #기사반응
                news_num = article_bs.select_one('div._reactionModule.u_likeit').attrs['data-cid']
                if news_num :
                    news_url =f'https://news.like.naver.com/v1/search/contents?q=NEWS%5B78526(period)%5D%7CNEWS%5B{news_num}%5D'
                    #print(news_url)
                    row.extend([get_news_reactions(news_url)])
                else :
                    row.extend([]) #반응이 없는 경우 없는경우 empty dict
            elif article_bs.select_one('div.news_headline h4.title') != None:
                print('스포츠기사')
                title_text = article_bs.select_one('div.news_headline h4.title').text.strip()
                title = re.sub(r'["“”‘’`]','',title_text)
                article_datetime = article_bs.select_one('div.news_headline div.info > span').getText().replace("\n", "")
                article_date = extract_date(article_datetime)
                #본문내용
                contents = article_bs.select_one('div#newsEndContents') 
                #스포츠인 경우 카테고리가 없음
                row.extend([article_date, title, sports_cleanup_content(contents), '스포츠']) 
                news_num = article_bs.select_one('div._reactionModule.u_likeit').attrs['data-cid']
                if news_num :
                    news_url =f'https://sports.like.naver.com/v1/search/contents?q=SPORTS%5B{news_num}%5D'
                   #print(news_url)
                    row.extend([get_news_reactions(news_url)])
                else :
                    row.extend([]) #없는경우 empty dict
            elif article_bs.select_one('h2.end_tit') != None:
                print('연예기사')
                title_text = article_bs.select_one('h2.end_tit').text.strip()
                title = re.sub(r'["“”‘’`]','',title_text)
                article_datetime = article_bs.select_one('span.author > em').getText().replace("\n", "")
                article_date = extract_date(article_datetime)
                #본문내용
                content = article_bs.select_one('#articeBody')
                row.extend([article_date, title, enter_cleanup_content(content), '연예']) 
                news_num = article_bs.select_one('div._reactionModule.u_likeit').attrs['data-cid']
                if news_num :
                    news_url = f'https://news.like.naver.com/v1/search/contents?q=ENTERTAIN%5B{news_num}%5D'
                    row.extend([get_news_reactions(news_url)])
                else :
                    row.extend([]) #없는경우 empty dict
            else: #해당하는 테그가 없을시
                print('Something is worong : {}', url)
            #최종 데이터 저장
            if len(row) > 0:
                rows.append(row)
                
        page += 1

with open("news230830.csv", mode="w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    for row in rows:
        writer.writerow(row)    

print('종료')  
