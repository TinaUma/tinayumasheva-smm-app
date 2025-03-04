import os
from flask import Blueprint, render_template, session, redirect, url_for, request
from generators.text_gen import TextGenerator
from generators.image_gen import ImageGenerator
from vk_publisher import VKPublisher

smm_bp = Blueprint('smm', __name__)

@smm_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    openai_key = os.getenv("OPENAI_API_KEY")
    vk_token = os.getenv("VK_TOKEN")
    group_id = 229537513  # Твой ID группы

    if not (openai_key and vk_token):
        return "Добавь OPENAI_API_KEY и VK_TOKEN в .env!"

    content = ""
    image_url = ""
    if request.method == 'POST':
        post_gen = TextGenerator(openai_key, tone="позитивный и веселый", topic="Украшения от Сваровски")
        content = post_gen.generate_post()
        img_desc = post_gen.generate_post_image_description()

        img_gen = ImageGenerator(openai_key)
        image_url = img_gen.generate_image(img_desc)

        vk_pub = VKPublisher(vk_token, group_id)
        vk_pub.publish_post(content, image_url)

    return render_template('dashboard.html', content=content, image_url=image_url)