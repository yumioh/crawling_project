import pandas as pd
import re
import csvfile
data = { '날짜' : ['2020-01-01','2020-01-01','2020-01-01','2020-01-01'],
                         'pos_content': [[['단독'], ['전임자'], ['버락'], ['미국인'], ['존경']], [['내부'], ['순도'], ['학습'], ['편리'], ['각종']],
                                         [['갤럽'], ['지지'], ['국립대', '성당'], ['조지'], ['부시']] , [['미스터'], ['비스트'], ['식목일', '단과'], ['캠페인']]]
}
filtered_df_with_dated_df = pd.DataFrame(data)
print(filtered_df_with_dated_df)
