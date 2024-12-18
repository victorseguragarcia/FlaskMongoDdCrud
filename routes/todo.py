from flask import Blueprint, jsonify, request
from config.mongo import mongo
from bson.objectid import ObjectId

todo = Blueprint('todo', __name__)

# Obtener todos los "todos"
@todo.route('/', methods=['GET'])
def get_all_todos():
    todos = mongo.db.todos.find()
    todos_list = [{
        '_id': str(todo['_id']),
        'nombre': todo['nombre'],
        'apellidos': todo['apellidos'],
        'peso': todo['peso'],
        'dni': todo['dni'],
        'email': todo['email']
    } for todo in todos]
    return jsonify(todos_list)

# Obtener un "todo" por ID
@todo.route('/<id>', methods=['GET'])
def get_todo_by_id(id):
    todo = mongo.db.todos.find_one({'_id': ObjectId(id)})
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({
        '_id': str(todo['_id']),
        'nombre': todo['nombre'],
        'apellidos': todo['apellidos'],
        'peso': todo['peso'],
        'dni': todo['dni'],
        'email': todo['email']
    })

# Crear un nuevo "todo"
@todo.route('/', methods=['POST'])
def create_todo():
    data = request.get_json()
    required_fields = ['nombre', 'apellidos', 'peso', 'dni', 'email']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    new_todo = {
        'nombre': data['nombre'],
        'apellidos': data['apellidos'],
        'peso': data['peso'],
        'dni': data['dni'],
        'email': data['email']
    }
    result = mongo.db.todos.insert_one(new_todo)
    return jsonify({
        '_id': str(result.inserted_id),
        'nombre': new_todo['nombre'],
        'apellidos': new_todo['apellidos'],
        'peso': new_todo['peso'],
        'dni': new_todo['dni'],
        'email': new_todo['email']
    }), 201

# Actualizar un "todo"
@todo.route('/<id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    
    updated_todo = {}
    if 'nombre' in data:
        updated_todo['nombre'] = data['nombre']
    if 'apellidos' in data:
        updated_todo['apellidos'] = data['apellidos']
    if 'peso' in data:
        updated_todo['peso'] = data['peso']
    if 'dni' in data:
        updated_todo['dni'] = data['dni']
    if 'email' in data:
        updated_todo['email'] = data['email']
    
    if not updated_todo:
        return jsonify({'error': 'No fields to update'}), 400

    result = mongo.db.todos.update_one({'_id': ObjectId(id)}, {'$set': updated_todo})
    if result.matched_count == 0:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'message': 'Todo updated'})

# Eliminar un "todo"
@todo.route('/<id>', methods=['DELETE'])
def delete_todo(id):
    result = mongo.db.todos.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'message': 'Todo deleted'})
