# telegram_bot.py

import os
import time
from telebot import TeleBot
from telebot import types
from vk_processor import upload_audio_file, process_audio, get_upload_url, check_status
from audio_manager import move_to_archive

# Инициализация Telegram Bot
bot = TeleBot("7161892299:AAGauiJPQdsSRXWrgnYuxGnxxFFAjtOOZ_4")

# ID пользователя, которому будет отправлен запрос на обработку файла
user_id = 148918255

# Путь к папке, которую мы мониторим
folder_path = 'audio'

# Словарь для хранения информации о файлах
files_info = {}


# Функция для отправки запроса пользователю в Telegram Bot
def send_request(file_name):
    # Создаем клавиатуру с inline кнопками "Да" и "Нет"
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("Да", callback_data=f"process_{file_name}")
    btn_no = types.InlineKeyboardButton("Нет", callback_data="cancel")
    keyboard.add(btn_yes, btn_no)

    bot.send_message(user_id, f"Хотите обработать файл '{file_name}'?", reply_markup=keyboard)


# Обработчик команды /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для обработки аудиофайлов. Жду новых файлов в папке 'audio'.")

"""
# Обработчик кнопки "Да" для запроса обработки файла
@bot.message_handler(func=lambda message: True)
def handle_request(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Файл будет обработан.")
        file_name = message.text.split("'")[1]
        file_path = os.path.join(folder_path, file_name)
        print(file_path)
        # Получаем адрес сервера для загрузки аудиозаписи в VK
        upload_url = get_upload_url(access_token)

        # Загружаем аудиозапись на сервер VK
        audio_data = upload_audio_file(upload_url, file_path)

        # Запускаем распознавание аудиозаписи
        model = "spontaneous"  # Модель распознавания речи
        task_id = process_audio(access_token, audio_data, model)

        # Проверяем статус обработки аудиозаписи в VK
        status = check_status(access_token, task_id)
        while status['status'] != 'finished':
            time.sleep(5)  # Подождем 5 секунд перед повторной проверкой
            status = check_status(access_token, task_id)

        # Если аудиозапись успешно обработана, передаем результат в OpenAI для суммаризации
        if status['status'] == 'finished':
            transcription = status['text']

            # Перемещаем обработанный файл в папку "archive"
            move_to_archive(file_name)

            # Отправляем запрос на обработку транскрипции
            send_request(file_name, transcription)

    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Ок, файл не будет обработан.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки для ответа.")
"""