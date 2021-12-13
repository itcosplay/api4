import os
import requests
import datetime

from pathlib import Path
from urllib.parse import urlparse
from environs import Env


def fetch_spacex_launch():
    launch = 90
    spacex_url = 'https://api.spacexdata.com/v4/launches'
    response = requests.get(spacex_url)
    response.raise_for_status() 
    links = response.json()[launch]['links']['flickr']['original']

    for image_num, link in enumerate(links, start=1):
        extention = get_image_extension_from_url(link)
        filename = f'spacex_{image_num}.{extention}'
        save_image_from_url(link, filename, 'spacex')

  
def get_images_from_NASA(token):  
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'count': 30,
        'api_key': token
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    images_data = response.json()

    for num, single_image_data in enumerate(images_data, start=1):
        image_url = single_image_data['url']
        image_extension = get_image_extension_from_url(image_url)
        filename = f'nasa_image_{num}{image_extension}'
        save_image_from_url(image_url, filename, 'nasa')


def get_EPIC_from_NASA(token):
    url = f'https://api.nasa.gov/EPIC/api/natural/images'
    payload = {
        'api_key': token
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    images_data = response.json()

    for single_image_data in images_data:
        date = datetime.datetime.fromisoformat(single_image_data['date'])
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        image_name = single_image_data['image']

        url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png'

        save_image_from_url(url, f'{image_name}.png', 'nasa_epic', payload)


def save_image_from_url(url, filename, dir_name, params=None):
    Path(f'./{dir_name}').mkdir(parents=True, exist_ok=True)

    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(f'./{dir_name}/{filename}', 'wb') as file:
        file.write(response.content)


def get_image_extension_from_url(url):
    url = urlparse(url)
    ext = os.path.splitext(url.path)

    return ext[1]


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    nasa_token = env('NASA_TOKEN')

    fetch_spacex_launch()
    get_images_from_NASA(nasa_token)
    get_EPIC_from_NASA(nasa_token)