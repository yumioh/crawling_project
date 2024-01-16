# 웹 크롤링을 통한 LDA 모델링 및 Twiiter의 Elon Musk의 발언 영향 주가 스윙 분석 

#### 사용언어 : python
#### 사용 Tools : VScode

# 크롤링

## 1. 테슬라 주가 (인베스팅 사이트 통한 주가 파일 다운로드)
    - 기간 : 2020.01.01 ~ 2023.09.30 (3년 9개월)
    - 수집 대상 : 테슬라 주가
    - 수집 항목 : 날짜, 종가, 시가, 고가, 저가, 거래량, 변동
    - stocks.csv 파일로 저장

## 2. 테슬라 뉴스 (news_collecting.py)
    - 기간 : 2020.01.01 ~ 2023.09.30 (3년 9개월)
    - 수집 대상 : 네이버 뉴스로 통해 수집 (이데일리, 한국경제, 전자신문 등)
    - 수집 항목 : 날짜, 타이틀, 기사본문, 카테고리 (카테고리가 여러개로 분류 될 경우 가장 앞에 있는 카테고리로 추출)
    - 뉴스 전처리
    - teslaNews_YYMM.csv파일로 저장

## 3. 테슬라 트위터
    - 기간 : 2020.01.01 ~ 2023.09.30 (3년 9개월)
    - 수집 대상 : selenium을 통해 수집
    - 수집 항목 : 아이디, 유저이름, 내용, 날짜 
    - 트위터 전처리
    - YYYY_twit_data.csv파일로 저장
<br/>

# 데이터 분석

## 1. 기사 데이터 전처리 
    - 뉴스 기사 전처리 : 날짜 타입 변경, 공백처리, 불용어 처리, 기사 길이가 140 이사 삭제
    
    | 결측지 제거 후 | dataframe shape | (114308, 3) |
    | 결측지 제거 전 | dataframe shape | (114208, 3) |

   
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
    - 모든 기사 워드클라우드 
<img src="https://github.com/yumioh/data_analysis/assets/38059057/bee57bcf-e516-42c3-bbb7-7daf00504dec" width="70%" height="50%"/>

    - 버즈량이 가장 많은 일자 워드 클라우드 : 8월 16일과 8일 
<div class="image-container">
    <img src="https://github.com/yumioh/data_analysis/assets/38059057/b5280d9d-82f0-4a3a-bc75-c02f639f359b" width="48%" height="50%" margin="5px"/>
    <img src="https://github.com/yumioh/data_analysis/assets/38059057/a6112af7-8ebf-443b-b024-f297509a080f" width="48%" height="50%"/>
</div>
    

## 5. 결론
    - 기사 버즈량과 주가를 비교 했을때 크게 주가에 크게 영향이 없었고, 삼성전자가 주제라 카테고리에서 경제 부분에 많이 나타나는 것으로 보입니다
      8월 16일과 8일이 가장 버즈량이 많은 날로 워드 클라우드로 분석해서 봤을때 지난헤 8월에 태풍 카눈과 잼버린 이슈로 인해 
      두 단어와 관련된 키워드가 대부분인걸 워드 클라우드로 확인이 가능합니다
      8월달 뉴스만 수집한 데이터로 그 수가 충분하지 않아 단순히 그달에 어떤 이슈가 있었는지 정도밖에 파악이 불가합니다
      현재 데이터로 수 자체가 적어 표본의 대표성을 가질 수 없어 뉴스와 주가 상관관계가 있다는 점을 알기 어렵습니다

