from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.user import User

app = Flask(__name__)
users_api = Blueprint('users_api', __name__)


@users_api.route('/api/v1/users', methods=['GET'])
def get_users():
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@users_api.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@users_api.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@users_api.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    data = request.json
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@users_api.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200


