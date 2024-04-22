import re
from string import ascii_letters


def check_word_letters(word:str, eng_bool:bool=True) -> bool:

    if eng_bool:
        letter_condition = lambda l: l in ascii_letters
        
    else:
        letter_condition = lambda l: re.match('[а-яА-Я]', l)\
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