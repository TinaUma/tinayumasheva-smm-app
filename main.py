import os
from generators.text_gen import TextGenerator  # Исправлено: generators и text_gen
from generators.image_gen import ImageGenerator  # Исправлено: generators и image_gen
from vk_publisher import VKPublisher

if __name__ == '__main__':
    # Бери ключи из секретов Replit
    openai_key = os.getenv("OPENAI_API_KEY")
    vk_token = os.getenv("VK_TOKEN")
    group_id = 229537513  # Замени на ID твоей группы (без минуса)

    if openai_key and vk_token and group_id:
        # Генерация текста и описания
        post_gen = TextGenerator(openai_key, tone="позитивный и веселый", topic="Новая коллекция кухонных ножей от компании ZeroKnifes")
        content = post_gen.generate_post()
        img_desc = post_gen.generate_post_image_description()

        # Генерация картинки
        img_gen = ImageGenerator(openai_key)
        image_url = img_gen.generate_image(img_desc)

        # Публикация в ВК
        vk_pub = VKPublisher(vk_token, group_id)
        vk_pub.publish_post(content, image_url)

        print("Контент:", content)
        print("URL картинки:", image_url)
    else:
        print("Добавь OPENAI_API_KEY, VK_TOKEN и укажи group_id в коде!")