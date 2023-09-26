import requests,re
import json

news_num = '0014200324'

headers  = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

enter_url='https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery111103661092026199333_1695051320003&q=ENTERTAIN%5Bne_001_0014105953%5D%7CJOURNALIST%5B76915(period)%5D%7CENTERTAIN_MAIN%5Bne_001_0014105953%5D&isDuplication=false&cssIds=MULTI_PC%2CENTERTAIN_PC&_=1695051320004' 
sports_url ='https://sports.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery111308237307660858897_1695089718681&q=SPORTS%5Bne_001_0014105967%5D%7CJOURNALIST%5B27942(period)%5D%7CSPORTS_MAIN%5Bne_001_0014105967%5D&isDuplication=false&cssIds=MULTI_PC%2CSPORTS_PC&_=1695089718682'
news_url = 'https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery3310999753245169029_1695089763056&q=NEWS%5Bne_001_0014105964%5D&isDuplication=false&cssIds=MULTI_MOBILE%2CNEWS_MOBILE&_=1695089763057'

#url = enter_url
#url = sports_url
url = news_url
react_response = requests.get(url,headers=headers)
callback = re.findall('(?<=callback\=)(.+?)(?=&)', url)[0]
contents_id = re.findall('(?<=%5B)(.+?)(?=%5D)', url)[0]
react_json = re.findall(f'(?<={callback}\()(.+)(?=\);)', react_response.text)[0]
#len(react_json)
#print(react_json)
json_data = json.loads(react_json)
#print(json_data)

_reactions = {}
for data in json_data['contents']:
    if data['contentsId'] == contents_id: # 연예 ENTERTAIN_MAIN 스포츠 SPORTS_MAIN 일반
        for reaction in data['reactions']:
            key = reaction['reactionType']
            val = reaction['count']
            _reactions[key] = val
print(_reactions)