#!/usr/bin/python3
"""REST Users API"""
from flask import abort, Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """show all users in json format """
    users = []
    for user in storage.all('User').values():
        users.append(user.to_json())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """retrieve user matching id """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete user matching id"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """create new user"""
    kwargs = request.get_json()

    if kwargs is None:
        return ('Not a JSON', 400)
    if 'email' not in kwargs:
        return ('Missing email', 400)
    if 'password' not in kwargs:
        return ('Missing password', 400)

    new_user = User(**kwargs)
    new_user.save()
    return (jsonify(new_user.to_json()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """update an attribute in user"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return ('Not a JSON', 400)
    for k, v in kwargs.items():
        setattr(user, k, v)
        user.save()
    return (jsonify(user.to_json()), 200)
