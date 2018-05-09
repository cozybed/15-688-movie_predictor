
import json
import glob
import requests
from bs4 import BeautifulSoup
import pandas


def remove_column(df, drop_list):
	for col_name in drop_list:
		df.drop(col_name, axis=1, inplace=True)
	return df

urls = []

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}


json_arr = []
for url in urls:
	response = requests.get(url, headers = headers)
	root = BeautifulSoup(response.text, "html5lib")
	items = root.find_all ("div", class_="lister-item mode-advanced")

	for item in items:
		title = str(item.find("h3").find("a"))
		idx_f =  title.find("/title/")
		idx_r = title.find("/?ref")
		mid =  (title[idx_f + 7: idx_r])


		url_token = "http://www.omdbapi.com/?apikey=8505fa3b&i=" + mid
		test  = requests.get(url_token, headers = headers)
		test_json = json.loads(test.text)
		json_arr.append(test_json)

df = pandas.DataFrame.from_dict(json_arr, orient='columns')
#df.to_csv("sample/sample_2001.csv")


path ='sample' # use your path
allFiles = glob.glob(path + "/*.csv")
frame = pandas.DataFrame()
list_ = []
for file_ in allFiles:
    df = pandas.read_csv(file_,index_col=None, header=0)
    list_.append(df)
    print (file_)
frame = pandas.concat(list_)
frame = remove_column(frame, ['Website','Plot', 'Response', 'Unnamed: 0','Type', 'Error','Poster'])

frame = frame.dropna(axis=0, how='any')
print (len(frame))
frame.to_csv("sample_all.csv")

