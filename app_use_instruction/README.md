# Запуск чат-бота

- После подключения к чат-боту Telegram нажимаем на клавишу `Start`.
<img src="./instruction_materials/start_1.png" alt="drawing" width="250" height="450"/>
&nbsp;

- Отгадываем правильный перевод английского слова.
<img src="./instruction_materials/start_2.png" alt="drawing" width="250" height="450"/>

---------------------

# Выбор варианта ответа и клавиша "Дальше"

- При выборе неправильного варианта ответа появится крестик.
<img src="./instruction_materials/choice_1.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При выборе корректного варианта ответа появятся MP3-файл и пример использования слова в предложении.
<img src="./instruction_materials/choice_2.png" alt="drawing" width="250" height="450"/>
&nbsp;

- Для продолжения пользователем нажимается клавиша `"Дальше"`.
<img src="./instruction_materials/next.png" alt="drawing" width="250" height="450"/>


---------------------

# Клавиша "Добавить слово"

- После нажатия на клавишу `"Добавить слово"` чат-бот просит пользователя ввести английское слово, которое необходимо добавить в собственную БД.
<img src="./instruction_materials/add_word1.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При добавлении существующего слова чат-бот сообщит о его наличии в базе данных пользователя.
<img src="./instruction_materials/add_word2.png" alt="drawing" width="250" height="450"/>
&nbsp;

- Непредусмотренное нажатие клавиш, содержащих команды `"Дальше"`, `"Добавить слово"` и `"Удалить слово"`, приводит к невозможности обработки их чат-ботом. 
<img src="./instruction_materials/add_word3.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При вводе нового английского слова, существующего в БД онлайн-словарей (Oxford, Promt.One), чат-бот автоматически добавляет его в БД пользователя Telegram.
<img src="./instruction_materials/add_word4.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При вводе нового английского слова, отсутствующего в БД онлайн-словарей (Oxford, Promt.One), чат-бот просит пользователя ввести перевод английского слова. 
<img src="./instruction_materials/add_word5.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При вводе русского слова вместо английского чат-бот просит пользователя Telegram нажать на клавишу `Добавить слово` и повторить попытку.
<img src="./instruction_materials/check_word1.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При вводе английского слова вместо русского чат-бот просит пользователя Telegram нажать на клавишу `Добавить слово` и повторить попытку.
<img src="./instruction_materials/check_word2.png" alt="drawing" width="250" height="450"/>
&nbsp;

---------------------

# Клавиша "Удалить слово"

- Для удаления английского слова из БД пользователя Telegram необходимо нажать на клавишу `"Удалить слово"`.
&nbsp;

- Непредусмотренное нажатие клавиш, содержащих команды `"Дальше"`, `"Добавить слово"` и `"Удалить слово"`, приводит к невозможности обработки их чат-ботом. 
<img src="./instruction_materials/delete_word1.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При отсутствии английского слова в БД пользователя Telegram чат-бот извещает его о невозможности выполнить запрошенную операцию.
<img src="./instruction_materials/delete_word2.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При наличии введенного английского слова в БД пользователя Telegram чат-бот удаляет его и демонстрирует количество оставшихся английских слов.
<img src="./instruction_materials/delete_word3.png" alt="drawing" width="250" height="450"/>
&nbsp;

- При вводе русского слова вместо английского чат-бот просит пользователя Telegram нажать на клавишу `Удалить слово` и повторить попытку.
<img src="./instruction_materials/check_word3.png" alt="drawing" width="250" height="450"/>
&nbsp;