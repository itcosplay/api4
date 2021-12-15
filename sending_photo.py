import telegram
import time

from environs import Env
from os import listdir


def send_photo(image_path, token, chat_id):
    bot = telegram.Bot(token=token)

    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)


def get_images_paths(*args):
    images_paths = []

    for folder in args:
        images = listdir(folder)

        for image in images:
            image = f'{folder}/{image}'
            images_paths.append(image)

    return images_paths


if __name__ == '__main__':
    env = Env()
    env.read_env()
    bot_token = env('BOT_TOKEN')
    chat_id = env('CHAT_ID')
    delay = int(env('DELAY'))
    
    images_paths = get_images_paths (
        'nasa',
        'nasa_epic',
        'spacex'
    )

    while True:
        for image_path in images_paths:
            send_photo(image_path, bot_token, chat_id)
            time.sleep(delay)
