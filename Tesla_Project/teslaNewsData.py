import csv
import re
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

#이메일 처리
def email_reg(content) -> str:
    result = re.sub('[\w.+-]+@[\w-]+\.[\w.-]+', '', content)
    return result


def clenaup_content(text) :
  return 0

#날짜형식 변경
def remove_time_prefix(input_str) :
  if any([x in input_str for x in ["오전", "오후"]]):
    #기사입력, 오후, 오전 반환
    date_time_str = re.sub(r'기사입력|오후 |오전 ', '', input_str).strip()
    #2023.10.07. 05:21
    try :
        date_time = datetime.strptime(date_time_str,"%Y.%m.%d. %H:%M")
    except ValueError: #올바른 형식으로 파싱 할수 없는 경우 None 반환
      return None
    
    #시간을 24시간 형식으로 변경 
    if "오후" in input_str:
      date_time = date_time.replace(hour = date_time.hour + 12)
    #datetime을 문자열로 변경
    formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
  else :
      formatted_date_time = input_str
  print(formatted_date_time)
  return formatted_date_time

#네이버 뉴스기사 정보 가져오기 
def get_news(URL) :
  res = requests.get(URL, headers=headers)
  soup = BeautifulSoup(res.text, "html.parser")

  title_element = ""
  date_element = ""
  media_element = ""
  content_element = ""

  if soup.select_one("h2#title_area span") != None:#일반 기사
    title_element = soup.select_one("h2#title_area span") 
    date_element = soup.select_one("span.media_end_head_info_datestamp_time") #기사작성일시
    media_element = soup.select_one("a.media_end_head_top_logo img") #뉴스매체명
    content_element = soup.select_one("div#newsct_article") #기사원문
  elif soup.select_one('h2.end_tit') != None : #연예기사
    title_element = soup.select_one('h2.end_tit') #제목
    date_element = soup.select_one("span.author > em") #기사작성일시
    media_element = soup.select_one("a.press_logo img") #뉴스매체명
    content_element = soup.select_one("div#articeBody") #기사원문
  elif soup.select_one('div.news_headline h4.title') != None : #스포츠기사
    title_element = soup.select_one("div.news_headline h4.title") #제목
    date_element = soup.select_one("div.info span") #기사작성일시
    media_element = soup.select_one("span.logo img") #뉴스매체명
    content_element = soup.select_one("div#newsEndContents") #기사원문

  if title_element:
    title = title_element.text.strip()
  else:
    title = "No Title Found"

  if date_element and 'data-date-time' in date_element.attrs:
    date = date_element['data-date-time'].strip()
  elif date_element :
    date = date_element.text.strip()
  else:
    date = "No Date Found"

  if media_element and 'title' in media_element.attrs:
    media = media_element['title'].strip()
  elif media_element and 'alt' in media_element.attrs :
    media = media_element['alt'].strip()
  else:
    media = "No Media Found"
  
  if content_element:
    content = content_element.text.strip()
    content = re.sub(r'[\r\n\t\"\'\,]', '', content)
  else:
    content = "No Content Found"
  return (title, remove_time_prefix(date), media, email_reg(content), URL)

#뉴스 리스트 들고 오기
def get_news_list(keyword, toDate, fromDate) :
    news = []
    page = "1" #뉴스 리스트 페이지

    #TODO : 페이징 처리

    URL = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+ keyword +'&sort=1&photo=0&field=0&pd=3&ds='+toDate+'&de='+fromDate+'&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from'+fromDate.replace(".","")+'to'+toDate.replace(".","")+',a:all&start='+page
    print(URL)
    res = requests.get(URL,headers = headers)
    soup = BeautifulSoup(res.text, "html.parser")

    #print(now_page = int(soup.select_one('div.paging strong').text.strip()))

    news_list = soup.select("ul.list_news li")
    for item in news_list :
      if len(item.select("div.info_group a")) == 2 :
        news.append(get_news(item.select("div.info_group a")[1]['href']))
    return pd.DataFrame(news, columns=['title','date','media','content','url'])
    #return news




keyword = "테슬라"
toDate = "2023.10.07"
fromDate = "2023.09.07"

rows = get_news_list(keyword, toDate, fromDate)

print(rows)

#with open("teslaNews.csv", mode="w", encoding="utf-8-sig", newline="") as file:
#    writer = csv.writer(file)
#    for row in rows:
#        writer.writerow(row)