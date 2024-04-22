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
from telebot_connection.telebot_functional.known_users import check_known_users
from telebot_connection.telebot_functional.letters import check_word_letters
from telebot_connection.telebot_functional.add_word import add_en_word
from telebot_connection.telebot_functional.add_word import count_words


def start_game_handler(bot:TeleBot, known_users:list, 
                        users_word_dict:dict, database:list) -> None:
    
    @bot.message_handler(commands=['cards', 'start'])
    def create_cards(message):
        cid = message.from_user.id
        check_known_users(bot, cid, known_users, 
                            users_word_dict, database)
    
        user_database = users_word_dict[cid]
        pos_database = get_random_pos_database(user_database)
        
        target_word, translate, others, transcription,\
            en_example, ru_example = get_random_words(pos_database)
        
        global buttons
        buttons, markup = setup_buttons(target_word, others)
        
        bot.send_message(message.chat.id,
                        f"Выбери перевод слова:\n🇷🇺 {translate}",
                        reply_markup = markup)
        
        bot.set_state(message.from_user.id, 
                    States.target_word, 
                    message.chat.id)
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['target_word'] = target_word
            data['translate_word'] = translate
            data['other_words'] = others
            data['transcription'] = transcription
            data['en_example'] = en_example
            data['ru_example'] = ru_example
    
    @bot.message_handler(func=lambda message: message.text==Command.NEXT)
    def next_cards(message):
        create_cards(message)


def delete_word_handler(bot:TeleBot, known_users:list, 
                        users_word_dict:dict, database:list) -> None:
    
    @bot.message_handler(func=lambda message: message.text==Command.DELETE_WORD)
    def delete_word(message):
        cid = message.chat.id
        check_known_users(bot, cid, known_users, users_word_dict, database)
        
        msg = "Введите английское слово для удаления из базы данных:"
        send_msg = bot.send_message(cid, msg)
        bot.register_next_step_handler(send_msg, delete_user_en_word)
    
    def delete_user_en_word(message):
        cid = message.chat.id
        user_database = users_word_dict[cid]
        user_en_word = message.text.lower()
        
        if user_en_word not in get_button_states():
            new_user_database = [
                                user_dict for user_dict in user_database 
                                if user_dict.get('en_word') != user_en_word
                            ]

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
            
            empty_bool = False
            if correct_letters and len(new_user_database) == len(user_database):
                msg = 'Введенное слово отсутсвует в базе данных пользователя'
                bot.send_message(cid, msg)
                empty_bool = True
            
            if not empty_bool and correct_letters:
                for i in range(len(new_user_database)):
                    user_dict = new_user_database[i]
                    user_dict['id'] = i + 1
                
                users_word_dict[cid] = new_user_database
                print(new_user_database)
                
                count_w = count_words(new_user_database)
                msg = f'Текущее количество английских слов - {count_w} шт.'
                bot.send_message(cid, msg)
        
        else:
            cmd_name = user_en_word
            msg = f'Я принимаю только слова.\
                Команда {cmd_name} в расчет не берется.'
            bot.send_message(cid, msg)


def add_word_handler(bot:TeleBot, known_users:list, 
                    users_word_dict:dict, database:list) -> None:
    
    @bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
    def add_word(message):
        cid = message.chat.id
        check_known_users(bot, cid, known_users, users_word_dict, database)

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
                    user_database = users_word_dict[cid]
                    new_user_database = add_en_word(bot, cid, 
                                                    user_database, 
                                                    user_en_word)
                    users_word_dict[cid] = new_user_database
                    
                    if users_word_dict[cid][-1]['ru_word'] is None:
                        msg =  "Введите перевод английского слова:"
                        send_msg = bot.send_message(cid, msg)
                        bot.register_next_step_handler(send_msg, 
                                                    add_user_ru_word)
                    
                    else:
                        print(user_database)

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
                print(user_database)           
            
        else:
            msg = f'Я принимаю только слова.\
                Команда {user_en_word} в расчет не берется.'
            bot.send_message(cid, msg)

    def add_user_ru_word(message):
        cid = message.chat.id
        user_ru_word = message.text.lower()
        user_database = users_word_dict[cid]
        
        check_word_bool = check_word_letters(user_ru_word, 
                                            eng_bool=False)
        
        if check_word_bool:
            user_database[-1].update({'pos_name': 'unidentified'})
            user_database[-1]['ru_word'] = user_ru_word
            print(user_database)
        
        else:
            msg = show_hint(*[
                            'В этом случае я принимаю только русские буквы.',
                            '',
                            'Пожалуйста, повторите попытку нажатием на кнопку',
                            f'{Command.ADD_WORD.lower()}'
                        ])
            
            del user_database[-1]
            
            print(user_database)
            bot.send_message(cid, msg)

        words_count = count_words(user_database)
        msg = f'Текущее количество английских слов - {words_count} шт.'
        bot.send_message(cid, msg)


def reply_handler(bot:TeleBot) -> None:
    
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


def connect_telebot(database:list, token_bot:str) -> None:

    print('Подключение к чат-боту Telegram...')
    bot = TeleBot(token_bot, state_storage = StateMemoryStorage())
    known_users, users_word_dict = [], {}
    
    start_game_handler(bot, known_users, users_word_dict, database)    
    delete_word_handler(bot, known_users, users_word_dict, database)
    add_word_handler(bot, known_users, users_word_dict, database)
    
    reply_handler(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)