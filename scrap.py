
import json

import requests
from bs4 import BeautifulSoup
import pandas




urls_2016 = [
'https://www.imdb.com/search/title?year=2007&title_type=feature&view=advanced&sort=boxoffice_gross_us,desc&page=1&ref_=adv_nxt',
'https://www.imdb.com/search/title?year=2007&title_type=feature&view=advanced&sort=boxoffice_gross_us,desc&page=2&ref_=adv_nxt',
'https://www.imdb.com/search/title?year=2007&title_type=feature&view=advanced&sort=boxoffice_gross_us,desc&page=3&ref_=adv_nxt',
'https://www.imdb.com/search/title?year=2007&title_type=feature&view=advanced&sort=boxoffice_gross_us,desc&page=4&ref_=adv_nxt',
'https://www.imdb.com/search/title?year=2007&title_type=feature&view=advanced&sort=boxoffice_gross_us,desc&page=5&ref_=adv_nxt',
'https://www.imdb.com/search/title?year=2007&title_type=feature&view=advanced&sort=boxoffice_gross_us,desc&page=6&ref_=adv_nxt',
'https://www.imdb.com/search/title?year=2007&title_type=feature&view=advanced&sort=boxoffice_gross_us,desc&page=7&ref_=adv_nxt'

]

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}


json_arr = []

for url in urls_2016:

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
	print ("....")

df = pandas.DataFrame.from_dict(json_arr, orient='columns')
df.to_csv("sample/sample_2007.csv")
print (df)
