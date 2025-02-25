import requests
import vk_api

class VKPublisher:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id
        self.vk_session = vk_api.VkApi(token=vk_api_key)  # Используем vk_api
        self.vk = self.vk_session.get_api()

    def upload_photo(self, image_url):
        try:
            # Скачиваем картинку
            image_data = requests.get(image_url).content
            with open("temp_image.jpg", "wb") as f:
                f.write(image_data)

            # Загружаем через vk_api
            upload = vk_api.VkUpload(self.vk_session)
            photo = upload.photo_wall("temp_image.jpg", group_id=self.group_id)
            return f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
        except Exception as e:
            print(f"Ошибка загрузки фото: {e}")
            return None

    def publish_post(self, content, image_url=None):
        try:
            params = {
                'from_group': 1,
                'owner_id': f'-{self.group_id}',
                'message': content
            }
            if image_url:
                attachment = self.upload_photo(image_url)
                if attachment:
                    params['attachments'] = attachment

            self.vk.wall.post(**params)
            print("Пост опубликован в ВК!")
        except Exception as e:
            print(f"Ошибка публикации: {e}")