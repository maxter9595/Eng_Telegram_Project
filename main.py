from database.creation import DBCreation
from database.repository import DBRepository
from tgbot.connection import connect_telebot


def main_function(dbname: str, user: str,
                  password: str, token: str) -> None:

    """
    Проверяет наличие БД и налаживает соединение с чат-ботом Telegram.

    Вводные параметры:
    - dbname: название базы данных
    - user: логин пользователя Postgres
    - password: пароль пользователя Postgres
    - token: токен для подключения к чат-боту Telegram
    """

    print('ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ...')

    database = DBCreation(
        dbname=dbname,
        user=user,
        password=password
    )

    if not database.exists_db():
        database.create_db()
        database.create_tables()
        database.prepare_words()

    repository = DBRepository(
        dbname=dbname,
        user=user,
        password=password
    )

    print('ПОДКЛЮЧЕНИЕ К ЧАТ-БОТУ...')

    connect_telebot(
        repository=repository,
        token=token
    )


if __name__ == '__main__':

    DB_NAME = 'EngStudyBot1'
    USER = 'postgres'
    PASSWORD = 'postgres'
    TOKEN = '7076512254:AAHwldFRsqwr3rAdEiCEOmSF-zoFFIjFtO4'

    main_function(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        token=TOKEN
    )
