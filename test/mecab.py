import os
existing_path = os.environ.get('PATH', '')
new_path = r'C:\mecab\bin'
os.environ['PATH'] = new_path + os.pathsep + existing_path

print(os.environ['PATH'])


from konlpy.tag import Mecab
mecab = Mecab()
mecab.nouns("무궁화꽃이피었습니다.")