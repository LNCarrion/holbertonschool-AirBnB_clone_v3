#!/usr/bin/python3
""" flask route """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage

@app_views.route('/status')
def status():
    """ returns status """
    statok = {"status": "OK"}
    return jsonify(statok)

@app_views.route('/stats', methods=['GET'])
def stats():
    """ function to return the count of all class objects """
    if request.method == 'GET':
        response = {}
        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)
