import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
params = {
    'page' : '1'
}
response = requests.get("https://finance.naver.com/item/sise_day.naver?code=005930", params=params, headers=headers)
bs = BeautifulSoup(response.text, 'html.parser')

# 최종 데이터 
samsung_data = []

#th값 데이터 값 들고 오기
# for th_val in bs.select("table.type2 tr > th") :
#     samsung_data.append(th_val.text.strip())

#날짜별 주가 정보 들고 
for tab_val in bs.select("table.type2 tr"):
    if tab_val is not None:
        samsung_data.append(tab_val.select("th"))
print(samsung_data)





