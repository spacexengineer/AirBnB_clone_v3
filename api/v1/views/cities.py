#!/usr/bin/python3
"""Use REST structure with cities in database"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage, CNC
from models.base_model import BaseModel
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Show all cities in json format with GET request"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = []
    for city in storage.all('City').values():
        if city.state_id == state.id:
            cities.append(city.to_json())
    return (jsonify(cities))


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieve city matching id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete city matching id with DELETE request"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_new_city(state_id):
    """create new city"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    if 'name' not in kwargs:
        return ('Missing name', 400)

    new_city = City(**kwargs)
    new_city.state_id = state_id
    new_city.save()
    return (jsonify(new_city.to_json()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_update_city(city_id):
    """Update an attribute in city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    for k, v in kwargs.items():
        setattr(city, k, v)
    city.save()
    return (jsonify(city.to_json()), 200)
