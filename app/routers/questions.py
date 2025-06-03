from flask import Blueprint, jsonify, request
# from app.models.questions import Question
# from app.models import db

from flask import request, jsonify
from pydantic import ValidationError

from app.models import db, Category
from app.models.questions import Question
from app.schemas.question import QuestionCreate, QuestionResponse


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()

    questions_data = [
        {
            'id': q.id,
            'text': q.text,
            'category': {
                'id': q.category.id,
                'name': q.category.name
            } if q.category else None
        }
        for q in questions
    ]
    return jsonify(questions_data)



@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()

    try:
        question_data = QuestionCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    # Проверка существования категории (необязательно, но желательно)
    if question_data.category_id:
        category = Category.query.get(question_data.category_id)
        if not category:
            return jsonify({'error': 'Категория не найдена'}), 400

    question = Question(
        text=question_data.text,
        category_id=question_data.category_id
    )
    db.session.add(question)
    db.session.commit()

    # Формируем ответ с категорией
    response = {
        'id': question.id,
        'text': question.text,
        'category': {
            'id': question.category.id,
            'name': question.category.name
        } if question.category else None
    }
    return jsonify(response), 201


# @questions_bp.route('/', methods=['POST'])
# def create_question():
#     """Создание нового вопроса."""
#     data = request.get_json()  # Получаем данные из запроса в формате JSON
#     if not data or 'text' not in data:
#         # Проверяем, что текст вопроса присутствует в данных
#         return jsonify({'error': 'No question text provided'}), 400
#
#     # Создаем экземпляр вопроса
#     question = Question(text=data['text'])
#     db.session.add(question)  # Добавляем вопрос в сессию для записи
#     db.session.commit()  # Фиксируем изменения в базе данных
#     return jsonify({'message': 'Вопрос создан', 'id': question.id}), 201


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Получение деталей конкретного вопроса по его ID."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404
    return jsonify({'message': f"Вопрос: {question.text}"}), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Обновление конкретного вопроса по его ID."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
        db.session.commit()
        return jsonify({'message': f"Вопрос обновлен: {question.text}"}), 200
    else:
        return jsonify({'message': "Текст вопроса не предоставлен"}), 4


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление конкретного вопроса по его ID."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200
