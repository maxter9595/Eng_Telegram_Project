
from telebot import TeleBot
from telebot_connection.telebot_functional.text import hello_text


def check_known_users(bot:TeleBot, cid:int, known_users:list,
                    users_word_dict:dict, database:list) -> None:

    if cid not in known_users:
        
        known_users.append(cid)
        users_word_dict[cid] = database
        
        bot.send_message(cid, hello_text())