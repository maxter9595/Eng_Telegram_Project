import random


def get_random_pos_database(user_database:list, 
                            pos_list:list = ['noun', 
                                            'verb', 
                                            'adjective']) -> list:

    pos = random.choice(pos_list)
    
    pos_database = [
                    word_dict for word_dict in user_database
                    if word_dict.get('pos_name') == pos
                ]
    
    return pos_database


def get_random_words(pos_database:list) -> tuple:
    
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
    
    transcription, en_example,\
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
    
    return (
            target_word, 
            translate, 
            random_others, 
            transcription, 
            en_example, 
            ru_example
        )