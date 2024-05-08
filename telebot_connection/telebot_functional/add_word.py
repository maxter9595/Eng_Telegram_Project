import os
# import sys
import re
import time
from typing import Optional

# import bs4
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
# from telebot import TeleBot

# sys.path.insert(1, os.path.join(os.path.abspath(os.getcwd())))
# from data_formation.english_html import write_dir, get_headers
# from data_formation.english_mp3 import write_mp3
# from data_formation.translation_html import get_translation
# from telebot_connection.telebot_functional.cmd_state import get_button_states




def write_dir(*args) -> os.path:
    abspath = os.path.abspath(args[0])
    root_dir = ''

    for arg in args[1:]:

        if root_dir:
            root_dir = os.path.join(root_dir, arg)

        else:
            root_dir = os.path.join(abspath, arg)

    return root_dir

def get_headers(os: str, browser: str) -> dict:
    return Headers(os=os, browser=browser).generate()

def write_mp3(url: str, file_path: str, os: str, browser: str,
              attempts: int, error_timeout: int) -> bool:
    attempt_count = 0
    for _ in list(range(1, attempts + 1)):

        if attempts >= attempt_count:

            try:
                headers = get_headers(os, browser)
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()

                with open(file_path, "wb") as fout:
                    fout.write(resp.content)

                return True

            except (requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError):
                print(f'requests.exceptions: не удалось обработать ссылку {url}')
                time.sleep(error_timeout)

        else:
            return False

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


# def form_db_dict(en_word:str, ru_word: str, en_trans:str='',
#                     mp_3_url:str='', en_lvl_code:str='none',
#                     en_lvl_name:str='unidentified',
#                     en_example:str='No example',
#                     ru_example:str='Пример отсутствует') -> dict:
#
#     return {
#             'en_word': en_word,
#             'en_trans': en_trans,
#             'mp_3_url': mp_3_url,
#             'en_lvl_code': en_lvl_code,
#             'en_lvl_name': en_lvl_name,
#             'en_example': en_example,
#             'ru_example': ru_example,
#             'ru_word': ru_word
#         }


def count_words(user_database:list) -> int:

    return len(
                set(
                    [word_dict.get('en_word')
                    for word_dict in user_database]
                )
            )

#
# def print_answer(bot:TeleBot, cid:int, user_database:list,
#                     new_word_bool:bool = False) -> None:
#
#     if new_word_bool is False:
#         bot.send_message(cid, 'Английское слово уже существует')
#
#     word_c = count_words(user_database)
#     count_msg = f'Текущее количество английских слов - {word_c} шт.'
#
#     bot.send_message(cid, count_msg)


# def get_en_lvl_code(item:bs4.element.Tag) -> str:
#
#     eng_lvl_codes = (
#                     'a1',
#                     'a2',
#                     'b1',
#                     'b2',
#                     'c1',
#                     'c2'
#                 )
#
#     en_lvl_code = ''
#
#     for c in eng_lvl_codes:
#
#         try:
#             en_pos_tag = str(item.\
#                 find('span', attrs = {'class':'ox3ksym_' + c}))
#
#             if 'None' not in en_pos_tag:
#                 en_lvl_code += en_pos_tag
#
#         except (AttributeError, TypeError):
#             pass
#
#     try:
#         en_lvl_code = re.search(r"class=.ox3ksym_(..)",
#                                 en_lvl_code).group(1)
#
#     except (IndexError,  KeyError, re.error):
#         en_lvl_code = 'none'
#
#     if en_lvl_code not in eng_lvl_codes:
#         en_lvl_code = 'none'
#
#     return en_lvl_code


def get_oxford_dict_data(en_word:str, os:str, 
                        browser:str) -> dict:

    base_url = 'https://www.oxfordlearnersdictionaries.com/'
    url_link = base_url + f'definition/english/{en_word}'
    
    url_link_list = [
                    url_link, 
                    url_link + "_1", 
                    url_link + "_2",
                    url_link + "_3"
                    ]

    data_dict = {}
    for l in url_link_list:
        
        headers = get_headers(os, browser)
        resp = requests.get(l, headers=headers)
        
        if 200 <= int(resp.status_code) < 300:
            soup = BeautifulSoup(resp.content, "lxml")
            
            
            for item in soup.findAll("div", {"class":"webtop"}):
                
                
                try:
                    pos_name = item.find('span', attrs = {'class':'pos'}).text
                    
                    mp3_find = item.find('div', attrs = {'class':'pron-uk'})
                    mp_3_url = re.search(r"mp3=(.+mp3.)", str(mp3_find)).\
                                            group(1).replace('"', '')
                    
                    # lvl_code = get_en_lvl_code(item)
                    #
                    # lvl_dict = {
                    #             'a1':'beginner',
                    #             'a2':'pre-intermediate',
                    #             'b1':'intermediate',
                    #             'b2':'upper-intermediate',
                    #             'c1':'advanced',
                    #             'c2':'proficiency',
                    #             'none':'unidentified'
                    #         }
                    
                    # data_dict[pos_name] = {
                    #                         'mp_3_url':mp_3_url,
                    #                         'en_lvl_code': lvl_code,
                    #                         'en_lvl_name': lvl_dict[lvl_code]
                    #                     }

                    data_dict[pos_name] = {'mp_3_url':mp_3_url}

                except AttributeError:
                    pass

    return data_dict


def receive_pos_oxford_dict_data(en_word:str, pos:str, 
                                os:str, browser:str) -> str:
    
    data_dict = get_oxford_dict_data(en_word, os, browser)
    
    if pos in data_dict:
        data_dict = data_dict.get(pos)
    
    mp_3_url = data_dict.get('mp_3_url', '')
    # en_lvl_code = data_dict.get('en_lvl_code', 'none')
    # en_lvl_name = data_dict.get('en_lvl_name', 'unidentified')

    # en_lvl_code,
    # en_lvl_name

    return mp_3_url

def receive_promt_data(en_word:str, pos:str, 
                        os:str, browser:str) -> tuple:
    
    dict_trans = get_translation(en_word, os, browser)
    
    try:
        dict_trans_pos = dict_trans[en_word][pos][0]
        
    except KeyError:
        dict_trans_pos = {}
    
    ru_word = dict_trans_pos.get('word', None)
    word_trans = dict_trans_pos.get('transcription', '')
    
    word_en_example = dict_trans_pos.get('example_en', 'No example')
    word_ru_example = dict_trans_pos.get('example_ru', 'Пример отсутствует')
    
    return (
            ru_word, 
            word_trans, 
            word_en_example, 
            word_ru_example
        )


def write_user_mp3(en_word:str, mp_3_url:str, word_trans:str, 
                    os:str, browser:str) -> None:
    
    if mp_3_url:
        
        if word_trans:
            mp3_path = write_dir('data', 'eng_audio_files_mp3', 
                        f'{en_word} {word_trans}.mp3').\
                replace('telebot_connection/telebot_functional/', '')
        else:
            mp3_path = write_dir('data', 'eng_audio_files_mp3', 
                        f'{en_word[::-1].replace(" ", "", 1)[::-1]}.mp3').\
                replace('telebot_connection/telebot_functional/', '')

        write_mp3(mp_3_url, mp3_path, os, browser, attempts=3, error_timeout=10)


def get_word_info(add_en_word:str, pos_list:list, os:str, browser:str) -> list:
    
    mp3_bool = False
    word_list = []
    
    for pos in pos_list:
        
        mp_3_url = receive_pos_oxford_dict_data(add_en_word, pos,
                                                os, browser)
        
        ru_word, word_trans, word_en_example,\
        word_ru_example = receive_promt_data(add_en_word, pos, 
                                                os, browser)

        if not mp3_bool:
            write_user_mp3(add_en_word, mp_3_url, word_trans, os, browser)
            mp3_bool = True
        
        user_dict = {
            'en_word': add_en_word,
            'ru_word': ru_word,
            'en_trans': word_trans,
            'pos_name': pos,
            'mp_3_url': mp_3_url,
            'en_example': word_en_example,
            'ru_example': word_ru_example
        }
        if user_dict not in word_list:
            word_list.append(user_dict)


    if len(word_list) > 1:
        for idx, word_dict in enumerate(word_list):
            if word_dict.get('ru_word') is None:
                word_list.pop(idx)

    return word_list


# if __name__ == '__main__':
#
#     res = get_word_info(add_en_word='glogobgabgolab',
#                          pos_list = ['noun', 'verb', 'adjective'],
#                          os='win', browser='chrome')
#     print(res)

    # cucumber => output: [{'en_word': 'cucumber', 'ru_word': 'огурец', 'en_trans': '[ˈkju:kʌmbə]', 'mp_3_url': 'https://www.oxfordlearnersdictionaries.com/media/english/uk_pron/c/cuc/cucum/cucumber__gb_2.mp3', 'en_example': 'Or take this sea cucumber.', 'ru_example': 'Или возьмём этот морской огурец.'}, {'en_word': 'cucumber', 'ru_word': None, 'en_trans': '', 'mp_3_url': '', 'en_example': 'No example', 'ru_example': 'Пример отсутствует'}, {'en_word': 'cucumber', 'ru_word': 'огуречный', 'en_trans': '[ˈkju:kʌmbə]', 'mp_3_url': '', 'en_example': 'Cold cucumber, corn and crab chowder.', 'ru_example': 'Холодный огуречный суп, кукурузный суп с крабами.'}]
    # glogogabgolab => output: [{'en_word': 'glogogabgolab', 'ru_word': None, 'en_trans': '', 'mp_3_url': '', 'en_example': 'No example', 'ru_example': 'Пример отсутствует'}]

    #     if user_dict not in user_database:
    #         user_database.append(user_dict)
    #         pos_check_list.append(pos)
    #
    # return (
    #         pos_check_list,
    #         ru_word
    #     )








#
#
#
#
# def update_user_database(pos_check_list:list,
#                         user_database:list,
#                         last_id:int) -> None:
#
#     n_len = len(pos_check_list)
#     last_dicts = user_database[-n_len:]
#
#     my_pos_list = []
#     if n_len > 1:
#
#         for last_dict, my_pos in zip(last_dicts, pos_check_list):
#             if last_dict.get('ru_word') == None:
#                 user_database.remove(last_dict)
#                 n_len -= 1
#
#             else:
#                 my_pos_list.append(my_pos)
#
#     else:
#         my_pos_list.append(pos_check_list[0])
#         n_len = 1
#
#     if last_id:
#         next_id = last_id + 1
#         new_id_list = list(range(next_id, next_id + n_len))
#     else:
#         next_id = 0
#         new_id_list = list(range(next_id, next_id + n_len))
#
#     for i, pos_name in enumerate(my_pos_list[::-1]):
#         idx = -1 * (i + 1)
#
#         user_database[idx].update({'id': new_id_list[idx],
#                                     'pos_name': pos_name})
#
#
# def add_en_word(bot:TeleBot, cid:int, user_database:list, add_en_word:str,
#                 pos_list:list=['noun', 'verb', 'adjective'],
#                 os:str='win', browser:str='chrome'):
#
#     unique_words = [
#                     word_dict.get('en_word') for word_dict in user_database
#                 ]
#
#     last_id = user_database[-1].get('id')
#
#     if add_en_word in unique_words:
#         print_answer(bot = bot, cid = cid, user_database = user_database)
#
#     else:
#         if add_en_word not in get_button_states():
#
#             pos_check_list, ru_word = pos_processing(user_database,
#                                                     add_en_word,
#                                                     pos_list,
#                                                     os,
#                                                     browser)
#
#             update_user_database(pos_check_list, user_database, last_id)
#
#             if ru_word:
#                 print_answer(bot = bot, cid = cid,
#                             user_database = user_database,
#                             new_word_bool = True)
#
#     return user_database