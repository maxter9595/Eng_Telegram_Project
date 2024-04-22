import telebot
from telebot import TeleBot
from telebot_connection.telebot_functional.text import show_hint


def get_example(bot:TeleBot, 
                message:telebot.types.Message, 
                markup:telebot.types.ReplyKeyboardMarkup,
                data:dict, hint:str) -> None:
    
    if 'Допущена ошибка!' not in hint:
        
        if data['en_example'] != 'No example' and\
            data['ru_example'] != "Пример отсутствует":
            
            en_example = data["en_example"]
            ru_example = data["ru_example"]
            
            example_text = show_hint('*Пример предложения:*',
                                    f'"{en_example}"', 
                                    f'"{ru_example}"')
            
            bot.send_message(message.chat.id, 
                            example_text, 
                            reply_markup = markup, 
                            parse_mode = 'Markdown')