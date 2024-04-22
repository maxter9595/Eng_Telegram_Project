import re
import os
import csv

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_oxford_data(soup:BeautifulSoup, base_url:str) -> list:
    
    word_list = []
    
    for item in soup.findAll("ul", {"class":"top-g"}):
            for item2 in item.findAll("li"):
                
                try:
                    word = item2.find('a').text
                    pos = item2.find('span', attrs = {'class':'pos'}).text
                    
                    lvl = item2.\
                        find('span', attrs = {'class':'belong-to'}).text
                    
                    mp3_find = item2.find('div', attrs = {'class': 
                        'sound audio_play_button icon-audio pron-uk'})
                    mp3_link = base_url[:-1] + re.search(r"mp3=(.+mp3.)",
                                                str(mp3_find)).\
                                                group(1).replace('"', '')
                                                
                except AttributeError:
                    word = None
                    
                if word:
                    print(f'Обрабатываю слово {word}')
                    word_list.append([word, pos, lvl, mp3_link])
                    
    return word_list


def write_dir(*args) -> os.path:
    
    abspath = os.path.abspath(args[0])
    root_dir = ''
    
    for arg in args[1:]:
        
        if root_dir:
            root_dir = os.path.join(root_dir, arg)
            
        else:
            root_dir = os.path.join(abspath, arg)
            
    return root_dir


def get_headers(os:str, browser:str) -> dict:
    
    return Headers(os=os, browser=browser).generate()


def write_oxford_data(os:str, browser:str) -> list:
    
    BASE_URL = 'https://www.oxfordlearnersdictionaries.com/'
    oxford5000_url = BASE_URL + 'wordlists/oxford3000-5000'
    
    headers = get_headers(os, browser)
    resp = requests.get(oxford5000_url, headers=headers)
    soup = BeautifulSoup(resp.content, "lxml")
    
    data = get_oxford_data(soup, BASE_URL)
    
    col_names = ['word', 'pos', 'level', 'mp3_url']
    csv_path = write_dir('data', 'dictionary_data_csv', 
                        'oxford5000_dictionary.csv')
    
    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        writer.writerows(data)
    
    print('Статус: английские слова словаря Oxford 5000 получены')
    
    return data