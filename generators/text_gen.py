from openai import OpenAI
import os

class TextGenerator:
    def __init__(self, openai_key, tone, topic):
        self.client = OpenAI(api_key=openai_key)
        self.tone = tone
        self.topic = topic

    def generate_post(self):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Если нет доступа, замени на "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "Ты высококвалифицированный SMM специалист, который будет помогать в генерации текста для постов с заданной мне тематикой и заданным тоном."},
                    {"role": "user", "content": f"Сгенерируй пост для соцсетей с темой '{self.topic}', используя тон: '{self.tone}'"}
                ]
            )
            print(response.choices[0].message.content)
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == '__main__':
    # Берем ключ из секретов Replit
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        generator = TextGenerator(openai_key=api_key, tone="Дружелюбный", topic="Уличная мода")
        generator.generate_post()
    else:
        print("Добавь OPENAI_API_KEY в секреты Replit!")