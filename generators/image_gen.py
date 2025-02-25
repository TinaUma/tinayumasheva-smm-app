from openai import OpenAI
import os

class ImageGenerator:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def generate_image(self, prompt):
        try:
            response = self.client.images.generate(
                model="dall-e-3",  # Если ошибка, замени на "dall-e-2"
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            return image_url
        except Exception as e:
            print(f"Ошибка генерации картинки: {e}")
            return None

if __name__ == '__main__':
    # Бери ключ из секретов Replit
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        generator = ImageGenerator(openai_key=openai_key)
        image_url = generator.generate_image("Уличная мода в дружелюбном стиле, яркие цвета")
        if image_url:
            print(f"Картинка готова: {image_url}")
    else:
        print("Добавь OPENAI_API_KEY в секреты Replit!")