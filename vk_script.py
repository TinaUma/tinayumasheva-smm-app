import os
from generators.text_gen import TextGenerator  # Путь: generators/text_gen.py
from generators.image_gen import ImageGenerator  # Путь: generators/image_gen.py
from vk_publisher import VKPublisher

if __name__ == '__main__':
    openai_key = os.getenv("OPENAI_API_KEY")
    vk_token = os.getenv("VK_TOKEN")
    group_id = 229537513  # Замени на ID твоей группы (без минуса)

    if openai_key and vk_token and group_id:
        post_gen = TextGenerator(
            openai_key=openai_key,
            tone="позитивный и веселый",
            topic="Украшения от Сваровски"
        )
        content = post_gen.generate_post()
        img_desc = post_gen.generate_post_image_description()

        img_gen = ImageGenerator(openai_key)
        image_url = img_gen.generate_image(img_desc)

        vk_pub = VKPublisher(vk_token, group_id)
        vk_pub.publish_post(content, image_url)

        print("Контент:", content)
        print("URL картинки:", image_url)
    else:
        print("Добавь OPENAI_API_KEY, VK_TOKEN и укажи group_id в коде!")