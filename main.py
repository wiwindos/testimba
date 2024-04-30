import os
import time
from threading import Thread
from telegram_bot import bot, send_request
from vk_processor import get_upload_url, upload_audio_file, process_audio, check_status
from audio_manager import move_to_archive

# Путь к папке, которую мы мониторим
folder_path_search = 'audio'
folder_path_arch = 'archive'
access_token = ""

# Создаем папку "archive", если она еще не создана
archive_path = 'archive'
if not os.path.exists(archive_path):
    os.makedirs(archive_path)


# Обработчик нажатия на inline кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data.startswith('process_'):
        # Если нажата кнопка "Да", обработаем файл
        file_name = call.data.split('_')[1]
        bot.send_message(call.message.chat.id, f"Файл '{file_name}' будет обработан.")
        file_path = os.path.join(folder_path_arch, file_name)

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

        # Если аудиозапись успешно обработана, перемещаем файл в папку "archive"
        if status['status'] == 'finished':
            bot.send_message(call.message.chat.id, f"Рашифровка '{file_name}': '{status['text']}' будет обработан.")

    elif call.data == "yes":
        bot.send_message(call.message.chat.id, "Файл будет обработан.")
        # Добавьте здесь необходимую логику для обработки нажатия кнопки "Да"
        # Удаляем кнопку "Да" после нажатия
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Ок, файл не будет обработан.")
        # Добавьте здесь необходимую логику для обработки нажатия кнопки "Нет"
        # Удаляем кнопку "Да" после нажатия
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


# Функция мониторинга папки audio
def monitor_audio_folder():
    while True:
        # Получаем список файлов в папке "audio"
        files = os.listdir(folder_path_search)

        # Проверяем каждый файл
        for file_name in files:
            # Проверяем, является ли файл аудиофайлом
            if file_name.endswith(".wav"):
                # Отправляем запрос на обработку файла в Telegram
                send_request(file_name)
                move_to_archive(file_name)
        time.sleep(5)  # Проверяем папку каждые 5 секунд

# Запускаем мониторинг папки в отдельном потоке
folder_monitor_thread = Thread(target=monitor_audio_folder)
folder_monitor_thread.start()

# Запускаем обработку команд телеграм-бота
bot.infinity_polling()
