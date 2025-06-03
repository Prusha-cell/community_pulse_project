from flask import Blueprint, jsonify, request
from app.models import db
from app.models.category import Category

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Не указано имя категории'}), 400

    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name}), 201


@categories_bp.route('/', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    result = [{'id': c.id, 'name': c.name} for c in categories]
    return jsonify(result)


@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Категория не найдена'}), 404

    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Не указано новое имя категории'}), 400

    category.name = data['name']
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name})


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Категория не найдена'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Категория удалена'})
