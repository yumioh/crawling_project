import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

#이메일 처리
def email_reg(content) -> str:
    result = re.sub('[\w.+-]+@[\w-]+\.[\w.-]+', '', content)
    return result

#날짜형식 변경
def remove_time_prefix(input_str) :
  if any([x in input_str for x in ["오전", "오후"]]):
    #기사입력, 오후, 오전 반환
    date_time_str = re.sub(r'기사입력|오후 |오전 ', '', input_str).strip()
    #print(date_time_str)
    #기사입력 2023.10.07. 오후 05:21
    try :
        # 날짜 및 시간 형식의 문자열을 날짜 객체로 파싱
        date_time = datetime.strptime(date_time_str, "%Y.%m.%d. %H:%M")
        # 날짜 부분만 추출
        date = date_time.strftime("%Y.%m.%d")
    except ValueError: #올바른 형식으로 파싱 할수 없는 경우 None 반환
      return None
  else :
      date_time = datetime.strptime(input_str, "%Y-%m-%d %H:%M:%S")
      date = date_time.strftime("%Y.%m.%d")
  return date

#네이버 뉴스기사 정보 가져오기 
def get_news(URL) :
  res = requests.get(URL, headers=headers)
  soup = BeautifulSoup(res.text, "html.parser")

  title_element = ""
  date_element = ""
  media_element = ""
  content_element = ""

  if soup.select_one("h2#title_area span") != None: #일반 기사
    title_element = soup.select_one("h2#title_area span") #제목
    date_element = soup.select_one("span.media_end_head_info_datestamp_time") #기사작성일시
    media_element = soup.select_one("a.media_end_head_top_logo img") #뉴스매체명
    content_element = soup.select_one("div#newsct_article") #기사원문
  elif soup.select_one('h2.end_tit') != None : #연예기사
    title_element = soup.select_one('h2.end_tit') 
    date_element = soup.select_one("span.author > em")
    media_element = soup.select_one("a.press_logo img") 
    content_element = soup.select_one("div#articeBody") 
  elif soup.select_one('div.news_headline h4.title') != None: #스포츠기사
    title_element = soup.select_one("div.news_headline h4.title")
    date_element = soup.select_one("div.info span") 
    media_element = soup.select_one("span.logo img") 
    content_element = soup.select_one("div#newsEndContents") 
  else :
    return None
  
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
    
  print(title, URL)
  return (title, remove_time_prefix(date), media, email_reg(content))

#뉴스 리스트 들고 오기
def get_news_list(keyword, toDate, fromDate) :
    news = []
    #뉴스 리스트 페이지
    for date in pd.date_range(toDate, fromDate) :
      str_d = date.strftime("%Y.%m.%d")
      page = 1
      while True:
        start = (page-1) * 10 + 1
        print(page)
        URL = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+ keyword +'&sort=1&photo=0&field=0&pd=3&ds='+str_d+'&de='+str_d+'&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from'+str_d.replace(".","")+'to'+str_d.replace(".","")+',a:all&start='+str(start)
        print(URL)
        res = requests.get(URL,headers = headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        #print(soup.select_one(".api_noresult_wrap"))

        #해당하는 페이지에 검색할 페이지가 없는 경우
        if soup.select_one("div.not_found02"):
          print("크롤링 끝")
          break

        news_list = soup.select("ul.list_news li")
        
        for item in news_list :
          if len(item.select("div.info_group a")) == 2 :
            news.append(get_news(item.select("div.info_group a")[1]['href']))
        page += 1
        
    return pd.DataFrame(news, columns=['title','date','media','content'])
    #return news

keyword = "테슬라"
toDate = "2023.04.01"
fromDate = "2023.04.15"

rows = get_news_list(keyword, toDate, fromDate)

#csv로 파일 저장
rows.to_csv('D:/data_analysis/data/tesla0415.csv', encoding='utf-8-sig')

