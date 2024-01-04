# 크롤링, 시각화 미니 프로젝트

#### 사용언어 : python
#### 사용 Tools : VScode, google colaboratory

# 크롤링

## 1. 삼성 주가 (newsData_Crawling.py)
    - 기간 : 2023.08.01 ~ 2023.08.31 (한달)
    - 수집 대상 : 삼성주가
    - 수집 항목 : 일자, 종가, 전일비, 시가, 고가, 저가, 거래량
    - stocks.csv 파일로 저장

## 2. 네이버 뉴스 (stockData_Crawling.py)
    - 기간 : 2023.08.01 ~ 2023.08.31(한달)
    - 수집 대상 : 연합뉴스
    - 수집 항목 : 날짜, 타이틀, 기사본문, 기사반응*, 카테고리 (카테고리가 여러개로 분류 될 경우 가장 앞에 있는 카테고리로 추출)
    - 기사내용 전처리
    - news.csv파일로 저장
    * 기사반응은 비동기 방식으로 추출
<br/>

<img src="https://github.com/yumioh/data_analysis/assets/38059057/8547f4ff-fd7f-478c-8ad4-dc66fc0c8475" width="50%" height="20%" />

# 통계 및 시각화

## 1. 기사 데이터 정리 및 통계
    - 전체기사 일자별 카운트
    - 본문이 비어있는 기사를 제외하고 삼성글자가 들어간 뉴스들만 분류
    - 일자별로 분류한 카운트와 삼성 주가 데이터 합치기 (주가가 없는 날짜 제외)
    - 데이터 수치를 백분위로 변경 (날짜별합/전체합 * 100)
    
   
## 2. 관심도, 카테고리 데이터 통계
    - 삼성 날짜별 관심도 정리
    - 삼성 기사 카테고리별 합계


## 3. 정리한 데이터를 기반으로 그래프 작성(시각화)
    - 기사버즈량 및 주가 비교

<img src="https://github.com/yumioh/data_analysis/assets/38059057/16b4b68f-d653-4347-a362-f5627e8b049b" width="70%" height="30%"/>

    - 일자별 기사 관심도 
<img src="https://github.com/yumioh/data_analysis/assets/38059057/d80a6ea9-edc9-4f35-bea4-e5166a49f855" width="70%" height="30%"/>

    - 카테고리별 기사량
<img src="https://github.com/yumioh/data_analysis/assets/38059057/f12404b6-0e86-4a65-8dd8-381d15784676" width="70%" height="30%"/>

## 4. 워드 클라우드 만들기



