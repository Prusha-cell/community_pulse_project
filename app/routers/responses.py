from flask import Blueprint

response_bp = Blueprint('response', __name__, url_prefix='/responses')

@response_bp.route('/', methods=['GET'])
def get_responses():
    """Получение статистики ответов."""
    return "Статистика всех ответов"

@response_bp.route('/', methods=['POST'])
def add_response():
    """Добавление нового ответа на вопрос."""
    return "Ответ добавлен"
