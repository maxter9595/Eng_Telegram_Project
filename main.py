from data import form_english_data
from database import create_and_fill_db
from data_formation.english_html import write_dir
from database_formation.db_get_table import get_db_table
from telebot_connection.telebot_connection import connect_telebot


def main_function(db_name:str, user:str, password:str, 
                    token:str, form_data:bool=False) -> None:
    
    # Задействование функционала папки data_formation и файла data.py
    if form_data:
        form_english_data(os = 'win', browser = 'chrome')
    
    # Построение пути к файлу database.csv
    csv_path = write_dir('data', 'database_csv', 'database.csv')
    
    # Задействование функционала папки database_formation и файла database.py
    create_and_fill_db(db_name = db_name, user = user, 
                        password = password, csv_path = csv_path)
    
    print(f'# ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ БД {db_name}:')
    
    database = get_db_table(db_name=db_name, user=user, 
                                password=password)
    
    print(f'Статус: данные извлечены из БД {db_name}')
    
    # Задействование функционала папки telebot_connection
    print('# ПОДКЛЮЧЕНИЕ К ЧАТ-БОТУ:')
    connect_telebot(database, token)


if __name__ == '__main__':
    
    DB_NAME = 'english_bot_db'
    USER = 'postgres'
    PASSWORD = 'postgres'
    TOKEN =  '7076512254:AAHwldFRsqwr3rAdEiCEOmSF-zoFFIjFtO4'
    
    main_function(DB_NAME, USER, PASSWORD, TOKEN)