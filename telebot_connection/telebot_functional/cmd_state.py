from telebot.handler_backends import State, StatesGroup


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'


class States(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


def get_button_states() -> tuple:
    
    add_word_btn_name = Command.ADD_WORD.lower()
    delete_word_btn_name = Command.DELETE_WORD.lower()
    next_word_btn_name = Command.NEXT.lower()
    
    return (
            add_word_btn_name, 
            delete_word_btn_name,
            next_word_btn_name
        )