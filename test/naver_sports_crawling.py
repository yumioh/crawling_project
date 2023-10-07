import requests
from bs4 import BeautifulSoup as bs
import re

article_url = 'https://sports.news.naver.com/news?oid=445&aid=0000143530'
headers = {'User-Agent':'Mozila/5.0'}
response = requests.get(article_url, headers=headers)
html = response.text
soup = bs(html, 'html.parser')

title = soup.select_one('h4.title')
content = soup.select_one('#newsEndContents')
# delete 'div', 'p' tags in the content
divs = content.select('div')
for div in divs:
    div.decompose()
ps = content.select('p')
for p in ps:
    p.decompose()
    
print(title.text)
print(content.text)








