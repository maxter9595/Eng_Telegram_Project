import csv
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup

from data_formation.english_html import write_dir
from data_formation.english_html import get_headers


def launch_get_requests(attempts: int, error_timeout: int,
                        promt_link: str, my_word: str,
                        os: str, browser: str) -> Optional[BeautifulSoup]:
    attempt_count = 0
    for _ in list(range(1, attempts + 1)):

        if attempts >= attempt_count:

            try:
                resp = requests.get(promt_link + my_word, timeout=10,
                                    headers=get_headers(os, browser))
                soup = BeautifulSoup(resp.content, "lxml")
                break

            except (requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError):
                print('requests.exceptions: повторная попытка...')
                time.sleep(error_timeout)
                attempt_count += 1

        else:
            return None

    return soup


def promt_site_parsing(soup: BeautifulSoup, my_word: str) -> dict:
    dict_pos = {}
    for item in soup.findAll("div", {"class": "cforms_result"}):
        for item2 in item.findAll("div", attrs={'translation-item'}):

            pos = item. \
                find("span", attrs={"class": "ref_psp"}).text

            word = item2. \
                find('span', attrs={'class': 'result_only sayWord'}).text

            try:
                example_en = item2. \
                    find('div', attrs={'class': 'samSource'}).text

                example_ru = item2. \
                    find('div', attrs={'class': 'samTranslation'}).text

            except AttributeError:
                example_en, example_ru = None, None

            try:
                trans = item. \
                    find('span', attrs={'class': 'transcription'}).text

            except AttributeError:
                trans = None

            if pos not in dict_pos:
                dict_pos[pos] = [{
                    'word': word,
                    'transcription': trans,
                    'example_en': example_en,
                    'example_ru': example_ru
                }]

            else:
                dict_pos[pos].append({
                    'word': word,
                    'transcription': trans,
                    'example_en': example_en,
                    'example_ru': example_ru
                })

    return {my_word: dict_pos}


def get_translation(my_word: str, os: str, browser: str) -> Optional[dict]:
    base_url = 'https://www.online-translator.com/'
    promt_link = base_url + 'translation/english-russian/'

    attempts = 3
    error_timeout = 30

    soup = launch_get_requests(attempts, error_timeout, promt_link,
                               my_word, os, browser)

    if not soup:
        return None

    else:
        dict_info = promt_site_parsing(soup, my_word)
        return dict_info


def write_promt_translation(word_list: list, pos_list: str,
                            os: str, browser: str) -> list:
    word_trans_data = []

    for my_word, pos in zip(word_list, pos_list):
        print(f'Обрабатываю слово {my_word}')

        try:
            trans = get_translation(my_word, os,
                                    browser)[my_word][pos][0]

        except KeyError:
            trans = None

        if trans:
            word_trans_data.append([
                trans['word'],
                my_word,
                trans['transcription'],
                trans['example_en'],
                trans['example_ru']
            ])

    csv_path = write_dir('data', 'dictionary_data_csv',
                         'promt_translation.csv')

    if word_trans_data:
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['ru_word', 'en_word', 'transcription',
                             'example_en', 'example_ru'])
            writer.writerows(word_trans_data)

        print('Статус: слова успешно переведены (переводчик Promt)')

        return word_trans_data
