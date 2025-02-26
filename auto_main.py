import os
from generators.text_gen import TextGenerator
from generators.image_gen import ImageGenerator
from vk_publisher import VKPublisher
from vk_stats import VKStats
import datetime
import time

if __name__ == '__main__':
    openai_key = os.getenv("OPENAI_API_KEY")
    vk_token = os.getenv("VK_TOKEN")
    group_id = 229537513  # Замени на свой ID группы

    if openai_key and vk_token and group_id:
        # Генерация и публикация поста
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

        # Ждём 5 секунд для обновления статистики
        time.sleep(5)

        # Получение статистики
        stats = VKStats(vk_token, group_id)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        stats.get_stats(week_ago, today)
        stats.get_followers()
    else:
        print("Добавь OPENAI_API_KEY, VK_TOKEN и укажи group_id в коде!")