from openai import OpenAI

class TextGenerator:
    def __init__(self, openai_key, tone, topic):
        self.client = OpenAI(api_key=openai_key)
        self.tone = tone
        self.topic = topic

    def generate_post(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты SMM специалист."},
                {"role": "user", "content": f"Сгенерируй пост с темой '{self.topic}' в тоне '{self.tone}'"}
            ]
        )
        return response.choices[0].message.content

    def generate_post_image_description(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты SMM специалист."},
                {"role": "user", "content": f"Опиши картинку для поста с темой '{self.topic}' в тоне '{self.tone}'"}
            ]
        )
        return response.choices[0].message.content

# Тестовый код для запуска файла отдельно
if __name__ == '__main__':
    import os
    openai_key = os.getenv("OPENAI_API_KEY")  # Бери ключ из секретов Replit
    if openai_key:
        post_gen = TextGenerator(
            openai_key=openai_key,
            tone="позитивный и веселый",  # Тон
            topic="Новая коллекция украшений из кристаллов от Swarovski"  # Тема
        )
        content = post_gen.generate_post()
        print("Сгенерированный пост:", content)
    else:
        print("Добавь OPENAI_API_KEY в секреты Replit!")