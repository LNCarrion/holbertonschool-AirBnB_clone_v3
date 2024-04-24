#!/usr/bin/python3
"""This is a place handler"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User

app = Flask(__name__)
places_api = Blueprint('places_api', __name__)


@places_api.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """
    Retrieves all places associated with a specific city.

    Args:
        city_id (str): The ID of the city.

    Returns:
        A JSON response containing a list of places associated with the city.

    Raises:
        404: If the city with the given ID does not exist.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@places_api.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieve a specific place by its ID.

    Args:
        place_id (str): The ID of the place to retrieve.

    Returns:
        dict: A dictionary representing the place in JSON format.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@places_api.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Delete a place by its ID.

    Args:
        place_id (str): The ID of the place to be deleted.

    Returns:
        tuple: A tuple containing an empty JSON response and the status code 200.

    Raises:
        404: If the place with the given ID does not exist.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@places_api.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Create a new place in a city.

    Args:
        city_id (str): The ID of the city where the place will be created.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.

    Raises:
        404: If the city with the given ID does not exist.
        400: If the request is not in JSON format, or if the 'user_id' or 'name' fields are missing.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.json
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@places_api.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Update a place with the given place_id.

    Args:
        place_id (str): The ID of the place to be updated.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

