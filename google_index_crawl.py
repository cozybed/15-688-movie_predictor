from pytrends.request import TrendReq
import socket
import socks
import requests
import csv
import datetime

one_week = datetime.timedelta(days=7)
four_week = datetime.timedelta(days=30)
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# socket.socket = socks.socksocket
pytrends = TrendReq(hl='en-US', tz=360)
from bs4 import BeautifulSoup

month_to_number = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}

def format_date(date):
    date = date.split()
    date = date[4] + '-' + month_to_number[date[3]] + '-' + date[2]
    return date
def get_title_id(query):
    url = 'https://www.imdb.com/find'
    response = requests.get(url, params={'q': query, 'ref_': 'nv_home'})
    #print(response.url)
    # print(response.text)
    page_html = BeautifulSoup(response.text, 'html.parser')
    title = page_html.find('td', class_="result_text")
    # open('dave2.html', 'w').write(response.text)
    #print(title.text)
    return title.a['href']


def get_release_date(query):
    title = get_title_id(query)
    url = 'https://www.imdb.com'
    response = requests.get(url + title)
    #print(response.url)
    page_html = BeautifulSoup(response.text, 'html.parser')
    details_div = page_html.find('div', id="titleDetails")
    for div in details_div.find_all('div', class_="txt-block"):
        if 'Release Date' in div.text:
            temp = div.text.strip('\n ').split('\n')[0]
            return temp


date_file = open('./google_index.txt', 'w')
with open('./movie_metadata.csv', 'r') as file:
    csv_file = csv.reader(file)
    for index, row in enumerate(csv_file):
        # change this condition to run different portion of data
        #if index not in range (0, 500) and index not in range(1500,2000):
        #    continue
        if index % 500 == 0:
            print(index)
        try:
            title = row[11].strip('\xa0')
            date = get_release_date(title)
            date = format_date(date)
            #print(date)
    
            release_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            start_date = release_date - one_week
            end_date = release_date + four_week
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
    
            title = title.split('(')[0]
            title = str(title)
            kw_list = [title]
            #print(start_date + ' ' + end_date, title)
            pytrends.build_payload(kw_list, timeframe=start_date + ' ' + end_date, geo='', gprop='')
            res = pytrends.interest_over_time()
            #print(res)
            date_file.write(row[11] + '\n')
            date_file.write(res.to_csv() + '\n')
            date_file.flush()
        except:
            pass