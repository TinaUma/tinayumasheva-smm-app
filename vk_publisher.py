import requests
import os

class VKPublisher:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def upload_photo(self, image_url):
        try:
            upload_url_response = requests.get(
                'https://api.vk.com/method/photos.getWallUploadServer',
                params={
                    'access_token': self.vk_api_key,
                    'v': '5.236',
                    'group_id': self.group_id
                }
            ).json()

            if 'error' in upload_url_response:
                print(f"Ошибка получения upload_url: {upload_url_response['error']['error_msg']}")
                return None

            upload_url = upload_url_response['response']['upload_url']
            print(f"Upload URL: {upload_url}")

            image_data = requests.get(image_url).content
            print(f"Картинка скачана, размер: {len(image_data)} байт")

            upload_response = requests.post(upload_url, files={'photo': ('image.jpg', image_data)}).json()
            print(f"Upload response: {upload_response}")

            if 'photo' not in upload_response:
                print(f"Ошибка загрузки на сервер: {upload_response}")
                return None

            save_response = requests.get(
                'https://api.vk.com/method/photos.saveWallPhoto',
                params={
                    'access_token': self.vk_api_key,
                    'v': '5.236',
                    'group_id': self.group_id,
                    'photo': upload_response['photo'],
                    'server': upload_response['server'],
                    'hash': upload_response['hash']
                }
            ).json()

            if 'error' in save_response:
                print(f"Ошибка сохранения фото: {save_response['error']['error_msg']}")
                return None

            photo_id = save_response['response'][0]['id']
            owner_id = save_response['response'][0]['owner_id']
            attachment = f'photo{owner_id}_{photo_id}'
            print(f"Фото загружено: {attachment}")
            return attachment

        except Exception as e:
            print(f"Ошибка в upload_photo: {e}")
            return None

    def publish_post(self, content, image_url=None):
        params = {
            'access_token': self.vk_api_key,
            'from_group': 1,
            'v': '5.236',
            'owner_id': f'-{self.group_id}',
            'message': content
        }
        if image_url:
            attachment = self.upload_photo(image_url)
            if attachment:
                params['attachments'] = attachment
            else:
                print("Картинка не прикреплена из-за ошибки загрузки")

        response = requests.post('https://api.vk.com/method/wall.post', params=params).json()
        if 'error' in response:
            print(f"Ошибка публикации: {response['error']['error_msg']}")
        else:
            print("Пост опубликован в ВК!")
        return response