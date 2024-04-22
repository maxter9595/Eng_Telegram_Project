import time

import requests

from data_formation.english_html import write_dir
from data_formation.english_html import get_headers


def write_mp3(url:str, file_path:str, os:str, browser:str,
                attempts:int, error_timeout:int) -> bool:
    
    attempt_count = 0
    for _ in list(range(1, attempts + 1)):
        
        if attempts >= attempt_count:
        
            try:
                headers = get_headers(os, browser)
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                
                with open(file_path, "wb") as fout:
                    fout.write(resp.content)
                
                return True
            
            except (requests.exceptions.ConnectTimeout, 
                    requests.exceptions.ReadTimeout, 
                    requests.exceptions.ConnectionError):
                print(f'requests.exceptions: не удалось обработать ссылку {url}')
                time.sleep(error_timeout)
        
        else:
            return False


def get_mp3_files(word_list:list, url_list:list, 
                    transcript_list:list, os:str, 
                    browser:str) -> None:
    
    mp3_dict = {}
    
    for word, url, transcription in zip(word_list, url_list, 
                                        transcript_list):
        
        print(f'Обрабатываю слово {word}')
        
        if transcription:
            mp3_name = f'{word} {transcription}.mp3'
            mp3_path = write_dir('data', 'eng_audio_files_mp3', mp3_name)
            
        else:
            mp3_name = f'{word[::-1].replace(" ", "", 1)[::-1]}.mp3'
            mp3_path = write_dir('data', 'eng_audio_files_mp3', mp3_name)
        
        attempts = 3
        error_timeout = 30
        
        mp3_bool = write_mp3(url, mp3_path, os, browser, 
                                attempts, error_timeout)
        
        if mp3_bool and word not in mp3_dict:
            mp3_dict[word] = mp3_path