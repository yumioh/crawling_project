import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

article_url = 'https://sports.news.naver.com/news?oid=445&aid=0000143530'
headers = {'User-Agent':'Mozila/5.0'}
response = requests.get(article_url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

title = soup.select_one('h4.title')
content = soup.select_one('#newsEndContents')
# delete 'div', 'p' tags in the content
divs = content.select('div')
for div in divs:
    div.decompose()
ps = content.select('p')
for p in ps:
    p.decompose()
    
#print(title.text)
#print(content.text)

news = []

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
  # elif soup.select_one('h2.end_tit') != None : #연예기사
  #   title_element = soup.select_one('h2.end_tit') 
  #   date_element = soup.select_one("span.author > em")
  #   media_element = soup.select_one("a.press_logo img") 
  #   content_element = soup.select_one("div#articeBody") 
  # elif soup.select_one('div.news_headline h4.title') != None: #스포츠기사
  #   title_element = soup.select_one("div.news_headline h4.title")
  #   date_element = soup.select_one("div.info span") 
  #   media_element = soup.select_one("span.logo img") 
  #   content_element = soup.select_one("div#newsEndContents") 
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
    
  #print(title, URL)
  return (title, date, media,content)


print(get_news('https://search.naver.com/search.naver?where=news&sm=tab_pge&query=테슬라&sort=1&photo=0&field=0&pd=3&ds=2023.01.16&de=2023.01.16&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from20230116to20230116,a:all&start=31'))








