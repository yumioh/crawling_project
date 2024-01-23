import pandas as pd

# 예시 데이터프레임 생성
data = {'날짜': [['2020-01-01'], ['2020-01-02'], ['2020-01-03'], ['2020-01-04']],
        'pos_content': [['대통령','대통령1','대통령2', []], ['년','년3','년4'], ['미국인', [],'미국인3','미국인'], ['오바마', '오바마',[]]]}
df = pd.DataFrame(data)
print('삭제 전:', df)

# # 리스트의 각 요소를 문자열로 결합하는 함수 정의
# def join_list_to_string(lst):
#     return ', '.join(map(str, lst))

# # '날짜' 열을 문자열로 변환
# df['날짜'] = df['날짜'].apply(join_list_to_string)

# 'pos_content' 열의 빈 리스트 제거
df['pos_content'] = df['pos_content'].apply(lambda x: ', '.join(map(str, [i for i in x if i])))

print('---------------------------------------------------')

# 결과 확인
print('삭제 후 : ', df)
