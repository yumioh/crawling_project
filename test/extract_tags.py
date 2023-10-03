import csv
import re
import requests
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

url = 'https://n.news.naver.com/mnews/article/001/0014162532'
sport_url = 'https://sports.naver.com/news?oid=001&aid=0014164596'
enter_url = 'https://entertain.naver.com/read?oid=001&aid=0014164167'

newsList_response = requests.get(url, headers=headers)
newsList_bs = BeautifulSoup(newsList_response.text, 'html.parser')

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

def email_reg(content) -> str:
    result = re.sub('[\w.+-]+@[\w-]+\.[\w.-]+', '', content)
    return result

#일반 신문 태그 제거 
def cleanup_content(text) :
    content = ''
    if text.select_one('strong') :
       text.select_one('strong').decompose()
    if text.select_one('span.end_photo_org > em') :
       for value in text.select('span.end_photo_org') :
           value.select_one('em').decompose()
    #print(text.getText().split('연합뉴스)'))
    if len(text.getText().split('연합뉴스)')) == 2 : 
       content = text.getText().split('연합뉴스)')[1]
    else:
        content = text.getText()
    result = re.sub(' +', ' ', content).replace('\n','').replace('\t','').strip()
    return(email_reg(result))

def sports_cleanup_content(text) :
    for pTag in text.select('p') :
        pTag.decompose()
    for divTag in text.select('div'):
        divTag.decompose()
    if text.select_one('span.end_photo_org em') :
        for emTag in text.select('span.end_photo_org') :
            emTag.select_one('em').decompose()
    if len(text.getText().split('연합뉴스)')) == 2 : 
       content = text.getText().split('연합뉴스)')[1]
    else:
        content = text.getText()
    result = re.sub(' +', ' ', content).replace('\n','').replace('\t','').strip()
    return(result)

def enter_cleanup_content(text) :
    content = ''
    if text.select_one('strong') :
       text.select_one('strong').decompose()
    if text.select_one('span.end_photo_org > em') :
       for value in text.select('span.end_photo_org') :
           value.select_one('em').decompose()
    if len(text.getText().split('연합뉴스)')) == 2 : 
       content = text.getText().split('연합뉴스)')[1]
    else:
        content = text.getText()
    result = re.sub(' +', ' ', content).replace('\n','').replace('\t','').strip()
    return(email_reg(result.replace('\n','').strip()))

#extractTag(newsList_bs)
text = newsList_bs.select_one('article#dic_area')
#newsList_bs.p.decompose()
sports_text = newsList_bs.select_one('div#newsEndContents')
enter_text = newsList_bs.select_one('#articeBody')
print(cleanup_content(text))
#print(contents.select_one('strong').decompose())
#print(contents)
#extractTags(contents)
#contents.select_one('strong').decompose()

#con = contents.getText()#연합뉴스 제거
#start = con.split('=')[2]
#print(re.sub(' +', ' ', con)) #공백 제거



