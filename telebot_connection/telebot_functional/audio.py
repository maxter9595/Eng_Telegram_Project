import telebot
from telebot import TeleBot

def get_mp3_audio(bot:TeleBot, data:dict, hint:str, 
                my_message:telebot.types.Message) -> None:

    if 'Допущена ошибка!' not in hint:
        
        try:
            word = data['target_word']
            transcription = data['transcription']
            
            if transcription.split():
                mp3_name = f"{word} {transcription}.mp3"
                
            else:
                mp3_name = f"{word}"[::-1].\
                    replace(" ", "", 1)[::-1] + '.mp3'
                
            mp3_path = f"data/eng_audio_files_mp3/{mp3_name}"
            
            bot.send_audio(my_message.chat.id, 
                            open(mp3_path, 'rb'), 
                            title=f"{mp3_name}", 
                            performer="Translator")
            
            print(f'MP3 файл загружен: {mp3_path}')

        except FileNotFoundError:
            print(f'Аудиозапись слова не удалось найти: {mp3_path}')