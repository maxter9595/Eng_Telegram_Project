# from data import form_english_data
# from database import create_and_fill_db
# from data_formation.english_html import write_dir
# from database_formation.db_get_table import get_db_table
from database_formation.table_filling import Repository
from telebot_connection.telebot_connection import connect_telebot
from database_formation.db_creation import Database


def main_function(db_name: str, user: str, password: str,
                  token: str) -> None:
    # Задействование функционала папки data_formation и файла data.py
    # if form_data:
    #     form_english_data(os = 'win', browser = 'chrome')

    # Построение пути к файлу database.csv
    # csv_path = write_dir('data', 'database_csv', 'database.csv')


    print('ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ...')

    database = Database(
        dbname=db_name,
        user=user,
        password=password
    )

    if not database.exists_db():
        database.create_db()
        database.create_tables()
        database.prepare_words()

    # Задействование функционала папки database_formation и файла database.py
    # create_and_fill_db(db_name=db_name, user=user, password=password)

    # print(f'# ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ БД {db_name}:')

    # database = get_db_table(db_name=db_name, user=user,
    #                         password=password)

    # print(f'Статус: данные извлечены из БД {db_name}')

    # Задействование функционала папки telebot_connection
    print('# ПОДКЛЮЧЕНИЕ К ЧАТ-БОТУ...')

    repository = Repository(dbname=db_name, user=user, password=password)
    connect_telebot(repository, token)


if __name__ == '__main__':
    DB_NAME = 'test_TGbot'
    USER = 'postgres'
    PASSWORD = 'postgres'
    TOKEN = ''
    main_function(DB_NAME, USER, PASSWORD, TOKEN)
