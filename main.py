import json
import os

import requests
import datetime

import config

req = input("Введите запрос: ")
url = 'https://serpapi.com/search.json'

params = {
    "engine": "youtube",
    "search_query": req,
    "gl": "ru",
    "hl": "ru",
    "api_key": config.api_key
}

r = requests.get(url, params=params)

r_json = r.json()

folder_name = 'history'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

date_info = datetime.datetime.now()
file_name = 'request_{0}.{1}.{2}_{3}.{4}.{5}.{6}.json'.format(str(date_info.year),
                                                              str(date_info.month),
                                                              str(date_info.day),
                                                              str(date_info.hour),
                                                              str(date_info.minute),
                                                              str(date_info.second),
                                                              str(date_info.microsecond))

with open(folder_name + os.path.sep + file_name, 'w', encoding='utf-8') as f:
    json.dump(r_json, f, ensure_ascii=False, indent=4)

try:
    playlist_results = r_json['playlist_results']
    # print(playlist_results)
except KeyError:
    playlist_results = None

try:
    video_results = r_json['video_results']
    # print(video_results)
except KeyError:
    video_results = None

print('  Результаты по запросу "' + req + '":')

if playlist_results is not None:
    print('Плейлисты:')
    for i in range(10):
        try:
            playlist = playlist_results[i]
            print(str(i + 1) + ". " + playlist['title'])
            print('Автор: ' + playlist['channel']['name'])
            print('Ссылка на автора: ' + playlist['channel']['link'])
            print('Количество видео: ' + str(playlist['video_count']))
            print('Ссылка: https://www.youtube.com/playlist?' + str(playlist['link']).split('&')[1])
            print('Смотреть: ' + playlist['link'])
        except:
            pass

if video_results is not None:
    if playlist_results is not None:
        print('')
    print('Видео:')
    for i in range(10):
        try:
            video = video_results[i]
            print(str(i + 1) + ". " + video['title'])
            print('Автор: ' + video['channel']['name'])
            print('Ссылка на автора: ' + video['channel']['link'])
            print('Опубликовано ' + video['published_date'])
            print('Просмотры: ' + str(video['views']))
            print('Длительность: ' + video['length'])
            print('Описание: ' + video['description'])
            print('Смотреть: ' + video['link'])
        except:
            pass
