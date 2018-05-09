
import json
import glob
import requests
from bs4 import BeautifulSoup
import pandas as pd


def remove_column(df, drop_list):
	for col_name in drop_list:
		df.drop(col_name, axis=1, inplace=True)
	return df


path ='sample2' # use your path
allFiles = glob.glob(path + "/*.csv")
print (allFiles)
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
    print (file_)
frame = pd.concat(list_)
#frame = remove_column(frame, ['Unnamed: 0'])

frame = frame.dropna(axis=0, how='any')
print (len(frame))
frame.to_csv("sample2/sample_all_1.csv")



"""
df1 = pd.read_csv('sample_all.csv',index_col=['imdbID'], header=0)
df2 = pd.read_csv('sample2/model1_20171.csv',index_col=['imdbID'], header=0)
print (len(df1), len(df2))

result = pd.concat([df1, df2], ignore_index=False,axis=1, join='inner')
result.to_csv("result.csv")
print (len(result))
"""