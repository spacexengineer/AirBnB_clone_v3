#!/usr/bin/python3
"""REST Amenities API"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """show all places in json format """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = []
    for place in storage.all('Place').values():
        if place.city_id == city_id:
            places.append(value.to_json())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """retrieve place matching id """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return (jsonify(place.to_json()))


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """delete place matching id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create a new place """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    if 'name' not in kwargs:
        return ('Missing name', 400)
    if 'user_id' not in kwargs:
        return ('Missing user_id', 400)

    new_place = Place(**kwargs)
    new_place.city_id = city_id
    user = storage.get('User', new_place.user_id)
    if user is None:
        abort(404)
    new_place.save()
    return jsonify(new_place.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """update an attribute in place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    for k, v in kwargs.items():
        setattr(place, k, v)
    place.save()
    return (jsonify(place.to_json()), 200)
