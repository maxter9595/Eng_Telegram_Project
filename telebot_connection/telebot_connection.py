import requests
import telebot
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from telebot_connection.telebot_functional.audio import get_mp3_audio
from telebot_connection.telebot_functional.example import get_example
from telebot_connection.telebot_functional.buttons import setup_buttons
from telebot_connection.telebot_functional.words import get_random_words
from telebot_connection.telebot_functional.words import get_random_pos_database
from telebot_connection.telebot_functional.cmd_state import Command, States
from telebot_connection.telebot_functional.cmd_state import get_button_states
from telebot_connection.telebot_functional.text import show_hint, show_target
# from telebot_connection.telebot_functional.known_users import check_known_users
from telebot_connection.telebot_functional.letters import check_word_letters
from telebot_connection.telebot_functional.add_word import get_word_info, count_words
# from telebot_connection.telebot_functional.add_word import count_words
from telebot_connection.telebot_functional.text import hello_text

from database_formation.table_filling import Repository


def get_database(user_dict, repository):
    user_id = user_dict.get('user_id')
    user_data = repository.get_users(user_id=user_id)
    if not user_data:
        repository.add_user(user_dict)
        repository.prepare_user_word_pairs(user_id=user_id)

def get_known_users(repository):
    users_data = repository.get_users()
    known_users = []
    for user_dict in users_data:
        known_users.append(user_dict.get('user_id'))
    return known_users

def get_user_words(repository, user_id):
    return repository.get_user_words(user_id=user_id)

def remove_user_word(repository, user_id, en_word):
    repository.remove_user_word(user_id=user_id, en_word=en_word)

def add_user_word(repository, user_id, data_dict):
    repository.add_user_word(user_id=user_id, data_dict=data_dict)

def get_words(repository, en_word, is_added_by_users):
    return repository.get_words(en_word=en_word, is_added_by_users=is_added_by_users)



def start_game_handler(bot: TeleBot, repository: object) -> None:
    @bot.message_handler(commands=['cards', 'start'])
    def create_cards(message):
        user_id = message.from_user.id

        user_dict = {
            'user_id': user_id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username
        }

        known_users = get_known_users(repository=repository)
        if user_id not in known_users:
            bot.send_message(user_id, hello_text())
            get_database(user_dict=user_dict,
                         repository=repository)

        # check_known_users(bot, cid, known_users,
        #                     users_word_dict, database)



        # user_database = users_word_dict[cid]
        user_database = get_user_words(repository=repository,
                                       user_id=user_id)

        pos_database = get_random_pos_database(user_database)

        target_word, translate, others, transcription, \
            en_example, ru_example = get_random_words(pos_database)

        global buttons
        buttons, markup = setup_buttons(target_word, others)
        chat_id = message.chat.id

        bot.send_message(chat_id,
                         f"Выбери перевод слова:\n🇷🇺 {translate}",
                         reply_markup=markup)

        bot.set_state(user_id, States.target_word, chat_id)

        with bot.retrieve_data(user_id, chat_id) as data:
            data['target_word'] = target_word
            data['translate_word'] = translate
            data['other_words'] = others
            data['transcription'] = transcription
            data['en_example'] = en_example
            data['ru_example'] = ru_example

    @bot.message_handler(func=lambda message: message.text == Command.NEXT)
    def next_cards(message):
        create_cards(message)


def delete_word_handler(bot: TeleBot, repository: object) -> None:
    @bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
    def delete_word(message):
        chat_id = message.chat.id
        user_dict = {
            'user_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username
        }

        known_users = get_known_users(repository=repository)
        if message.from_user.id not in known_users:
            bot.send_message(chat_id, hello_text())
            get_database(user_dict=user_dict,
                         repository=repository)

        # check_known_users(bot, cid, known_users, users_word_dict, database)

        msg = "Введите английское слово для удаления из базы данных:"
        send_msg = bot.send_message(chat_id, msg)
        bot.register_next_step_handler(send_msg, delete_user_en_word)

    def delete_user_en_word(message):
        cid = message.chat.id

        user_database = get_user_words(repository=repository,
                                       user_id=message.from_user.id)
        # user_database = users_word_dict[cid]

        user_en_word = message.text.lower()

        if user_en_word not in get_button_states():

            correct_letters = True
            if not check_word_letters(user_en_word, eng_bool=True):
                msg = show_hint(*[
                    'Слово должно содержать только английские буквы.',
                    '',
                    'Пожалуйста, повторите попытку нажатием на кнопку',
                    f'{Command.DELETE_WORD.lower()}'
                ])
                bot.send_message(cid, msg)
                correct_letters = False

            if correct_letters:
                remove_user_word(repository=repository,
                                 user_id=message.from_user.id,
                                 en_word=user_en_word)
                # new_user_database = [
                #     user_dict for user_dict in user_database
                #     if user_dict.get('en_word') != user_en_word
                # ]
                new_user_database = get_user_words(repository=repository,
                                                   user_id=message.from_user.id)

                if len(new_user_database) == len(user_database):
                    msg = 'Введенное слово отсутсвует в базе данных пользователя'
                    bot.send_message(cid, msg)
                else:
                    msg = f'Слово "{user_en_word}" удалено'
                    bot.send_message(cid, msg)

                    count_w = count_words(new_user_database)
                    msg = f'Текущее количество английских слов - {count_w} шт.'
                    bot.send_message(cid, msg)

                # for i in range(len(new_user_database)):
                #     user_dict = new_user_database[i]
                #     user_dict['id'] = i + 1
                #
                # print(new_user_database)


                # users_word_dict[cid] = new_user_database
                # print(new_user_database)

        else:
            cmd_name = user_en_word
            msg = f'Я принимаю только слова.\
                Команда {cmd_name} в расчет не берется.'
            bot.send_message(cid, msg)

def add_word_handler(bot: TeleBot, repository: object) -> None:
    @bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
    def add_word(message):
        cid = message.chat.id

        # check_known_users(bot, cid, known_users, users_word_dict, database)

        msg = "Введите английское слово для добавления в базу данных:"
        send_msg = bot.send_message(cid, msg)
        bot.register_next_step_handler(send_msg, add_user_en_word)

    def add_user_en_word(message):
        cid = message.chat.id
        user_en_word = message.text.lower()

        if user_en_word not in get_button_states():
            if '❌' not in user_en_word:

                check_word_bool = check_word_letters(user_en_word,
                                                     eng_bool=True)

                if check_word_bool:

                    user_database = get_user_words(repository=repository,
                                                   user_id=message.from_user.id)

                    existing_words = list(set([dict_.get('en_word') for dict_ in user_database]))

                    if user_en_word in existing_words:
                        bot.send_message(cid, 'Английское слово уже существует')

                    else:

                        try:
                            new_word_info = get_word_info(add_en_word=user_en_word,
                                                          pos_list = ['noun', 'verb', 'adjective'],
                                                          os='win',
                                                          browser='chrome')

                        except requests.exceptions.ConnectionError:
                            new_word_info = [{'ru_word': None}]


                        if new_word_info[0].get('ru_word') is None:

                            word_dict = new_word_info.pop()
                            data_dict = {
                                'en_word': word_dict.get('en_word'),
                                'en_trans': '',
                                'mp_3_url': '',
                                'pos_name': 'unidentified',
                                'ru_word': '',
                                'en_example': '',
                                'ru_example': ''
                            }
                            add_user_word(repository=repository,
                                          user_id=message.from_user.id,
                                          data_dict=data_dict)

                            msg = "Введите перевод английского слова:"
                            send_msg = bot.send_message(cid, msg)
                            bot.register_next_step_handler(send_msg,
                                                           add_user_ru_word)

                        else:
                            for word_dict in new_word_info:
                                data_dict = {
                                    'en_word': word_dict.get('en_word'),
                                    'en_trans': word_dict.get('en_trans'),
                                    'mp_3_url': word_dict.get('mp_3_url'),
                                    'pos_name': word_dict.get('pos_name'),
                                    'ru_word': word_dict.get('ru_word'),
                                    'en_example': word_dict.get('en_example'),
                                    'ru_example': word_dict.get('ru_example')
                                }
                                add_user_word(repository=repository,
                                              user_id=message.from_user.id,
                                              data_dict=data_dict)

                            new_user_database = get_user_words(repository=repository,
                                                               user_id=message.from_user.id)

                            if len(user_database) != len(new_user_database):
                                count_w = count_words(new_user_database)
                                msg = f'Текущее количество английских слов - {count_w} шт.'
                                bot.send_message(cid, msg)

                        # else:
                    #     print(user_database)

                else:
                    msg = show_hint(*[
                        'Слово должно содержать только английские буквы.',
                        '',
                        'Пожалуйста, повторите попытку нажатием на кнопку',
                        f'{Command.ADD_WORD.lower()}'
                    ])
                    bot.send_message(cid, msg)

            else:
                msg = 'Английское слово уже существует в пользовательской БД'
                bot.send_message(cid, msg)
                # print(user_database)

        else:
            msg = f'Я принимаю только слова.\
                Команда {user_en_word} в расчет не берется.'
            bot.send_message(cid, msg)


    def add_user_ru_word(message):
        cid = message.chat.id
        user_ru_word = message.text.lower()

        # user_database = users_word_dict[cid]

        check_word_bool = check_word_letters(user_ru_word,
                                             eng_bool=False)

        user_words = get_user_words(repository=repository,
                                    user_id=message.from_user.id)
        last_en_word = user_words[-1].get('en_word')

        data_dict = {
            'en_word': last_en_word,
            'en_trans': '',
            'mp_3_url': '',
            'pos_name': 'unidentified',
            'ru_word': user_ru_word,
            'en_example': '',
            'ru_example': ''
        }

        if check_word_bool:

            repository.add_user_word(user_id=message.from_user.id,
                                     data_dict=data_dict)

            new_user_database = get_user_words(repository=repository,
                                               user_id=message.from_user.id)

            words_count = len(new_user_database)
            msg = f'Текущее количество английских слов - {words_count} шт.'
            bot.send_message(cid, msg)

            # get_words(repository=repository,
            #           en_word= user_en_word,
            #           is_added_by_users=True)

            # user_database[-1].update({'pos_name': 'unidentified'})
            # user_database[-1]['ru_word'] = user_ru_word
            # print(user_database)

        else:

            repository.delete_user_word_pair(user_id=message.from_user.id,
                                             en_word=last_en_word)

            repository.delete_word(data_dict=data_dict)

            msg = show_hint(*[
                'В этом случае я принимаю только русские буквы.',
                '',
                'Пожалуйста, повторите попытку нажатием на кнопку',
                f'{Command.ADD_WORD.lower()}'
            ])
            bot.send_message(cid, msg)

            # del user_database[-1]
            #
            # print(user_database)


def reply_handler(bot: TeleBot) -> None:
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def message_reply(message):
        text = message.text
        markup = types.ReplyKeyboardMarkup(row_width=2)

        try:
            with bot.retrieve_data(message.from_user.id,
                                   message.chat.id) as data:

                target_word = data['target_word']

                if text == target_word:
                    hint = show_target(data)
                    hint = show_hint(*["Отлично!❤", hint])

                else:
                    for btn in buttons[:4]:
                        if btn.text == text:
                            if '❌' not in btn.text:
                                btn.text = text + '❌'

                            transl = data['translate_word']
                            hint = show_hint("Допущена ошибка!",
                                             f"Попробуй ещё раз вспомнить слово 🇷🇺{transl}")

                            break

            markup.add(*buttons)
            my_message = bot.send_message(message.chat.id, hint,
                                          reply_markup=markup)

            get_mp3_audio(bot, data, hint, my_message)
            get_example(bot, message, markup, data, hint)

        except (TypeError, KeyError, UnboundLocalError):
            pass


def connect_telebot(repository: object, token_bot: str) -> None:
    print('Подключение к чат-боту Telegram...')
    bot = TeleBot(token_bot, state_storage=StateMemoryStorage())
    # known_users, users_word_dict = [], {}

    start_game_handler(bot, repository)
    delete_word_handler(bot, repository)
    add_word_handler(bot, repository)

    reply_handler(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)
