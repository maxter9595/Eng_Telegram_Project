import csv

from database_formation.db_creation import create_database
from database_formation.table_structure import EngWord, EngPos
from database_formation.table_structure import EngLevel, EngExample
from database_formation.table_structure import RuWord, EngDbTable
from database_formation.table_filling import get_db_dict_data, fill_tables


def read_database(path:str) -> list:
    
    with open(path, "r") as f:
        reader = csv.reader(f)
        data_list = list(reader)[1:]
        
    return data_list


def create_and_fill_db(db_name:str, user:str, 
                        password:str, csv_path:str) -> None:
    
    print('# СОЗДАНИЕ БАЗЫ ДАННЫХ:')
    create_database(db_name=db_name, user=user, password=password)
    
    print('# ЧТЕНИЕ ДАННЫХ:')
    data_list = read_database(csv_path)
    
    print('Статус: файл с данными прочитан', 
        '# ПОДГОТОВКА ДАННЫХ:', sep = "\n")

    dict_list = get_db_dict_data(data_list)
    
    print('Статус: данные подготовлены', 
        f'# ЗАГРУЗКА ДАННЫХ В ТАБЛИЦЫ БД {db_name}:',
        sep = "\n")
    
    class_list = [
                    EngWord, 
                    EngExample, 
                    RuWord, 
                    EngLevel,
                    EngPos, 
                    EngDbTable
                ]

    fill_table_bool = fill_tables(db_name=db_name, user=user, password=password,
                                    class_list=class_list, dict_list=dict_list)
    
    if fill_table_bool:
        print(f'Статус: данные загружены в таблицы БД {db_name}')