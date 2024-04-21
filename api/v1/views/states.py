from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET', 'POST'])
def states():
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
        return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state(state_id):
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
