#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """
    Retrieves the list of all State objects or creates a new State object
    GET:
        Returns a JSON representation of all State objects
    POST:
        Creates a new State object based on the JSON body of the request
    Returns:
        JSON representation of the State object(s) or an error message
    """
    if request.method == 'GET':
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_state = State(**data)
        new_state.save()


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state(state_id):
    """
    Retrieves, updates or deletes a State object based on its ID
    Args:
        state_id (str): The ID of the State object
    GET:
        Returns a JSON representation of the State object
    PUT:
        Updates the State object based on the JSON body of the request
    DELETE:
        Deletes the State object
    Returns:
        JSON representation of the State object or an error message
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
