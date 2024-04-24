#!/usr/bin/python3
"""This is the cities"""
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """
    Retrieves the list of cities or creates a new city for a given state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        If the request method is GET:
            A JSON response containing the list of cities associated with the state.
        If the request method is POST:
            A JSON response containing the newly created city.

    Raises:
        404: If the state with the given ID does not exist.
        400: If the request method is POST and the request data is not in JSON format,
             or if the request data is missing the 'name' field.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        cities_list = storage.all(City).values()
        state_cities = [city.to_dict() for city in cities_list if city.state_id == state_id]
        return jsonify(state_cities)

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_city = City(state_id=state_id, **data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def city_list(city_id):
    """
    Retrieves, updates, or deletes a City object based on the HTTP method.

    Args:
        city_id (str): The ID of the City object.

    Returns:
        If the HTTP method is GET:
            A JSON representation of the City object.
        If the HTTP method is PUT:
            A JSON representation of the updated City object.
        If the HTTP method is DELETE:
            An empty JSON response with a status code of 200.

    Raises:
        404: If the City object with the specified ID does not exist.
        400: If the request data is not in JSON format.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities', methods=['GET'])
def get_cities():
    """
    Retrieve a list of all cities.

    Returns:
        A JSON response containing a list of dictionaries, where each dictionary represents a city.
    """
    cities_list = storage.all(City).values()
    return jsonify([city.to_dict() for city in cities_list])
