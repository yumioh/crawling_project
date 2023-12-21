import csv
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

#삼성전자 주가 메인
main_response = requests.get("https://finance.naver.com/item/sise.nhn?code=005930", headers=headers)
main_bs = BeautifulSoup(main_response.text, 'html.parser')

#삼성정자 데이터 
samsung_data = []

title = [] #타이틀
rows = []  #날짜, 종가, 상승/하락 여부, 전일비, 시가, 고가, 저가, 거래량

page = 2
last_page = 5
is_title_populated = False #타이틀 추출 여부
expected_year_month = '2023.08' #8월꺼만 추출

while True :
    
    print('page : ', page)

    params = {
    'page' : str(page)
    }

    #삼성전자 일별 주가
    daily_url = main_bs.select_one("iframe[title='일별 시세']").get('src')
    daily_response = requests.get('https://finance.naver.com' + daily_url, params=params, headers=headers)
    daily_bs = BeautifulSoup(daily_response.text, 'html.parser')

    #page2 ~ page4까지 8월 주가 데이터
    if page == last_page:
        break

    for item_val in daily_bs.select('table.type2'):

        #타이틀
        if not is_title_populated:
            is_title_populated = True
            for title_val in item_val.select('table.type2 tr > th'):
                title.append(title_val.getText())

        for row_element in item_val.select("tr[onmouseout='mouseOut(this)']"):
            is_expected_date = False #해당 일자값 추출을 위한 default값
            row = []
            for idx, data_element in enumerate(row_element.select('td')):
                data = data_element.find('span').getText().strip()
                #print(f'{idx} {data}')
                if idx == 0: #날짜
                    is_expected_date = True if data.startswith(expected_year_month) else False
                    if is_expected_date:
                        row.append(data.replace('.','-'))
                if is_expected_date and idx == 1: #종가
                    row.append(data.replace(',',''))
                if is_expected_date and idx == 2: #전일비
                    img = data_element.find('img')
                    if img:
                        data = ('-' if img.attrs['alt'] == '하락' else '+') + data
                    row.append(data.replace(',',''))
                if is_expected_date and idx == 3: #시가
                    row.append(data.replace(',',''))
                if is_expected_date and idx == 4: #고가
                    row.append(data.replace(',',''))
                if is_expected_date and idx == 5: #저가
                    row.append(data.replace(',',''))
                if is_expected_date and idx == 6: #거래량
                    row.append(data.replace(',',''))
            if is_expected_date:
                rows.append(row)
    page += 1

# print(rows)
with open("stocks.csv", mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(title)
    for row in rows:
        writer.writerow(row)

print("종료")
