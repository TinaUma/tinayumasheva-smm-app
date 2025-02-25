from openai import OpenAI

class ImageGenerator:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def generate_image(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url

if __name__ == '__main__':
    import os
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        img_gen = ImageGenerator(openai_key)
        image_url = img_gen.generate_image("Украшения из кристаллов в позитивном и весёлом стиле")  # Тестовая тема
        print("URL картинки:", image_url)
    else:
        print("Добавь OPENAI_API_KEY в секреты Replit!")