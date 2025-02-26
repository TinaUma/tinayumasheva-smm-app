from flask import Blueprint

smm_bp = Blueprint('smm', __name__)

@smm_bp.route('/dashboard')
def dashboard():
    return "Страница дашборда (пока заглушка)"