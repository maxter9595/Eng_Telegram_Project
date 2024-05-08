import os
import random
import re
import time
from string import ascii_letters
from typing import Optional

import requests
import telebot
from bs4 import BeautifulSoup
from fake_headers import Headers
from telebot import TeleBot, types


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'


class TelebotFunctional:

    def write_dir(self, *args) -> os.path:
        abspath = os.path.abspath(args[0])
        root_dir = ''

        for arg in args[1:]:
            if root_dir:
                root_dir = os.path.join(root_dir, arg)
            else:
                root_dir = os.path.join(abspath, arg)

        return root_dir

    def get_headers(self, os: str, browser: str) -> dict:
        return Headers(os=os, browser=browser).generate()

    def write_mp3(self, url: str, file_path: str,
                  os: str, browser: str, attempts: int,
                  error_timeout: int) -> bool:
        attempt_count = 0

        for _ in list(range(1, attempts + 1)):
            if attempts >= attempt_count:
                try:
                    headers = self.get_headers(os, browser)
                    resp = requests.get(url, headers=headers, timeout=10)
                    resp.raise_for_status()

                    with open(file_path, "wb") as file:
                        file.write(resp.content)
                    return True

                except (requests.exceptions.ConnectTimeout,
                        requests.exceptions.ReadTimeout,
                        requests.exceptions.ConnectionError):
                    print(f'requests.exceptions: не удалось обработать ссылку {url}')
                    time.sleep(error_timeout)

            else:
                return False

    def launch_get_requests(self, attempts: int, error_timeout: int,
                            promt_link: str, my_word: str,
                            os: str, browser: str) -> Optional[BeautifulSoup]:
        attempt_count = 0
        for _ in list(range(1, attempts + 1)):
            if attempts >= attempt_count:
                try:
                    resp = requests.get(
                        promt_link + my_word,
                        timeout=10,
                        headers=self.get_headers(os, browser)
                    )
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

    def promt_site_parsing(self, soup: BeautifulSoup, my_word: str) -> dict:
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

    def get_translation(self, my_word: str, os: str, browser: str) -> Optional[dict]:
        base_url = 'https://www.online-translator.com/'
        promt_link = base_url + 'translation/english-russian/'

        attempts = 3
        error_timeout = 30
        soup = self.launch_get_requests(attempts, error_timeout,
                                        promt_link, my_word, os, browser)
        if not soup:
            return None
        else:
            dict_info = self.promt_site_parsing(soup, my_word)
            return dict_info

    def count_words(self, user_database: list) -> int:
        return len(set([
            word_dict.get('en_word')
            for word_dict in user_database
        ]))

    def get_oxford_dict_data(self, en_word: str, os: str,
                             browser: str) -> dict:
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
            headers = self.get_headers(os, browser)
            resp = requests.get(l, headers=headers)

            if 200 <= int(resp.status_code) < 300:
                soup = BeautifulSoup(resp.content, "lxml")

                for item in soup.findAll("div", {"class": "webtop"}):
                    try:
                        pos_name = item.find('span', attrs={'class': 'pos'}).text
                        mp3_find = item.find('div', attrs={'class': 'pron-uk'})
                        mp_3_url = re.search(r"mp3=(.+mp3.)", str(mp3_find)). \
                            group(1).replace('"', '')
                        data_dict[pos_name] = {'mp_3_url': mp_3_url}
                    except AttributeError:
                        pass

        return data_dict

    def receive_pos_oxford_dict_data(self, en_word: str, pos: str,
                                     os: str, browser: str) -> str:
        data_dict = self.get_oxford_dict_data(en_word, os, browser)

        if pos in data_dict:
            data_dict = data_dict.get(pos)

        mp_3_url = data_dict.get('mp_3_url', '')
        return mp_3_url

    def receive_promt_data(self, en_word: str, pos: str,
                           os: str, browser: str) -> tuple:
        dict_trans = self.get_translation(en_word, os, browser)

        try:
            dict_trans_pos = dict_trans[en_word][pos][0]
        except KeyError:
            dict_trans_pos = {}

        ru_word = dict_trans_pos.get('word', None)
        word_trans = dict_trans_pos.get('transcription', '')
        word_en_example = dict_trans_pos.get('example_en', 'No example')
        word_ru_example = dict_trans_pos.get('example_ru', 'Пример отсутствует')

        return ru_word, word_trans, word_en_example, word_ru_example

    def write_user_mp3(self, en_word: str, mp_3_url: str,
                       word_trans: str, os: str, browser: str) -> None:
        if mp_3_url:
            if word_trans:
                mp3_path = self.write_dir('data', 'eng_audio_files_mp3',
                                          f'{en_word} {word_trans}.mp3'). \
                    replace('telebot_connection/telebot_functional/', '')
            else:
                mp3_path = self.write_dir('data', 'eng_audio_files_mp3',
                                          f'{en_word[::-1].replace(" ", "", 1)[::-1]}.mp3'). \
                    replace('telebot_connection/telebot_functional/', '')

            self.write_mp3(mp_3_url, mp3_path, os, browser, attempts=3, error_timeout=10)

    def get_word_info(self, add_en_word: str, pos_list: list,
                      os: str, browser: str) -> list:
        mp3_bool = False
        word_list = []

        for pos in pos_list:
            mp_3_url = self.receive_pos_oxford_dict_data(add_en_word, pos,
                                                         os, browser)

            ru_word, word_trans, word_en_example, \
                word_ru_example = self.receive_promt_data(add_en_word, pos,
                                                          os, browser)

            if not mp3_bool:
                self.write_user_mp3(add_en_word, mp_3_url,
                                    word_trans, os, browser)
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

    def get_mp3_audio(self, bot: TeleBot, data: dict, hint: str,
                      my_message: telebot.types.Message) -> None:
        if 'Допущена ошибка!' not in hint:
            try:
                word = data['target_word']
                transcription = data['transcription']
                if transcription.split():
                    mp3_name = f"{word} {transcription}.mp3"
                else:
                    mp3_name = f"{word}"[::-1]. \
                                   replace(" ", "", 1)[::-1] + '.mp3'

                mp3_path = f"data/eng_audio_files_mp3/{mp3_name}"
                bot.send_audio(my_message.chat.id,
                               open(mp3_path, 'rb'),
                               title=f"{mp3_name}",
                               performer="Translator")
                print(f'MP3 файл загружен: {mp3_path}')

            except FileNotFoundError:
                print(f'Аудиозапись слова не удалось найти: {mp3_path}')

    def setup_buttons(self, target_word: str, others: list) -> tuple:
        target_word_btn = types.KeyboardButton(target_word)
        other_words_btns = [
            types.KeyboardButton(word)
            for word in others
        ]

        buttons = []
        buttons.append(target_word_btn)
        buttons.extend(other_words_btns)
        random.shuffle(buttons)

        next_btn = types.KeyboardButton(Command.NEXT)
        add_word_btn = types.KeyboardButton(Command.ADD_WORD)
        delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)

        btn_list = [
            next_btn,
            add_word_btn,
            delete_word_btn
        ]
        buttons.extend(btn_list)

        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(*buttons)

        return buttons, markup

    def get_button_states(self) -> tuple:
        add_word_btn_name = Command.ADD_WORD.lower()
        delete_word_btn_name = Command.DELETE_WORD.lower()
        next_word_btn_name = Command.NEXT.lower()

        return add_word_btn_name, delete_word_btn_name, next_word_btn_name

    def show_hint(self, *lines: tuple) -> str:
        return '\n'.join(lines)

    def hello_text(self) -> str:

        text = """
        Привет 👋 Давай попрактикуемся в английском языке.

        Тренировки можешь проходить в удобном для себя темпе.

        Для этого воспрользуйся следующимим инструментами:
        добавить слово ➕,
        удалить слово 🔙.

        Ну что, начнём ⬇️
        """

        return '\n'.join(
            line.lstrip()
            for line in text.splitlines()
        )

    def show_target(self, data: dict) -> str:
        target = data['target_word']
        trans = data['translate_word']
        return f"{target} -> {trans}"

    def get_example(self, bot: TeleBot,
                    message: telebot.types.Message,
                    markup: telebot.types.ReplyKeyboardMarkup,
                    data: dict, hint: str) -> None:

        if 'Допущена ошибка!' not in hint:
            if data['en_example'] != 'No example' and \
                    data['ru_example'] != "Пример отсутствует":
                en_example = data["en_example"]
                ru_example = data["ru_example"]

                example_text = self.show_hint('*Пример предложения:*',
                                              f'"{en_example}"',
                                              f'"{ru_example}"')

                bot.send_message(message.chat.id,
                                 example_text,
                                 reply_markup=markup,
                                 parse_mode='Markdown')

    def check_word_letters(self, word: str, eng_bool: bool = True) -> bool:
        if eng_bool:
            letter_condition = lambda l: l in ascii_letters
        else:
            letter_condition = lambda l: re.match('[а-яА-Я]', l) \
                                         or l in ('ё', 'Ё')

        for w in word:
            if w.isalpha():
                if letter_condition(w):
                    continue
                else:
                    return False
            else:
                return False
        return True

    def get_random_pos_database(self, user_database: list,
                                pos_list: list = ['noun', 'verb', 'adjective']
                                ) -> list:
        pos = random.choice(pos_list)

        pos_database = [
            word_dict for word_dict in user_database
            if word_dict.get('pos_name') == pos
        ]
        return pos_database

    def get_random_words(self, pos_database: list) -> tuple:
        word_keys = [
            'en_word',
            'ru_word'
        ]

        en_pos_list, ru_pos_list = (
            [d.get(k) for d in pos_database]
            for k in word_keys
        )

        random.shuffle(ru_pos_list)
        translate = random.choice(ru_pos_list)

        filter_word = [
            d['en_word'] for d in pos_database
            if d['ru_word'] == translate
        ]

        if len(filter_word) > 1:
            target_word = random.choice(filter_word)
        else:
            target_word = filter_word[0]

        other_info_keys = [
            'en_trans',
            'en_example',
            'ru_example'
        ]

        transcription, en_example, \
            ru_example = (
            [d[key] for d in pos_database
             if d['en_word'] == target_word][0]
            for key in other_info_keys
        )

        others = [
            w for w in en_pos_list
            if w not in filter_word
        ]
        random_others = random.sample(others, 3)

        return target_word, translate, random_others, transcription, en_example, ru_example
