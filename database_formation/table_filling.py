import csv

import sqlalchemy as sq
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from database_formation.table_structure import create_tables


def get_dsn(db_name:str, user:str, password:str, 
            host:str='localhost', port:str='5432') -> str:
    
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def turn_on_engine(dns_link: str) -> sq.Engine:
    
    return sq.create_engine(dns_link)


def get_en_lvl_list() -> list:
    
    level_code = [
                    'a1', 
                    'a2', 
                    'b1', 
                    'b2', 
                    'c1', 
                    'c2'
                ]
    
    level_name = [
                    'beginner', 
                    'pre-intermediate',
                    'intermediate', 
                    'upper-intermediate', 
                    'advanced', 
                    'proficiency'
                ]
    
    return [
            level_code, 
            level_name
        ]


def get_pos_name_list() -> list:
    
    return [
            'noun', 
            'verb', 
            'adjective'
        ]


def get_dict_data_by_list(key_list:list, 
                        list_of_val_lists: list) -> list:
    
    append_list = []
    
    for i, _ in enumerate(list_of_val_lists[0]):
        
        dict_data = {
                    'id': i+1
                }
        
        dict_update = {
                        k: v[i] for k, v in zip(
                                                key_list,
                                                list_of_val_lists
                                            )
                    }
        
        dict_data.update(dict_update)
        append_list.append(dict_data)
        
    return append_list


def get_dict_data_by_idx(data_list: list, idx_loc: int, key_list: 
                        list, idx_value_list: list) -> list:
    
    element_idx_list = [
                        l[idx_loc] for l in data_list
                    ]
    
    unique_list = sorted(
                        set(element_idx_list)
                    )
    
    append_list = []
    
    for i, val in enumerate(unique_list):
        
        info_list  = [
                        l for l in data_list if l[idx_loc] == val
                ]
        
        if len(info_list) > 0:
            info_list = info_list[0]
            
            dict_data = {
                        'id': i+1
                    }
            
            dict_update = {
                            k: info_list[i] for k, i in zip(
                                                            key_list, 
                                                            idx_value_list
                                                        )
                        }
            
            dict_data.update(dict_update)
            append_list.append(dict_data)
            
    return append_list


def get_db_dict_data(data_list:list) -> list:
    
    pos_name_dict = get_dict_data_by_list(
                                            ['pos_name'], 
                                            [get_pos_name_list()]
                                        )
    
    en_lvl_dict = get_dict_data_by_list(
                                        ['level_code', 'level_name'], 
                                        get_en_lvl_list()
                                    )
    
    en_word_dict = get_dict_data_by_idx(
                                        data_list, 
                                        0, 
                                        ['en_word', 'en_trans', 'mp_3_url'],
                                        [0, 5, 3]
                                    )
    
    ru_word_dict = get_dict_data_by_idx(
                                        data_list, 
                                        4, 
                                        ['ru_word'], 
                                        [4]
                                    )
    
    en_example_dict = get_dict_data_by_idx(
                                            data_list, 
                                            6, 
                                            ['en_example', 'ru_example'], 
                                            [6, 7]
                                        )
    
    en_db_dict = []
    
    for i, word_data in enumerate(data_list):
        
        en_word, pos_name, en_example,\
        level_code, ru_word = (
                                word_data[0], 
                                word_data[1], 
                                word_data[6],
                                word_data[2], 
                                word_data[4]
                            )
        
        val_list = [
                    en_word, 
                    pos_name, 
                    en_example, 
                    level_code, 
                    ru_word
                ]    
        
        key_list = [
                    'en_word', 
                    'pos_name', 
                    'en_example',
                    'level_code', 
                    'ru_word'
                ]
        
        
        dict_list = [
                        en_word_dict, 
                        pos_name_dict,
                        en_example_dict, 
                        en_lvl_dict, 
                        ru_word_dict
                    ]
        
        id_en_word, id_pos, id_example,\
        id_level, id_ru_word = (
                                [d for d in dict if d[k] == v][0]['id']
                                for dict, k, v in zip(
                                                        dict_list,
                                                        key_list, 
                                                        val_list
                                                    )
                            )
        
        append_dict = {
                        'id': i+1, 
                        'id_en_word': id_en_word,
                        'id_pos': id_pos, 
                        'id_example': id_example,
                        'id_level':id_level, 
                        'id_ru_word': id_ru_word
                    }
        
        en_db_dict.append(append_dict)
    
    en_example_dict[0].\
        update({
                'id': 1, 
                'en_example': 'No example', 
                'ru_example': 'Пример отсутствует'
            })
    
    return [
            en_word_dict, 
            en_example_dict, 
            ru_word_dict, 
            en_lvl_dict, 
            pos_name_dict, 
            en_db_dict
        ]


def fill_tables(db_name:str, user:str, password:str, 
                class_list:list, dict_list:list) -> bool:
    
    dns = get_dsn(db_name = db_name, user = user, password = password)
    engine = turn_on_engine(dns)
    
    create_tables(engine)
    
    session_class = sessionmaker(bind=engine)
    session = session_class()
    
    try:
        for my_class, my_dict_list in zip(class_list, dict_list):
                print(f'Обрабатываю класс {my_class}')
                
                for my_dict in my_dict_list:
                    print(f'{my_dict}')
                    
                    model = my_class(**my_dict)
                    session.add(model)
                    session.commit()
        
    except exc.IntegrityError:
        print("IntegrityError: данные по значениям уже существуют")
        return False
    
    session.close()
    return True