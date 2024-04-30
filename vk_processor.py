# vk_processor.py

import requests
import json

# Функция для загрузки аудиозаписи на сервер VK
def upload_audio_file(upload_url, audio_file_path):
    files = {'file': open(audio_file_path, 'rb')}
    response = requests.post(upload_url, files=files)
    return response.json()

# Функция для запуска распознавания аудиозаписи
def process_audio(access_token, audio_data, model):
    url = "https://api.vk.com/method/asr.process"
    params = {
        "access_token": access_token,
        "v": "5.131",  # Версия API
        "audio": json.dumps(audio_data),
        "model": model
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data['response']['task_id']

# Функция для получения адреса сервера для загрузки аудиозаписи
def get_upload_url(access_token):
    url = "https://api.vk.com/method/asr.getUploadUrl"
    params = {
        "access_token": access_token,
        "v": "5.131"  # Версия API
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['response']['upload_url']

# Функция для проверки статуса задачи на обработку аудиозаписи
def check_status(access_token, task_id):
    url = "https://api.vk.com/method/asr.checkStatus"
    params = {
        "access_token": access_token,
        "v": "5.131",  # Версия API
        "task_id": task_id
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['response']
