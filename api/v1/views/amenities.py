#!/usr/bin/python3
"""REST Amenities API"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """show all amenities in json format """
    amenities = []
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_json())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """retrieve amenity matching id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete amenity matching id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create new amenity """
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    if 'name' not in kwargs:
        return ('Missing name', 400)

    new_amenity = Amenity(**kwargs)
    new_amenity.save()
    return (jsonify(new_amenity.to_json()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_update_amenity(amenity_id):
    """update an attribute in amenity"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    for k, v in kwargs.items():
        setattr(amenity, k, v)
    amenity.save()
    return (jsonify(amenity.to_json()), 200)
