
from pprint import pprint
import json
from tqdm import tqdm
import requests

# Формируем класс для создания папки на яндекс диске
class YD:
    def __init__(self, token):
        self.headers = {'Authorization': f'OAuth {token}'}

    def create_folder(self, folder_name):
        url_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {"path": folder_name}
        response = requests.put(url_create_folder, headers=self.headers, params=params)
        return response.status_code


# Создаем класс для получения ссылок на фото из VK
class VK:
    base_url = 'https://api.vk.com/method'
    def __init__(self, access_token, user_id, version):
        self.access_token = access_token
        self.user_id = user_id
        self.version = version
        self.params = {"access_token": self.access_token, "v": self.version}

    def photo_info(self, count):
        params = {'owner_id': self.user_id,'album_id': 'profile',"extended": 1, 'count': count}
        response = requests.get(f'{self.base_url}/photos.get', params={**self.params,**params})
        return response.json()

# Создаем функцию для сохрвнения полученных с профиля VK фото на яндекс диск
def saving_photos(id_VK, token_YD, name_folder, count_photos=5):
    client_YD = YD(token_YD)
    client_YD.create_folder(name_folder)
    client_VK = VK('',
                   id_VK,
                       "5.199")

    answer = client_VK.photo_info(count_photos)
    photos_all = answer['response']['items']
    # ранжируем литеры размерного ряда фото
    s,m,x,o,p,q,r,y,z,w = 1,2,3,4,5,6,7,8,9,10
    # создаем необходимый список фото с максимальными размерами
    photos_list = []
    for item in photos_all:
        photo_size_likes = {}
        max_size = 's'
        max_url = ''
        for size in item['sizes']:
             if eval(size['type']) >= eval(max_size):
                max_size = size['type']
                max_url = size['url']
        photo_size_likes['file_name'] = f'{item['likes']['count']}_{item['date']}'
        photo_size_likes['size'] = max_size
        photo_size_likes['url'] = max_url
        photos_list.append(photo_size_likes)

    # загрузка файлов на яндекс диск
    for photo in tqdm(photos_list):
        requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                      params={'url': photo['url'], 'path': f'{name_folder}/{photo['file_name']}.jpg'},
                      headers=client_YD.headers)
    # создаем json-файл
    for photo in photos_list:
        del photo ["url"]
    with open("photos.json", "w") as file:
        json.dump(photos_list, file, indent=4)

# запуск программы
id_VK = str(input("Введите id_VK"))
token_YD = str(input("Введите token яндекс диска"))
name_folder = str(input("Введите имя папки на диске"))
count = int(input("Введите количество фото для отправки (по умолчанию 5)"))

saving_photos(id_VK,token_YD,name_folder)



