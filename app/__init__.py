import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my-super-secret-key-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    from app.auth import auth_bp
    from app.smm import smm_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(smm_bp, url_prefix='/smm')

    @app.route('/')
    def home():
        return "Добро пожаловать в SMM-ассистент!"

    with app.app_context():
        print("Создаём базу данных...")
        db.create_all()
        print("База данных создана!")
        print(f"Путь к базе: {os.path.abspath('site.db')}")

    return app