from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.user import User

app = Flask(__name__)
users_api = Blueprint('users_api', __name__)


@users_api.route('/api/v1/users', methods=['GET'])
def get_users():
    """
    Retrieve all users from the database and return them as a JSON response.

    Returns:
        A JSON response containing a list of dictionaries, where each dictionary represents a user.
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@users_api.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a user by their ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        dict: A dictionary representing the user's information.

    Raises:
        404: If the user with the specified ID does not exist.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@users_api.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by their ID.

    Args:
        user_id (str): The ID of the user to be deleted.

    Returns:
        tuple: A tuple containing an empty JSON response and a status code of 200.

    Raises:
        404: If the user with the specified ID does not exist.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@users_api.route('/api/v1/users', methods=['POST'])
def create_user():
    """
    Create a new user.

    This function is responsible for creating a new user by receiving a JSON
    object in the request body. The JSON object should contain the 'email' and
    'password' fields. If the request is not in JSON format or if any of the
    required fields are missing, the function will return a 400 error.

    Returns:
        A JSON response containing the newly created user's information and a
        status code of 201.

    Raises:
        400: If the request is not in JSON format or if any of the required
        fields are missing.
    """
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
    """
    Update a user with the given user_id.

    Args:
        user_id (str): The ID of the user to be updated.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
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


