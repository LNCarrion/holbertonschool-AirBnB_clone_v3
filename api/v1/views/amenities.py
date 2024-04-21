#!/usr/bin/python3

from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
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
