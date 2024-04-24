#!/usr/bin/python3
"""This is the amenities """
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """
    Retrieves a list of amenities or creates a new amenity.

    GET request:
        Retrieves a list of all amenities in the storage.

    POST request:
        Creates a new amenity based on the provided JSON data.

    Returns:
        - If GET request: a JSON response containing a list of amenities.
        - If POST request: a JSON response containing the newly created amenity.

    Raises:
        - 400 Bad Request: If the request is not a valid JSON or if the 'name' field is missing.
    """
    if request.method == 'GET':
        amenities_list = storage.all(Amenity).values()
        return jsonify([amenity.to_dict() for amenity in amenities_list])

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenity_list(amenity_id):
    """
    Retrieve, update or delete an amenity.

    Args:
        amenity_id (str): The ID of the amenity to retrieve, update or delete.

    Returns:
        If the request method is 'GET':
            A JSON representation of the amenity.

        If the request method is 'PUT':
            A JSON representation of the updated amenity.

        If the request method is 'DELETE':
            An empty JSON response with a status code of 200.

    Raises:
        404: If the amenity with the specified ID does not exist.

        400: If the request method is 'PUT' and the request body is not a valid JSON.

    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())

    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
