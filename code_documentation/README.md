# Документация к коду проектной работы «Обучалка английскому языку (чат-бот Telegram)»

-----------------------------

## Структура документации кода

- **1. Формирование данных по английским словам** (папка data_formation + файл data.py)
- **2. Создение БД в PostgreSQL с использованием Python** (папка database_formation + файл database.py)
- **3. Настройка чат-бота Telegram** (папка telebot_connection + файл main.py)

-----------------------------

## 1. Формирование данных по английским словам (папка data_formation + файл data.py)

#### get_oxford_data (функция)

Позволяет выгрузить английские слова, входящие в сборник [Oxford 5000](https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000 "Сборник слов Oxford 5000").

**Местоположение:** файл `english_html.py`.

- **Вводные параметры:**
    - `soup`: объект класса BeautifulSoup, необходимый для парсинга веб-сайта.
    - `base_url`: URL-адрес страницы. В данном случае это ссылка на [онлайн-словарь Оксфордского университета](https://www.oxfordlearnersdictionaries.com/ "Онлайн-словарь Оксфордского университета").

- **Выводной параметр:**
    - `word_list`: список, содержащий информацию о загруженных словах, включенных в сборник Oxford 5000 (слово, часть речи, уровень владения английским языком, ссылка на MP3 файл произношения слова).

```python
from bs4 import BeautifulSoup

def get_oxford_data(soup:BeautifulSoup, base_url:str) -> list:
    ...
    return word_list
```

-----------------------------

#### write_dir (функция)

Выводит путь к файлу, состоящий из заданных нами аргументов.

**Местоположение:** файл `english_html.py`.

- **Вводные параметры:**
  - `*args`: аргументы, используемые для формирования директории.

- **Выводной параметр:**
    - `root_dir`: путь к файлу.

```python
import os

def write_dir(*args) -> os.path
    ...
    return root_dir
```

-----------------------------

#### get_headers (функция)

Создает фейковые заголовки, необходимые для работы с функционалом библиотеки `requests`.

**Местоположение:** файл `english_html.py`.

- **Вводные параметры:**
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
    - Словарь-заголовок, необходимый для работы с функциями библиотеки `requests`.

```python
from fake_headers import Headers

def get_headers(os:str, browser:str)->dict:
    return Headers(os=os, browser=browser).generate()
```

-----------------------------

#### write_oxford_data (функция)

Записывает данные по английским словам на локальный файл проекта.

**Местоположение:** файл `english_html.py`.

- **Вводные параметры:**
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
    - `data`: лист с данными, полученными в результате отработки функции `get_oxford_data`.

```python
def write_oxford_data(os:str, browser:str) -> list:
    ...
    return data
```

- **Результат работы функции:** запись английских слов в файл `oxford5000_dictionary.csv` (папка data).

-----------------------------

#### launch_get_requests (функция)

Запускает GET-запрос для парсинга [онлайн-словаря PROMT.One](https://www.online-translator.com/translation/english-russian/, 'Онлайн-словарь PROMT.One').

**Местоположение:** файл `translation_html.py`.

- **Вводные параметры:**
  - `attempts`: количество попыток парсинга сайта в условиях наличия возможной ошибки `requests.exceptions.ConnectTimeout`.
  - `error_timeout`: количество секунд остановки функции, после которых последует реализация следующей попытки осуществления GET-запроса.
  - `promt_link`: ссылка на онлайн-словарь PROMT.One.
  - `my_word`: слово, которое необходимо перевести.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводные параметры:**
  - В случае успешного осуществления запроса выводится объект класса `BeautifulSoup` (`soup`).
  - В случае неудачного запроса выводится `None`.

```python
from typing import Optional
from bs4 import BeautifulSoup

def launch_get_requests(attempts:int, error_timeout:int, promt_link:str, my_word:str, os:str, browser:str) -> Optional[BeautifulSoup]
    ...
    return soup
```

-----------------------------

#### promt_site_parsing (функция)

Позволяет вытащить все необходимые данные из HTML-кода [онлайн-словаря PROMT.One](https://www.online-translator.com/translation/english-russian/, 'Онлайн-словарь PROMT.One').

**Местоположение:** файл `translation_html.py`.

- **Вводные параметры:**
  - `soup`: объект класса BeautifulSoup, необходимый для парсинга веб-сайта.
  - `my_word`: слово, которое необходимо перевести.

- **Выводной параметр:**
    - `{my_word: dict_pos}:` словарь, состоящий из английского слова `my_word` и информационного словаря `dict_pos`.
      - `dict_pos` - словарь, содержащий перевод в рамках отдельных частей речи (перевод, транскрипция, примеры на английском и русском языках).

```python
from bs4 import BeautifulSoup

def promt_site_parsing(soup:BeautifulSoup, my_word:str) -> dict:
    ...
    return {my_word: dict_pos}
```

-----------------------------

#### get_translation (функция)

Выводит перевод английских слов из [онлайн-словаря PROMT.One](https://www.online-translator.com/translation/english-russian/, 'Онлайн-словарь PROMT.One').

**Местоположение:** файл `translation_html.py`.

- **Вводные параметры:**
  - `my_word`: слово, которое необходимо перевести.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
  - в случае удачного GET-запроса выводится словарь `{my_word: dict_pos}`, полученный в рамках функции `promt_site_parsing`.
  - в случае неудачного GET-запроса выводится `None`.

```python
from typing import Optional

def get_translation(my_word:str, os:str, browser:str) -> Optional[dict]:
    ...
    return {my_word: dict_pos}
```

-----------------------------

#### write_promt_translation (функция)

Записывает переведенные английские слова в отдельный csv-файл.

**Местоположение:** файл `translation_html.py`.

- **Вводные параметры:**
  - `word_list`: список английских слов, требующих перевода.
  - `pos_list`: список частей речи, учитываемых в разрезе [онлайн-словаря PROMT.One](https://www.online-translator.com/translation/english-russian/, 'Онлайн-словарь PROMT.One').
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
    - `word_trans_data:` список, содержащий перевод слова и прочую информацию о нем (транскрипция, примеры предложений).

```python
write_promt_translation(word_list:list, pos_list:str, os:str, browser:str) -> list:
    ...
    return word_trans_data
```

- **Результат работы функции:** запись переведенных английских слов в файл `promt_translation.csv` (папка data).

-----------------------------

#### write_mp3 (функция)

Проводит запись MP3 файла по URL-ссылке, полученной в результате реализации функции `get_oxford_data`.

**Местоположение:** файл `english_mp3.py`.

- **Вводные параметры:**
  - `url`: URL-ссылка на MP3-файл, полученная из [веб-сайта Оксфордского университета](https://www.oxfordlearnersdictionaries.com/ "Онлайн-словарь Оксфордского университета").
  - `file_path`: директория, относительно которой необходимо записать MP3 файл на ПК.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.
  - `attempts`: количество попыток парсинга сайта в условиях наличия возможной ошибки `requests.exceptions.ConnectTimeout`.
  - `error_timeout`: количество секунд остановки функции, после которых последует реализация следующей попытки осуществления GET-запроса.

- **Выводной параметр:**
    - `True/False:` булевы значения, отражающие успешную/безуспешную запись MP3 файла на ПК (папка data).
      - `True:` успешная запись файла.
      - `False:` неудачная запись файла.


```python
def write_mp3(url:str, file_path:str, os:str, browser:str, attempts:int, error_timeout:int) -> bool:
    
    try:
        ...
        return True

    except requests.exceptions.ConnectionError:
        ...
        return False
```

-----------------------------

#### get_mp3_files (функция)

Позволяет на основе списка слов и URL-ссылок массово записать MP3 файлы на ПК.

**Местоположение:** файл `english_mp3.py`.

- **Вводные параметры:**
  - `word_list`: список английских слов.
  - `url_list`: список URL-ссылок на MP3-файлы.
  - `transcript_list`: список транскрипций английских слов.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

```python
def get_mp3_files(word_list:list, url_list:list, transcript_list:list, os:str, browser:str) -> None:
    ...
```

- **Результат работы функции:** запись MP3-файлов произношений английских слов в папку `eng_audio_files_mp3` (папка data).

-----------------------------

#### get_pos_data (функция)

Фильтрует английские слова по частям речи (существительные, глаголы, прилагательные).

**Местоположение:** файл `data.py`.

- **Вводные параметры:**
  - `oxford_data_list:` список с данными по английским словам, полученный из функции `write_oxford_data`.
  - `oxford_pos_list:` список частей речи, по которым фильтруются слова.

- **Выводной параметр:**
  - `(pos_data_list, pos_word_list, pos_list):` кортеж с данными, полученными после фильтрации слов.
    - `pos_data_list:` список с информацией относительно английских слов (слово, часть речи, уровень владения английским языком, ссылка на MP3 файл произношения слова).
    - `pos_word_list:` список английских слов.
    - `pos_list:` список частей речи.

```python
def get_pos_data(oxford_data_list:list, oxford_pos_list:list) -> tuple:
    ...
    return (pos_data_list, pos_word_list, pos_list)
```

-----------------------------

#### get_processed_data (функция)

Объединяет данные по английским словам из [онлайн-словаря Oxford](https://www.oxfordlearnersdictionaries.com/ "Сборник слов Oxford 5000") и сведения, полученные из [онлайн-словаря PROMT.One](https://www.online-translator.com/translation/english-russian/, 'Онлайн-словарь PROMT.One').

**Местоположение:** файл `data.py`.

- **Вводные параметры:**
  - `word_trans_data:` список, содержащий перевод слова и прочую информацию о нем (транскрипция, примеры предложений).
  - `pos_data_list:` список с информацией относительно английских слов (слово, часть речи, уровень владения английским языком, ссылка на MP3 файл произношения слова).
  - `pos_word_list:` список английских слов.

- **Выводной параметр:**
  - `processed_data_list:` список с обработанными данными (английское слово, часть речи, уровень владения английским языком, ссылка на MP3-файл, перевод слова, транскрипция, примеры использования слова на английском и русском языках).

```python
def get_processed_data(word_trans_data:list, pos_data_list:list, pos_word_list:list) -> list:
    ...
    return processed_data_list
```

-----------------------------

#### write_processed_data (функция)

Запись обработанных данных, выведенных из функции `get_processed_data`, на ПК.

**Местоположение:** файл `data.py`.

- **Вводной параметр:**
  - `processed_data_list:` список с обработанными данными (английское слово, часть речи, уровень владения английским языком, ссылка на MP3-файл, перевод слова, транскрипция, примеры использования слова на английском и русском языках).

```python
def write_processed_data(processed_data_list:list) -> None:
    ...
```

- **Результат работы функции:** запись обработанных данных по английским словам в файл `database.csv` (папка data).

-----------------------------

#### download_mp3 (функция)

Записывает MP3 файлы на основе URL-ссылок, содержащихся в списке с обработанными данными (`processed_data_list`).

**Местоположение:** файл `data.py`.

- **Вводные параметры:**
  - `processed_data_list:` список с обработанными данными (английское слово, часть речи, уровень владения английским языком, ссылка на MP3-файл, перевод слова, транскрипция, примеры использования слова на английском и русском языках).
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

```python
def download_mp3(processed_data_list:list, os:str, browser:str) -> None:
    ...
```

- **Результат работы функции:** запись MP3-файлов произношений английских слов в папку `eng_audio_files_mp3` (папка data).

-----------------------------

#### process_english_data (функция)

Выполняет все функции, представленные в разделе №1 текущей документации.

**Местоположение:** файл `data.py`.

- **Вводные параметры:**
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

```python
def process_english_data(os:str='win', browser:str='chrome') -> None:
    ...
```

- **Результат работы функции:** запись переведенных английских слов в папку data.

-----------------------------

## 2. Создение БД в PostgreSQL с использованием Python (папка database_formation + файл database.py)

#### create_database (функция)

Создает базу данных относительно пользователя Postgres с использованием движка `psycopg2`.

**Местоположение:** файл `db_creation.py`.

- **Вводные параметры:**
  - `db_name`: название базы данных.
  - `user`: имя пользователя Postgres.
  - `password`: пароль пользователя Postgres.
  - `host`: хост, относительно которого проводится создание базы данных.

```python
def create_database(db_name:str, user:str, password:str, host:str='localhost') -> None:
    ...
```

- **Результат работы функции:** создание базы данных Postgres под именем `db_name`.

-----------------------------

#### create_tables (функция)

Создает таблицы, сформированные в разрезе ORM `sqlalchemy`.

**Местоположение:** файл `table_structure.py`.

- **Вводной параметр:**
  - `engine`: движок, формируемый в результате отработки функции `sqlalchemy.create_engine`.

```python
def create_tables(engine: sq.Engine) -> None: 
    Base.metadata.create_all(engine)
```

- **Результат работы функции:** формирование таблиц с заданной структурой.

-----------------------------

#### get_dsn (функция)

Формирует DNS-ссылку, необходимую для запуска движка ORM `sqlalchemy`.

**Местоположение:** файл `table_filling.py`.

- **Вводные параметры:**
  - `db_name`: название базы данных.
  - `user`: имя пользователя Postgres.
  - `password`: пароль пользователя Postgres.
  - `host`: хост, относительно которого проводится создание базы данных.
  - `port`: порт.

- **Выводной параметр:**
  - DNS-ссылка.

```python
def get_dsn(db_name:str, user:str, password:str, host:str='localhost', port:str='5432') -> str:

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
```
-----------------------------

#### turn_on_engine (функция)

Формирует движок ORM `sqlalchemy`, необходимый для инициации сессий.

**Местоположение:** файл `table_filling.py`.

- **Вводной параметр:**
  - `dns_link`: DNS-ссылка, полученная в разрезе функции `get_dsn`.

- **Выводной параметр:**
  - `dns_link`: движок ORM `sqlalchemy`.

```python
def turn_on_engine(dns_link: str) -> sq.Engine:
    
    return sq.create_engine(dns_link)
```

-----------------------------

#### get_en_lvl_list (функция)

Выводит список, содержащий всевозможные уровни владения английским языком.

**Местоположение:** файл `table_filling.py`.

- **Выводной параметр:**
  - `[level_code, level_name]`: список, включающий в себя списки `level_code` и `level_name`.
    - `level_code`: список с уникальными кодами уровней знания английского языка.
    - `level_name`: список с уникальными названиями уровней знания английского языка.

```python
def get_en_lvl_list() -> list:
    ...
    return [level_code, level_name]
```

-----------------------------

#### get_pos_name_list (функция)

Выводит список, содержащий название следующих частей речи: существительное, глагол, прилагательное (noun, verb, adjective).

**Местоположение:** файл `table_filling.py`.

- **Выводной параметр:**
  - список частей речи, планируемых для заполнения в БД.

```python
def get_pos_name_list() -> list:

    return ['noun', 'verb', 'adjective']
```

-----------------------------

#### get_dict_data_by_list (функция)

Формирует список словарей, каждый из которых содержит id и остальные ключи, задаваемые в рамках параметра `key_list`.

Функция используется для формирования данных, которые в дальнейшем будут заполнены в таблицах `en_pos_table` (части речи) и `en_level_table` (уровни владения английским языком).

**Местоположение:** файл `table_filling.py`.

- **Вводные параметры:**
  - `key_list`: список ключей, которые необходимо разместить вместе с id.
  - `list_of_val_lists`: список списков. Каждый список, содержащийся внутри, используется для формирования значений конкретного ключа из `key_list` (см. пример ниже).

- **Выводной параметр:**
  - `append_list`: список словарей, каждый из которых содержит id и остальные ключи, заданные параметром `key_list`.

```python
def get_dict_data_by_list(key_list:list, val_list_of_lists: list) -> list:
    ...
    return append_list
```

- **Пример:**
  - *Вводные параметры:*
    - `key_list` = `['level_code', 'level_name']`
    - `list_of_val_lists` = `[['a1', 'a2', 'b1'], ['beginner', 'pre-intermediate', 'intermediate']]`
  - *Выводной параметр:*
    - `append_list` = `[{'id': 1, 'level_code': 'a1', 'level_name': 'beginner'}, {'id': 2, 'level_code': 'a2', 'level_name': 'pre-intermediate'}, {'id': 3, 'level_code': 'b1', 'level_name': 'intermediate'}]`

-----------------------------

#### get_dict_data_by_idx (функция)

Формирует список словарей, каждый из которых содержит id и остальные ключи, задаваемые в рамках индексирования данных списка, содержащего сведения csv-файла `database.csv`.

**Местоположение:** файл `table_filling.py`.

- **Вводные параметры:**
  - `data_list`: список списков с данными, полученный в результате чтения csv-файла `database.csv`. Пусть каждый список, содержащийся в `data_list` будет называться `info_list`.
  - `idx_loc`: индекс значения списка `info_list`, который необходимо вывести в списке словарей `append_list` в уникальном формате (т.е. без повторов при чтении списка списков `data_list`).
  - `key_list`: список ключей, которые необходимо разместить вместе с id внутри словаря, содержащегося в списке `append_list`.
  - `idx_value_list`: индексы списка `info_list`, на основе которых берутся значения ключей, принадлежащих к `key_list`.

- **Выводной параметр:**
  - `append_list`: список словарей, какждый из которых содержит id и остальные ключи, заданные параметром `key_list`.

```python
def get_dict_data_by_idx(data_list:list, idx_loc:int, key_list:list, idx_value_list:list) -> list:
    ...
    return append_list
```

- **Пример:**
  - *Вводные параметры:*
    - `data_list` = `[['chart', 'noun', 'a1', 'https://www.site.mp3', 'график', '[tʃɑ:t]', 'Periodicity — choose the chart timeframe.', 'Период — выбрать период графика.']]`
    - `idx_loc` = `0`
    - `key_list` = `['en_word', 'en_trans', 'mp_3_url']`
    - `idx_value_list` = `[0, 5, 3]`
  - *Выводной параметр:*
    - `append_list` = `[[{'id': 1, 'en_word': 'chart', 'en_trans': '[tʃɑ:t]', 'mp_3_url': https://www.site.mp3'}]]`

-----------------------------

#### get_db_dict_data (функция)

Формирует обобщенный список списков словарей, данные которых будут отправлены в БД пользователя PostgreSQL.

**Местоположение:** файл `table_filling.py`.

- **Вводной параметр:**
  - `data_list`: список списков с данными, полученный в результате чтения csv-файла `database.csv`.

- **Выводной параметр:**
  - `[en_db_dict, en_word_dict, en_example_dict, ru_word_dict, en_lvl_dict, pos_name_dict]`: список, содержащий списки словарей с данными.
    - `en_db_dict`: список словарей, содержащий данные таблицы `en_db_table`.
    - `en_word_dict`: список словарей, содержащий данные таблицы `en_word_table`.
    - `en_example_table`: список словарей, содержащий данные таблицы `en_word_table`.
    - `ru_word_dict`: список словарей, содержащий данные таблицы `ru_word_table`.
    - `en_lvl_dict`: список словарей, содержащий данные таблицы `en_level_table`.
    - `pos_name_dict`: список словарей, содержащий данные таблицы `en_pos_table`.

```python
def get_db_dict_data(data_list:list) -> list:
    ...
    return [en_db_dict, en_word_dict, en_example_dict, ru_word_dict, en_lvl_dict, pos_name_dict]
```

-----------------------------

#### fill_tables (функция)

Заполняет таблицы БД пользователя Postgres.

**Местоположение:** файл `table_filling.py`.

- **Вводной параметр:**
  - `db_name`: название базы данных.
  - `user`: имя пользователя Postgres.
  - `password`: пароль пользователя Postgres.
  - `class_list`: список классов, задействованных для построения таблиц в рамках ORM `sqlalchemy`.
  - `dict_list`: список словарей, полученный в результате отработки функции `get_db_dict_data`.

- **Выводной параметр параметр:**
    - `True/False:` булевы значения, отражающие успешную/неудачную загрузку данных в БД пользователя Postgres.
      - `True:` успешная запись данных в БД.
      - `False:` неудачная запись данных в БД.

```python
def fill_tables(db_name:str, user:str, password:str, class_list:list, dict_list:list) -> bool:
    ..
    except exc.IntegrityError:
      print("exc.IntegrityError: данные по указанным значениям уже существуют")
      return False

    session.close()
    return True
```

-----------------------------

#### get_db_table (функция)

Выводит данные из БД пользователя Postgres.

**Местоположение:** файл `db_get_table.py`.

- **Вводной параметр:**
  - `db_name`: название базы данных.
  - `user`: имя пользователя Postgres.
  - `password`: пароль пользователя Postgres.
  - `host`: хост, относительно которого проводится вызов базы данных.
  - `port`: порт.

- **Выводной параметр:**
  - `english_data`: список, содержащий данные по каждому учтенному английскому слову (английское слово, транскрипция, ссылка на MP3-файл, часть речи, требуемый уровень владения английским, пример на русском и английском языках, перевод английского слова).

```python
def get_db_table(db_name:str, user:str, password:str, host: str = 'localhost', port: str = '5432') -> list:
    ...
    return english_data
```

-----------------------------

#### read_database (функция)

Читает данные, содержащиеся в csv-файле `database.csv`.

**Местоположение:** файл `database.py`.

- **Вводной параметр:**
  - `path`: путь к CSV-файлу.

- **Выводной параметр:**
  - `data_list`: лист с базой данных английских слов.

```python
def read_database(path:str) -> list:
    ...
    return data_list
```

-----------------------------

#### create_and_fill_db (функция)

Выполняет весь функционал, представленный в предыдущих функциях раздела №2.

**Местоположение:** файл `database.py`.

- **Вводные параметры:**
  - `db_name`: название базы данных.
  - `user`: имя пользователя Postgres.
  - `password`: пароль пользователя Postgres.
  - `csv_path`: путь к CSV-файлу.

```python
def create_and_fill_db(db_name:str, user:str, password:str, csv_path:str) -> None:
    ...
```

-----------------------------

## 3. Настройка чат-бота Telegram (папка telebot_connection + файл main.py)

#### form_db_dict (функция)

Формирует структуру словаря по заданным значениям. Необходима для реализации добавления нового слова в БД пользователя Telegram (не путать с БД пользователя Postgres).

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `en_word`: английское слово.
  - `ru_word`: перевод английского слова.
  - `en_trans`: транскрипция английского слова.
  - `mp_3_url`: URL-ссылка на MP3-файл произношения английского слова.
  - `en_lvl_code`: код уровня знания английского языка (т.е. a1, a2 и т.д.).
  - `en_lvl_name`: название уровня знания английского языка (т.е. Intermediate, Upper-Intermediate и т.д.).
  - `en_example`: пример предложения с использованием английского слова.
  - `ru_example`: перевод предложения `en_example`.

- **Выводной параметр:**
  - словарь с вводными параметрами.

```python
def form_db_dict(en_word:str, ru_word: str, en_trans:str='', mp_3_url:str='', en_lvl_code:str='none', en_lvl_name:str='unidentified', en_example:str='No example', ru_example:str='Пример отсутствует') -> dict:

    return {'en_word': en_word, 'en_trans': en_trans, 'mp_3_url': mp_3_url, 'en_lvl_code': en_lvl_code, 'en_lvl_name': en_lvl_name, 'en_example': en_example, 'ru_example': ru_example, 'ru_word': ru_word}
```

-----------------------------

#### word_count (функция)

Выводит количество уникальных английских слов, содержащихся в БД пользователя Telegram.

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводной параметр:**
  - `user_database`: список с данными по английским словам, принадлежащим БД пользователя Telegram.

- **Выводной параметр:**
  - количество уникальных английских слов, содержащихся в БД пользователя Telegram.

```python
def word_count(user_database:list) -> int:

    return len(set([word_dict.get('en_word') 
                for word_dict in user_database]))
```

-----------------------------

#### print_answer (функция)

Выводит ответ чат-бота Telegram относительно наличия слова и их количества в БД пользователя Telegram.

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `cid`: ID чата, в рамках которого формируется БД пользователя Telegram.
  - `user_database`: список с данными по английским словам, принадлежащим БД пользователя Telegram.
  - `new_word_bool`: переменная булевого типа, отражающая факт наличия нового слова.  
      - `False:` отсутствие нового слова.
      - `True:` наличие нового слова.

```python
from telebot import TeleBot

def print_answer(bot:TeleBot, cid:int, user_database:list, new_word_bool:bool = False) -> None:
    ...
```

- **Результат работы функции:** 
  - вывод фразы *"Английское слово уже существует в пользовательской базе данных"* в случае, если `new_word_bool` равен `False`.
  - вывод количества слов в БД пользователя Telegram.

-----------------------------

#### get_en_lvl_code (функция)

Формирует код требуемого уровня знания английского языка во время парсинга [онлайн-словаря Оксфордского университета](https://www.oxfordlearnersdictionaries.com/definition/english/ "Онлайн-словарь Оксфордского университета") (функция `get_oxford_dict_data`).

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводной параметр:**
  - `item`: объект класса `Tag`, позволяющий найти нужную информацию в HTML-коде веб-сайта по тегам и атрибутам.

- **Выводной параметр:**
  - `en_lvl_code`: строка, обозначающая код требуемого знания языка. В случае его отсутствия выводит строку `'none'`.

```python
import bs4

def get_en_lvl_code(item:bs4.element.Tag) -> str:
    ...
    return en_lvl_code
```

-----------------------------

#### get_oxford_dict_data (функция)

Выводит данные по английскому слову из [онлайн-словаря Оксфордского университета](https://www.oxfordlearnersdictionaries.com/definition/english/ "Онлайн-словарь Оксфордского университета") (ссылка на MP3-файл, требуемый уровень знания английского языка).

Функция применяется в отношении тех слов, которые необходимо добавить в БД Telegram.

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `en_word`: английское слово.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
  - `data_dict`: словарь с данными относительно английского слова, которое необходимо добавить в БД пользователя Telegram (ссылка на MP3-файл, требуемый уровень знания английского языка).

```python
def get_oxford_dict_data(en_word:str, os:str, browser:str) -> dict:
    ...
    return data_dict
```

-----------------------------

#### receive_pos_oxford_dict_data (функция)

Выводит данные по английскому слову из [онлайн-словаря Оксфордского университета](https://www.oxfordlearnersdictionaries.com/definition/english/ "Онлайн-словарь Оксфордского университета") с фильтрацией относительно части речи (`pos`) и учетом отсутствия тех или иных данных.

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `en_word`: английское слово.
  - `pos`: название части речи.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
  - `(mp_3_url, en_lvl_code, en_lvl_name)`: кортеж с данными по английским словам.
    - `mp_3_url`: ссылка на MP3-файл (в случае ее отсутствия выводится пустая строка `''`).
    - `en_lvl_code`: код требуемого знания английского языка (в случае его отсутствия выводится строка `'none'`).
    - `en_lvl_name`: название уровня знания английского языка (в случае его отсутствия выводится строка `'unidentified'`).

```python
def receive_pos_oxford_dict_data(en_word:str, pos:str, os:str, browser:str) -> tuple:
    ...
    return (mp_3_url, en_lvl_code, en_lvl_name)
```

-----------------------------

#### receive_promt_data (функция)

Выводит перевод нового английского слова, запрашиваемого пользователем Telegram. Перевод выводится посредством парсинга [онлайн-словаря PROMT.One](https://www.online-translator.com/translation/english-russian/, 'Онлайн-словарь PROMT.One').

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `en_word`: английское слово.
  - `pos`: название части речи.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
  - `(ru_word, word_trans, word_en_example, word_ru_example)`: кортеж с данными по английским словам.
    - `ru_word`: перевод нового английского слова.
    - `word_trans`: транскрипция нового английского слова.
    - `word_en_example`: пример английского предложения с новым английским словом.
    - `word_ru_example`: перевод примера английского предложения `word_en_example`.

```python
def receive_promt_data(en_word:str, pos:str, os:str, browser:str) -> tuple:
    ...
    return (ru_word, word_trans, word_en_example, word_ru_example)
```

-----------------------------

#### write_user_mp3 (функция)

Записывает MP3-файл нового английского слова, введенного пользователем Telegram. 

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `en_word`: английское слово.
  - `mp_3_url`: ссылка на MP3-файл.
  - `word_trans`: транскрипция нового английского слова.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

```python
def write_user_mp3(en_word:str, mp_3_url:str, word_trans:str, os:str, browser:str) -> None:
    ...
```

-----------------------------

#### pos_processing (функция)

Извлекает обобщенные данные о новом добавленном английском слове в разрезе конкретной части речи. Данные заполняются в список пользователя Telegram `user_database`.

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `user_database`: список с данными по английским словам, принадлежащим БД пользователя Telegram.
  - `add_en_word`: слово, которое необходимо добавить в БД пользователя Telegram.
  - `pos_list`: список частей речи, учитываемых в разрезе [онлайн-словаря Оксфордского университета](https://www.oxfordlearnersdictionaries.com/definition/english/ "Онлайн-словарь Оксфордского университета") и [онлайн-словаря PROMT.One](https://www.online-translator.com/translation/english-russian/, 'Онлайн-словарь PROMT.One').
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
  - `(pos_check_list, ru_word)`: кортеж с переменными `pos_check_list` и `ru_word`.
    - `pos_check_list`: список с теми частями речи, которые не были задействованы в рамках добавленного английского слова.
    - `ru_word`: перевод нового английского слова в разрезе части речи `pos_check_list`.

```python
def pos_processing(user_database:list, add_en_word:str, pos_list:list, os:str, browser:str) -> tuple:
    ...
    return (pos_check_list, ru_word)
```

-----------------------------

#### update_user_database (функция)

Обновляет данные добавленные в разрезе функции `pos_processing`. Обновление проводится в разрезе id и части речи.

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
    - `pos_check_list`: список с теми частями речи, которые не были задействованы в рамках добавленного английского слова.
    - `user_database`: список с данными по английским словам, принадлежащим БД пользователя Telegram.
    - `last_id`: id последнего словаря, включенного в список `user_database`.

```python
def update_user_database(pos_check_list:list, user_database:list, last_id:int) -> None:
    ...
```

- **Результат работы функции:** Обновление последних добавленных данных в разрезе id и части речи английского слова.

-----------------------------

#### add_en_word (функция)

Реализовывает все функции, включенные в файл файл `add_word.py` (папка telebot_functional).

**Местоположение:** файл `add_word.py` (папка telebot_functional).

- **Вводные параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `cid`: ID чата, в рамках которого формируется БД пользователя Telegram.
  - `user_database`: список с данными по английским словам, принадлежащим БД пользователя Telegram.
  - `add_en_word`: слово, которое необходимо добавить в БД пользователя Telegram.
  - `pos_list`: список частей речи.
  - `os`: название операционной системы в разрезе библиотеки `fake_headers`.
  - `browser`: название браузера в разрезе библиотеки `fake_headers`.

- **Выводной параметр:**
  - `user_database`: обновленный список с базой данных английских слов пользователя Telegram.

```python
def add_en_word(bot:TeleBot, cid:int, user_database:list, add_en_word:str, pos_list:list=['noun', 'verb', 'adjective'], os:str='win', browser:str='chrome'):
    ...
    return user_database
```

-----------------------------

#### get_mp3_audio (функция)

**Местоположение:** файл `audio.py` (папка telebot_functional).

Запускает MP3-файл в чате Telegram.

- **Вводные параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `data`: словарь с данными, фиксируемыми в памяти бота.
  - `hint`: строка, отражающая ответ чат-бота на выбор одного из четырех вариантов слов.
  - `my_message`: сообщение чат-бота, относительно которого параллельно запускается MP3-файл.

```python
import telebot
from telebot import TeleBot

def get_mp3_audio(bot:TeleBot, data:dict, hint:str, 
my_message:telebot.types.Message) -> None:
    ...
```

- **Результат работы функции:** вывод MP3-файла в чате пользователя Telegram.

-----------------------------

#### setup_buttons (функция)

Настраивает клавишный функционал чат-бота Telegram.

**Местоположение:** файл `buttons.py` (папка telebot_functional).

- **Вводные параметры:**
  - `target_word`: целевое английское слово, относительно которого будет настроена одна из четырех выборочных клавиш.
  - `others`: список с остальными английскими словами, относительно которых будут настроены остальные выборочные клавиши.

- **Выводной параметр:**
  - `(buttons, markup)`: кортеж с переменными, затрагивающими клавишный функционал.
    - `buttons`: список объектов класса `KeyboardButton`, отражающих принадлежность клавиш к тому или иному выборочному английскому слову.
    - `markup`: объект класса `ReplyKeyboardMarkup`, отвечающий за формирование разметки клавиатуры и отклик на ее нажатие.

```python
def setup_buttons(target_word:str, others:list) -> tuple:
    ...
    return return (buttons, markup)
```

-----------------------------

#### get_button_states (функция)

Вовзращает названия клавиш, отвечающих за функционал: 1) добавления нового английского слова; 2) удаления имеющегося английского слова; 3) продолжения выбора одного из четырех вариантов ответа.

**Местоположение:** файл `cmd_state.py` (папка telebot_functional).

- **Выводной параметр:**
  - `(add_word_btn_name, delete_word_btn_name, next_word_btn_name)`: кортеж с переменными, отражающими название клавиш.
    - `add_word_btn_name`: название клавиши, отвечающей за добавление нового английского слова.
    - `delete_word_btn_name`: название клавиши, отвечающей за удаление имеющегося английского слова.
    - `next_word_btn_name`: название клавиши, отвечающей за продолжение выбора одного из четырех вариантов ответа.

```python
def get_button_states() -> tuple:
    ...
    return (add_word_btn_name, delete_word_btn_name,next_word_btn_name)
```

-----------------------------

#### get_example (функция)

Выводит пример предложения с использованием выбранного английского слова.

**Местоположение:** файл `example.py` (папка telebot_functional).

- **Вводные параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `message`: объект класса `Message`, позволяющий определить ID чата пользователя Telegram.
  - `markup`: объект класса `ReplyKeyboardMarkup`, отвечающий за формирование разметки клавиатуры и отклик на ее нажатие.
  - `data`: словарь с данными, фиксируемыми в памяти бота.
  - `hint`: строка, отражающая ответ чат-бота на выбор одного из четырех вариантов слов.

```python
def get_example(bot:TeleBot, message:telebot.types.Message, markup:telebot.types.ReplyKeyboardMarkup, data:dict, hint:str) -> None:
    ...
```

- **Результат работы функции:** вывод примера предложения с использованием английского слова в чате пользователя Telegram.

-----------------------------

#### check_known_users (функция)

Проверяет является ли пользователь чат-бота Telegram новым.

**Местоположение:** файл `known_users.py` (папка telebot_functional).

- **Вводные параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `cid`: ID чата, в рамках которого формируется БД пользователя Telegram.
  - `known_users`: список пользователей, не являющихся новыми в чате Telegram.
  - `users_word_dict`: словарь, в котором: 1) ключом выступает номер ID чата пользователя Telegram (`cid`); 2) значением является внутренняя БД пользователя Telegram, прикрепленного к конкретному `cid`.
- `database`: список, содержащий сведения из БД пользователя Postgres (не путать с БД пользователя Telegram).

```python
def check_known_users(bot:TeleBot, cid:int, known_users:list, users_word_dict:dict, database:list) -> None:
    ...
```

- **Результат работы функции:** проверка наличия нового пользователя чат-бота Telegram.

-----------------------------

#### check_word_letters (функция)

Проверяет наличие английских/русских букв в слове, указанном пользователем во время реализации команд `"Добавить слово"` и `"Удалить слово"`. 

**Местоположение:** файл `letters.py` (папка telebot_functional).

- **Вводные параметры:**
  - `word`: слово, требуещее проверки на наличие английских/русских букв.
  - `eng_bool`: переменная булева типа, отвечающая за выбор английского или русского алфавита.
    - `True`: выбираются только буквы английского алфавита.
    - `False`: выбираются только буквы русского алфавита.

- **Выводной параметр:**
  - переменная булева типа, отражающая соответствие (`True`) или несоответствие (`False`) слова на наличие исключительно английских/русских букв.

```python
def check_word_letters(word:str, eng_bool:bool=True) -> bool:    
    ...
        else:
            return False
    return True
```

-----------------------------

#### hello_text (функция)

Пишет пользователю чат-бота Telegram приветственный текст, описывающий принципы работы чат-бота.

**Местоположение:** файл `text.py` (папка telebot_functional).

- **Выводимый параметр:**
  - строковый текст с информацией о работе чат-бота Telegram.

```python
def hello_text() -> str:
    ...
    return '\n'.join(line.lstrip() for line in text.splitlines())
```

-----------------------------

#### show_hint (функция)

Выводит подсказку в чат Telegram бота при наличии корректного/некорректного выбора одного из четырех вариантов ответа.

**Местоположение:** файл `text.py` (папка telebot_functional).

- **Выводимые параметры:**
  - `*lines`: кортеж, состоящий из строковых аргументов. Они образовывают ответное сообщение чат-бота Telegram в разрезе функции `show_hint`.

```python
def show_hint(*lines:tuple) -> str:
    return '\n'.join(lines)
```

-----------------------------

#### show_target (функция)

Выводит ответ в чат Telegram бота при наличии корректного ответа пользователя на выбор одного из четырех вариантов ответа.

**Местоположение:** файл `text.py` (папка telebot_functional).

- **Вводимый параметр:**
  - `data`: словарь с данными фиксируемыми в памяти бота.

- **Выводимый параметр:**
  - строка, имеющая следующую структуру "целевое английское слово -> перевод целевого английского слова".

```python
def show_target(data:dict) -> str:
    ...
    return f"{target} -> {trans}"
```

-----------------------------

#### get_random_pos_database (функция)

Выводит слова в разрезе рандомно выбранной части речи.

**Местоположение:** файл `words.py` (папка telebot_functional).

- **Вводимый параметр:**
  - `user_database`: список с данными по английским словам, принадлежащим БД пользователя Telegram.
  - `pos_list`: список частей речи. По умолчанию выбираются существительные, глаголы и прилагательные.

- **Выводимый параметр:**
  - `pos_database`: список с данными по английским словам, принадлежащим к рандомно выбранной части речи.

```python
def get_random_pos_database(user_database:list, pos_list:list = ['noun', 'verb', 'adjective']) -> list:
    ...
    return pos_database
```

-----------------------------

#### get_random_words (функция)

Выбирает целевое английское слово (т.е. слово, которое необходимо угадать, зная его перевод).

Помимо этого функция рандомно выбирает три остальных слова, принадлежащих к той же части речи, что и целевое слово.

**Местоположение:** файл `words.py` (папка telebot_functional).

- **Вводимый параметр:**
  - `pos_database`: список с данными по английским словам, принадлежащим БД пользователя Telegram и конкретной части речи. Часть речи уже задана в рамках функции `get_random_pos_database`.

- **Выводной параметр:**
  - `(target_word, translate, random_others, transcription, en_example, ru_example)`: кортеж с данными.
    - `target_word`: целевое слово, которое необходимо угадать пользователю чат-бота Telegram.
    - `translate`: перевод целевого английского слова `target_word`.
    - `random_others`: список остальных трех английских слов, являющихся некорректными вариантами ответа. Выбираются рандомным образом.
    - `transcription`: транскрипция целевого английского слова `target_word`.
    - `en_example`: пример английского предложения с использованием целевого слова `target_word`.
    - `ru_example`: пример русского предложения с использованием перевода `translate`.

```python
def get_random_words(pos_database:list) -> tuple:
    ...
    return (target_word, translate, random_others, transcription, en_example, ru_example)
```

-----------------------------

#### start_game_handler (функция)

Позволяет начать работу с чат-ботом и перейти к следующему выбору одного из четырех вариантов ответа.


**Местоположение:** файл `telebot_connection.py` (папка telebot_connection).

- **Вводимые параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `known_users`: список пользователей, не являющихся новыми в чате Telegram.
  - `users_word_dict`: словарь, в котором: 1) ключом выступает номер ID чата пользователя Telegram (`cid`); 2) значением является внутренняя БД пользователя Telegram, прикрепленного к конкретному `cid`.
  - `database`: список, содержащий сведения из БД пользователя Postgres (не путать с БД пользователя Telegram).

```python
def start_game_handler(bot:TeleBot, known_users:list, users_word_dict:dict, database:list) -> None:
    ...
```

- **Результат работы функции:** начало работы с чат-ботом и переход к отгадыванию английских слов.

-----------------------------

#### delete_word_handler (функция)

Позволяет удалить имеющееся английское слово, введенное пользователем.

**Местоположение:** файл `telebot_connection.py` (папка telebot_connection).

- **Вводимые параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `known_users`: список пользователей, не являющихся новыми в чате Telegram.
  - `users_word_dict`: словарь, в котором: 1) ключом выступает номер ID чата пользователя Telegram (`cid`); 2) значением является внутренняя БД пользователя Telegram, прикрепленного к конкретному `cid`.
  - `database`: список, содержащий сведения из БД пользователя Postgres (не путать с БД пользователя Telegram).

```python
def delete_word_handler(bot:TeleBot, known_users:list, users_word_dict:dict, database:list) -> None:
    ...
```

- **Результат работы функции:** удаление имеющегося английского слова.

-----------------------------

#### add_word_handler (функция)

Позволяет добавить новое английское слово, введенное пользователем.

**Местоположение:** файл `telebot_connection.py` (папка telebot_connection).

- **Вводимые параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).
  - `known_users`: список пользователей, не являющихся новыми в чате Telegram.
  - `users_word_dict`: словарь, в котором: 1) ключом выступает номер ID чата пользователя Telegram (`cid`); 2) значением является внутренняя БД пользователя Telegram, прикрепленного к конкретному `cid`.
  - `database`: список, содержащий сведения из БД пользователя Postgres (не путать с БД пользователя Telegram).

```python
def add_word_handler(bot:TeleBot, known_users:list, users_word_dict:dict, database:list) -> None:
    ...
```

- **Результат работы функции:** добавление нового английского слова.

-----------------------------

#### reply_handler (функция)

Формирует отклик на выбор английского слова пользователем чат-бота Telegram.

**Местоположение:** файл `telebot_connection.py` (папка telebot_connection).

- **Вводимые параметры:**
  - `bot`: объект класса `TeleBot`, позволяющий выполнять функционал чат-бота Telegram (написание сообщения и др.).

```python
def reply_handler(bot:TeleBot) -> None:
    ...
```

- **Результат работы функции:** отклик на выбор английского слова пользователем чат-бота Telegram.

-----------------------------

#### connect_telebot (функция)

Позволяет подключиться к телеграм-боту через класс `TeleBot` и запустить весь функционал, содержащийся в файле `telebot_connection.py`.

**Местоположение:** файл `telebot_connection.py` (папка telebot_connection).

- **Вводимые параметры:**
  - `database`: список, содержащий сведения из БД пользователя Postgres (не путать с БД пользователя Telegram).
  - `token_bot`: токен для подключения к чат-боту Telegram.

```python
def connect_telebot(database:list, token_bot:str) -> None:
    ...
```

- **Результат работы функции:** запуск чат-бота Telegram.

-----------------------------

#### main_function (функция)

Позволяет создать БД Postgres и заполнить ее в случае необходимости, а также подключиться к чат-боту Telegram.

**Местоположение:** файл `main.py`.

- **Вводимые параметры:**
  - `db_name`: название базы данных.
  - `user`: имя пользователя Postgres.
  - `password`: пароль пользователя Postgres.
  - `token`: токен для подключению к чат-боту Telegram.
  - `form_data`: значение булевого типа, отражающее нужно ли заниматься предварительным скачиванием данных посредством веб-парсинга.
    - `False` (по умолчанию): не нужно предварительно парсить данные веб-сайтов Oxford и Promt.
    - `True` (по умолчанию): нужно предварительно парсить данные веб-сайтов Oxford и Promt (функционал файла `data.py` + папки `data_formation`).