import json

import requests
import pandas as pd

from pprint import pprint

def get_data():
    url_main = 'https://2ch.hk'
    pages = [1,2,3,4,5,6,7,8,9,10]
    page = 1
    # with open ('data.json','w') as file:
    #     json.dump(data['threads'],file)
    _2ch_blog = pd.DataFrame()
    arr = []
    data_dict = {}
    while page !=len(pages):
        req = requests.get(f'https://2ch.hk/b/{page}.json')
        data = req.json()
        for info in data['threads']:
            num = info['posts'][0]['num']
            date = info['posts'][0]['date']
            link = info['posts'][0]['files'][0]['name'].split('.')
            if link[-1] == 'mp4' or link[-1] == 'webm':
                link = info['posts'][0]['files'][0]['path']
                arr.append({'Data': date, 'link': url_main + link})
                data_dict[num] = {
                    'date': date,
                    'link': url_main + link
                }
            else:
                continue

        page+=1
    with open ('dict.json', 'w') as file:
        json.dump(data_dict,file,indent=4, ensure_ascii=False)

    _2ch_blog = pd.concat([_2ch_blog, pd.DataFrame(arr)], ignore_index=True)
    _2ch_blog = _2ch_blog.sort_values('Data', ascending=False)
    print(_2ch_blog)
    return _2ch_blog.to_csv('2ch.csv')


def check_new_update():
    with open('dict.json') as file:
        data_dict = json.load(file)
    url_main = 'https://2ch.hk'
    pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    page = 1
    fresh_data_dict = {}

    while page != len(pages):
        req = requests.get(f'https://2ch.hk/b/{page}.json')
        data = req.json()
        for info in data['threads']:
            num = str(info['posts'][0]['num'])
            if num in data_dict:
                continue
            else:
                date = info['posts'][0]['date']
                link = info['posts'][0]['files'][0]['name'].split('.')

                if link[-1] == 'mp4' or link[-1] == 'webm':
                    link = info['posts'][0]['files'][0]['path']

                    data_dict[num] = {
                        'date': date,
                        'link': url_main + link
                    }

                    fresh_data_dict[num] = {
                        'date': date,
                        'link': url_main+link
                    }
        page+=1
    print(data_dict)
    print(fresh_data_dict)
    with open ('dict.json', 'w') as file:
        json.dump(data_dict,file,indent=4, ensure_ascii=False)
    return fresh_data_dict
def caregory():
    a = input('Выберете категорию: ')
    return a
def main():
    get_data()
    check_new_update()
if __name__ == '__main__':
    main()


