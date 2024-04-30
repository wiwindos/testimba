import os
import time
from telebot import TeleBot
from telebot import types  # Импортируем модуль types для работы с клавиатурой

# Инициализация Telegram Bot
bot = TeleBot("7161892299:AAGauiJPQdsSRXWrgnYuxGnxxFFAjtOOZ_4")

# ID пользователя, которому будет отправлен запрос на обработку файла
user_id = 148918255

# Путь к папке, которую мы мониторим
folder_path = 'audio'

# Путь к папке, в которую перемещаем обработанные файлы
archive_path = 'archive'

# Словарь для хранения информации о файлах
files_info = {}

# Функция для отправки запроса пользователю в Telegram Bot
def send_request(file_name):
    bot.send_message(user_id, f"Хотите обработать файл '{file_name}'?", reply_markup=keyboard)

# Функция для перемещения файла в папку "archive"
def move_to_archive(file_name):
    source_path = os.path.join(folder_path, file_name)
    target_path = os.path.join(archive_path, file_name)
    os.rename(source_path, target_path)

# Функция для обработки новых файлов в папке
def process_new_files():
    global files_info
    for file_name in os.listdir(folder_path):
        # Проверяем, является ли элемент файлом (а не папкой)
        if os.path.isfile(os.path.join(folder_path, file_name)):
            # Проверяем, был ли файл уже обработан
            if file_name not in files_info:
                # Отправляем запрос на обработку
                send_request(file_name)
                # Добавляем файл в словарь files_info
                files_info[file_name] = True

# Обработчик команды /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для обработки аудиофайлов. Жду новых файлов в папке 'audio'.")

# Обработчик кнопки "Да" для запроса обработки файла
@bot.message_handler(func=lambda message: True)
def handle_request(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Файл будет обработан.")
        file_name = message.text.split("'")[1]
        # Здесь вызываем функцию для загрузки файла в VK и дальнейшей обработки
        # Пример: process_audio_in_vk(file_path)
        move_to_archive(file_name)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Ок, файл не будет обработан.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки для ответа.")

# Основной цикл программы
if __name__ == "__main__":
    # Создаем клавиатуру для запроса обработки файла
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_yes = types.KeyboardButton("Да")
    btn_no = types.KeyboardButton("Нет")
    keyboard.add(btn_yes, btn_no)

    # Запускаем бесконечный цикл мониторинга папки
    while True:
        process_new_files()
        time.sleep(5)  # Проверяем папку каждые 5 секунд
