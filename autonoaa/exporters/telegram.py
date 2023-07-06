import telebot
import os
import time

def send(config, path, max_el, start_time, sat_name):
    bot = telebot.TeleBot(config['TelegramExporter']['telegram_token'])
    png_files = []

    for file in os.listdir(path):
        if file.endswith(".png"):
            png_files.append(os.path.join(path, file))

    if len(png_files) < 2:
        return False

    media_groups = []

    for i in range(0, len(png_files), 10):
        media_objects = []
        for file in png_files[i:i+10]:
            media_object = telebot.types.InputMediaPhoto(open(file, 'rb'))
            media_objects.append(media_object)
        media_groups.append(media_objects)

    for media_group in media_groups:
        bot.send_media_group(config['TelegramExporter']['telegram_chat'], media_group, timeout = 300)
        time.sleep(30)
    bot.send_message(config['TelegramExporter']['telegram_chat'], f"👆👆👆\n{sat_name}\n{start_time}\nMax Elevation: {max_el}")

