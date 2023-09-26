import csv
import re
import requests
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

newsList_response = requests.get("https://n.news.naver.com/mnews/article/001/0014164627", headers=headers)
newsList_bs = BeautifulSoup(newsList_response.text, 'html.parser')

#일반 신문 태그 제거 
def extractTag(text) :
    text.select_one('strong').decompose()
    for value in text.select('span.end_photo_org') :
        value.select_one('em').decompose()
    content = text.getText().split('=')[2]
    result = re.sub(' +', ' ', content)
    return(result)

#extractTag(newsList_bs)
text = newsList_bs.select_one('article#dic_area')
print(extractTag(text))
#print(contents.select_one('strong').decompose())
#print(contents)
#extractTags(contents)
#contents.select_one('strong').decompose()

#con = contents.getText()#연합뉴스 제거
#start = con.split('=')[2]
#print(re.sub(' +', ' ', con)) #공백 제거



