from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
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
    cities_list = storage.all(City).values()
    return jsonify([city.to_dict() for city in cities_list])
