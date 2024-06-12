import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import time

pages = 1
def get_data(url):
    _2ch_blog = pd.DataFrame()
    arr = []

    url_main = 'https://2ch.hk'
    type_video = ['mp4', 'webm', 'youtube']
    headers =  {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    }
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.text, features='lxml')
    articles = soup.find_all('div', class_ = 'thread')
    for article in articles:
        date = article.find('div', class_ = 'post').find('div', class_ = 'post__details').find_all(
            'span', class_= 'post__detailpart')[1].find('span').text

        links = article.find('div', class_ = 'post__images').find_all('figure',
                                                                                           class_ =
                                                                                           'post__image')

        for i in links:
            link = i.find('a').get('href')

            link_split = link.split('.')
            if link_split[-1] in type_video:
                links = link
            else:
                continue

            arr.append({'Data': date, 'link': url_main + links})
            time.sleep(0.1)

    _2ch_blog = pd.concat([_2ch_blog, pd.DataFrame(arr)], ignore_index=True)
    _2ch_blog = _2ch_blog.sort_values('Data', ascending=False)
    print(_2ch_blog)


get_data('https://2ch.hk/b/')
