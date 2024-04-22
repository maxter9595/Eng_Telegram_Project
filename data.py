import csv

from data_formation.english_html import write_oxford_data, write_dir
from data_formation.translation_html import write_promt_translation
from data_formation.english_mp3 import get_mp3_files


def get_pos_data(oxford_data_list:list, 
                    oxford_pos_list:list) -> tuple:
    
    pos_data_list, pos_word_list, pos_list = [], [], []
    verb_tuple = (
                'verb', 'linking verb', 
                'modal verb', 'auxiliary verb'
            )
    
    for loop_list in oxford_data_list:
        if loop_list[1] in oxford_pos_list:
            
            if loop_list[1] in verb_tuple:
                loop_list[1] = 'verb'

            if loop_list not in pos_data_list:
                pos_data_list.append(loop_list)
                pos_word_list.append(loop_list[0])
                pos_list.append(loop_list[1])
    
    return (pos_data_list, pos_word_list, pos_list)


def get_processed_data(word_trans_data:list, pos_data_list:list,
                        pos_word_list:list) -> list:
    
    processed_data_list = []
    for word in pos_word_list:
        
        data_list1 = [
                        my_list for my_list in pos_data_list 
                        if my_list[0] == word
                    ]
        
        data_list2 = [
                        my_list for my_list in word_trans_data 
                        if my_list[1] == word 
                        and my_list[-1] != ''
                        and my_list[-2] != ''
                    ]
        
        if data_list2:
            processed_data_list.\
                append(
                        data_list1[0] +\
                        [data_list2[0][0]] +\
                        data_list2[0][2:]
                    )
    
    processed_data_list = [
                            list(x) for x in
                            set(
                                tuple(x) for x 
                                in processed_data_list
                                )
                            ]

    return processed_data_list


def write_processed_data(processed_data_list:list) -> None:
    
    csv_db_path = write_dir(
                            'data', 
                            'database_csv', 
                            'database.csv'
                        )
    
    col_names = [
                    'en_word', 'pos', 
                    'level', 'mp3_url', 
                    'ru_word', 'transcription',
                    'en_example', 'ru_example'
                ]
    
    with open(csv_db_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        writer.writerows(processed_data_list)


def download_mp3(processed_data_list:list, 
                    os:str, browser:str) -> None:
    
    word_list, url_mp3_list, trascript_list = [], [], []
    
    for l in processed_data_list[1:]:
        
        en_word, url_mp3, trascription = (l[0], l[3], l[5])
        word_list.append(en_word)
        url_mp3_list.append(url_mp3)
        trascript_list.append(trascription)
        
    get_mp3_files(
                    word_list, url_mp3_list, 
                    trascript_list, os, browser
                )


def form_english_data(os:str='win', browser:str='chrome') -> None:
    
    print('# ПОЛУЧЕНИЕ АНГЛИЙСКИХ СЛОВ (OXFORD):')
    oxford_data_list = write_oxford_data(os, browser)
    
    oxford_pos_list = [
                        'noun', 'verb', 'linking verb', 
                        'modal verb', 'auxiliary verb', 'adjective'
                        ]
    
    pos_data_list, pos_word_list,\
        pos_list = get_pos_data(
                                oxford_data_list, 
                                oxford_pos_list
                                )
    
    print('# ПЕРЕВОД СЛОВ И ПОДБОР ПРИМЕРОВ ПРЕДЛОЖЕНИЙ (PROMT):')
    word_trans_data = write_promt_translation(
                                                pos_word_list, 
                                                pos_list, 
                                                os, browser
                                            )
    
    print('# ПОЛУЧЕНИЕ ОБРАБОТАННЫХ ДАННЫХ (OXFORD+PROMT):')
    processed_data_list = get_processed_data(
                                                word_trans_data, 
                                                pos_data_list, 
                                                pos_word_list
                                            )
    
    write_processed_data(processed_data_list)
    print('Статус: данные успешно записаны')
    
    print('# ВЫВОД MP3 ФАЙЛОВ ПО URL-ССЫЛКАМ:')
    download_mp3(processed_data_list, os, browser)
    print('Статус: MP3 файлы успешно записаны')