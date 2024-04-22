import os
import sys
import random

from telebot import types

sys.path.insert(1, os.path.join(os.path.abspath(os.getcwd())))
from telebot_connection.telebot_functional.cmd_state import Command


def setup_buttons(target_word:str, others:list) -> tuple:
    
    buttons = []
    
    target_word_btn = types.KeyboardButton(target_word)
    
    other_words_btns = [
                        types.KeyboardButton(word) 
                        for word in others
                    ]
    
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
    
    return (
            buttons, 
            markup
        )