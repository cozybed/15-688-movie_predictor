from time import time, sleep
from requests import get
from warnings import warn
from bs4 import BeautifulSoup
from random import randint
import os
from collections import defaultdict
import csv

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}


# For every year in the interval 2000-2017

def get_id (url):
    idx_f =  url.find("/title/")
    idx_r = url.find("/?ref")
    return (url[idx_f + 7: idx_r])


def get_details(url):
    response = get(url, headers=headers)
    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')
    open('save.html', 'w').write(response.text)
    res = {}


    # get url
    imdbID = get_id(url)
    print (imdbID)
    res['imdbID'] = imdbID

    '''
    # get name
    name_h4 = page_html.find('h1', itemprop="name").text
    res['name'] = name_h4.split('\xa0')[0]

    
    # get directors
    span = page_html.find('span', itemprop="director")
    director_name = span.a.text
    res['director'] = director_name
   

    # run time
    time = page_html.find('time', itemprop="duration")
    time = time.text.strip('\n ')
    duration = 0
    for item in time.split():
        if 'h' in item:
            duration += 60 * int(item[:-1])
        if 'min' in item:
            duration += int(item[:-3])
    res['run time'] = str(duration)
    '''
    '''
    # get genres
    genres = page_html.find_all('span', class_="itemprop", itemprop="genre")
    genres_text = []
    for genre in genres:
        genres_text.append(genre.text)
    res['genres'] = '|'.join(genres_text)
    '''

    # release date, Budget, Opening Weekend USA, Gross USA, Cumulative Worldwide Gross, production CO.
    details_div = page_html.find('div', id="titleDetails")
    for div in details_div.find_all('div', class_="txt-block"):
        
        '''
        if 'Release Date' in div.text:
            temp = div.text.strip('\n ').split('\n')[0]
            res['release date'] = temp[temp.find(':') + 1:].strip().rsplit(' ', 1)[0]
        '''

        if 'Budget:' in div.text:
            temp = div.text.strip('\n ').split('\n')[0]
            res['budget'] = temp[temp.find(':') + 1:].strip()[1:].replace(',', '')

        if 'Opening Weekend USA' in div.text:
            temp = div.text.strip('\n ').split('\n')[0]
            res['Opening Weekend USA'] = temp[temp.find(':') + 1:].strip()[1:].replace(',', '')

        if 'Gross USA' in div.text:
            temp = div.text.strip('\n ').split('\n')[0]
            res['Gross USA'] = temp[temp.find(':') + 1:].strip()[1:].replace(',', '').split()[0]

        if 'Cumulative Worldwide Gross' in div.text:
            temp = div.text.strip('\n ').split('\n')[0]
            res['Cumulative Worldwide Gross'] = temp[temp.find(':') + 1:].strip()[1:].replace(',', '').split()[0]

        '''
        if 'Production Co' in div.text:
            temp = [x.strip(' \n,') for x in div.text.strip('\n ').split('\n')[2:-1]]
            res['Production Co'] = '|'.join(temp)
        '''

    # find critic and reviews:
    review_div = page_html.find('div', class_="titleReviewBarItem titleReviewbarItemBorder")
    for a in review_div.find_all('a'):
        if 'user' in a.text:
            res['user review number'] = a.text.split()[0].replace(',', '')
        if 'critic' in a.text:
            res['critic number'] = a.text.split()[0].replace(',', '')

    # get rating value
    '''
    ratingValue_div = page_html.find('div', class_="ratingValue")
    value = ratingValue_div.strong['title']
    res['imdb_rating'] = value.split()[0]
    res['votes'] = value.split()[3].replace(',', '')
    s = page_html.find('div', class_='title_wrapper').find_next('div').strings
    s = list(s)
    res['certificate'] = s[1].strip()
    '''
    return res


def gogo(years=['2003'], pages=['1','2','3','4','5','6','7','8']):
    samples = []

    # Preparing the monitoring of the loop
    start_time = time()
    requests = 0

    for year_url in years:

        # For every page in the interval 1-4
        for page in pages:

            # Make a get request
            response = get(
                'https://www.imdb.com/search/title?title_type=feature&sort=boxoffice_gross_us,desc&release_date=' + year_url +
                '&page=' + page, headers=headers)

            # Pause the loop
            sleep(randint(0, 3))

            # Monitor the requests
            requests += 1
            elapsed_time = time() - start_time
            print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))

            # Throw a warning for non-200 status codes
            if response.status_code != 200:
                warn('Request: {}; Status code: {}'.format(requests, response.status_code))

            # Break the loop if the number of requests is greater than expected

            # Parse the content of the request with BeautifulSoup
            page_html = BeautifulSoup(response.text, 'html.parser')

            # Select all the 50 movie containers from a single page
            mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')

            # For every movie of these 50
            for container in mv_containers:
                datapoint = defaultdict(str)
                try:
                    # If the movie has a Metascore, then:
                    if container.find('div', class_='ratings-metascore') is not None:
                        # Scrape the name
                        name = container.h3.a.text
                        # datapoint['name'] = name
                        detail_url = container.h3.a['href']

                        

                        details = get_details('https://www.imdb.com' + detail_url)
                        for key, value in details.items():
                            datapoint[key] = value
                        #print(datapoint)
                        samples.append(datapoint)
                except Exception as e:
                    print(e)
            keys = set()
            for feature_dict in samples:
                for key in feature_dict.keys():
                    keys.add(key)
            keys = list(keys)
            with open('sample2/model1_' + year_url + page+ ".csv", 'w') as output_file:
                output_file.write(','.join(keys) + '\n')
                for feature in samples:
                
                    output_file.write(','.join([feature[x] for x in keys]) + '\n')

    return samples


samples = gogo()