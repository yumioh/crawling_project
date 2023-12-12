import pandas as pd

stockFilePath = './data/samsung_stocks_2308.csv'
newsFilePath = './data/samsung_2308.csv'
newsData = pd.read_csv(newsFilePath)
print(newsData)