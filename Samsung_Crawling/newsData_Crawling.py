import csv
import re
import requests
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
# #전처리를 위한 정규식
# def content_reg(content):
        
#     email_reg = '[\w.+-]+@[\w-]+\.[\w.-]+' #이메일주소
#     em_reg = '<em*(.*?)<(\/?)em>' #em태그
#     br_reg = '(<([^>]+)>)' # 모든태그 없애기
#     button_reg = '<button*(.*?)<(\/?)button>' #버튼태그
#     dt_reg = '<dt*(.*?)<(\/?)dt>' #dt태그
#     ap_tag= '<[a|p](.*)<(\/?)[a|p]>'#a/p 태그

#     content= content.replace('\n', '')
#     result = re.sub(email_reg,'',content)
#     result = re.sub(ap_tag,'',result)
#     result = re.sub(em_reg,'',result)
#     result = re.sub(button_reg,'',result)
#     result = re.sub(dt_reg,'',result)
#     result = re.sub(br_reg,'',result)
#     return result

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

#기사 내용 전처리 
def cleanup_content(text) :
    content = ''
    if (text.select_one('strong')) :
       text.select_one('strong').decompose()
    for value in text.select('span.end_photo_org') :
        value.select_one('em').decompose()
    if len(text.getText().split('=')) != 1 : # 영문신문인 경우 =이 없음
       content = text.getText().split('=')[2]
    else : 
        content = text.getText()
    result = re.sub(' +', ' ', content)
    return(email_reg(result.strip()))

def get_news_reactions(url) -> dict:
    react_response = requests.get(url, headers=headers)
    react_json = re.findall('(?<=jQuery.{34}\()(.*)(?=\);)', react_response.text)[0]
    json_data = json.loads(react_json)

    _reactions = {}
    for data in json_data['contents']:
        if data['serviceId'] == 'NEWS':
            for reaction in data['reactions']:
                key = reaction['reactionType']
                val = reaction['count']
                _reactions[key] = val
    return _reactions

# 8월달만 추출
mode = 'LPOD'
mid = 'sec'
oid = '001' #연합뉴스 001
page = 1

for date in range(20230831,20230830,-1) :
    #8월 한달간 데이터 추출
    while True:
        print('page : ',page)
        prams = {
            'mode':mode,
            'mid': mid,
            'oid': oid,
            'date' : date,
            'page': 1 #str(page)
        }
        print(date)

        #연합뉴스 기사리스트
        newsList_response = requests.get("https://news.naver.com/main/list.naver", headers=headers, params=prams)
        print(newsList_response.url)
        newsList_bs = BeautifulSoup(newsList_response.text, 'html.parser')

        #page 처리
        now_page = int(newsList_bs.select_one('div.paging strong').text.strip())
        
        if page != now_page:
            break

        #최종 데이터 저장
        rows = []

        for elements in newsList_bs.select('div.list_body.newsflash_body > ul li'):
            url = elements.select_one('a').attrs['href']
            article_response = requests.get(url , headers=headers)
            print(url)
            article_bs = BeautifulSoup(article_response.text, 'html.parser')
            
            row = []
            if article_bs.select_one('h2#title_area') != None:
                print('일반기사')
                title = article_bs.select_one('h2#title_area').getText()
                article_datetime = article_bs.select_one('span.media_end_head_info_datestamp_time._ARTICLE_MODIFY_DATE_TIME').getText().replace("\n", "")
                article_date = extract_date(article_datetime)
                contents = article_bs.select_one('article#dic_area') #본문내용
                #print(contents)
                t_category = article_bs.select_one('em.media_end_categorize_item') #카테고리
                print(cleanup_content(contents))
                row.extend([article_date, title, "", t_category.getText() if t_category else '미분류'])
                news_num = article_bs.select_one('div._reactionModule.u_likeit').attrs['data-cid']
                if news_num :
                    news_url ='https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery33108070717792052775_1695046642179&q=JOURNALIST%5B27406(period)%5D%7CNEWS%5B'+ news_num +'%5D&isDuplication=false&cssIds=MULTI_MOBILE%2CNEWS_MOBILE&_=1695046642180'
                    row.append(get_news_reactions(news_url))
                else :
                    row.append({}) #없는경우 empty dict
            elif article_bs.select_one('div.news_headline h4.title') != None:
                print('스포츠기사')
                title = article_bs.select_one('div.news_headline h4.title').getText().strip()
                article_datetime = article_bs.select_one('div.news_headline div.info > span').getText().replace("\n", "")
                article_date = extract_date(article_datetime) #날짜
                contents = article_bs.select_one('div#newsEndContents').text.replace('\n','').strip() #본문내용
                #row.append([article_date, title, cleanup_content(contents), '스포츠']) #카테고리
                news_num = article_bs.select_one('div._reactionModule.u_likeit').attrs['data-cid']
                # if news_num :
                #     news_url ='https://sports.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery111306507478702215144_1695048035128&q=SPORTS%5Bne_001_0014105967%5D%7CJOURNALIST%5B27942(period)%5D%7CSPORTS_MAIN%5Bne_001_0014105967%5D&isDuplication=false&cssIds=MULTI_PC%2CSPORTS_PC&_=1695048035129'
                #     row.append(get_news_reactions(news_url))
                # else :
                row.append({}) #없는경우 empty dict
            elif article_bs.select_one('h2.end_tit') != None:
                print('연예기사')
                title = article_bs.select_one('h2.end_tit').getText()
                article_datetime = article_bs.select_one('span.author > em').getText().replace("\n", "")#본문내용
                article_date = extract_date(article_datetime) #날짜
                content = article_bs.select_one('#articeBody').text.replace('\n','').strip() #본문내용
                #print(article_bs.select_one('em.guide_categorization_item')) #카테고리
                #row.append([article_date, title, cleanup_content(contents), '연예']) #카테고리
                news_num = article_bs.select_one('div._reactionModule.u_likeit').attrs['data-cid']
                row.append({})#반응
            else:
                print('Something is worong : {}', url)

        page += 1

    #최종 데이터 저장
        if len(row) > 0:
            rows.append(row)
        print(rows)
print('크롤링종료')  
